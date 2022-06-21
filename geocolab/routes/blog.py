# !/usr/bin/env python
# encoding: utf-8

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, current_user

from ._decorators import admin_required
from ..extensions import db
from ..models import BlogPost, BlogAuthor, User
from ..schemas import BlogPostSchema, BlogSummarySchema, BlogAuthorSchema

bp = Blueprint('blog', __name__, url_prefix='/blog')


@bp.route('/post/<post_id>')
def get_post_by_id(post_id):
    post = BlogPost.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found.'}), 404
    return jsonify(BlogPostSchema().dump(post))


@bp.route('/<slug>')
def get_post_by_slug(slug):
    post = BlogPost.query.filter_by(slug=slug).one_or_none()
    if not post:
        return jsonify({'error': 'Post not found.'}), 404
    return jsonify(BlogPostSchema().dump(post))


@bp.route('/save', methods=['POST'])
@admin_required
def save_post():
    post_dict = BlogPostSchema().load(request.json)
    if post_dict.get('id'):
        post = BlogPost.query.get(post_dict.get('id'))
        for k, v in post_dict.items():
            setattr(post, k, v)
    else:
        post = BlogPost(**post_dict)
        current_author = BlogAuthor.query.filter_by(user_id=current_user.id).one_or_none()
        if not current_author:
            current_author = BlogAuthor.query.get(1)
        post.author_id = current_author.id
    db.session.add(post)
    db.session.commit()
    return jsonify(BlogPostSchema().dump(post))


@bp.route('/summaries')
def get_summaries():
    post_query = BlogPost.query
    author_id = request.args.get('author')
    tags = request.args.get('tags')
    if author_id:
        post_query = post_query.filter_by(author_id=author_id)
    return jsonify(BlogSummarySchema(many=True).dump(post_query.order_by(BlogPost.posted.desc()).all()))


@bp.route('/author/<author_id>', methods=['GET'])
def author(author_id):
    author_object = BlogAuthor.query.get(author_id)
    if not author_object:
        return jsonify({'error': 'Author not found.'}), 404
    return jsonify(BlogAuthorSchema().dump(author_object))


@bp.route('/author/<author_id>/posts')
def author_posts(author_id):
    author_object = BlogAuthor.query.get(author_id)
    if not author_object:
        return jsonify({'error': 'Author not found.'}), 404
    return jsonify(BlogSummarySchema(many=True).dump(author_object.posts))


@bp.route('/author/save', methods=['POST'])
def save_author():
    author_dict = BlogAuthorSchema().load(request.json)
    user = User.query.get(author_dict.get('user_id'))
    if user.email != author_dict['public_email']:
        author_dict['email'] = author_dict['public_email']
    del author_dict['public_email']
    if author_dict.get('id'):
        author_object = BlogAuthor.query.get(author_dict.get('id'))
        for k, v in author_dict.items():
            setattr(author_object, k, v)
    else:
        author_object = BlogAuthor(**author_dict)
    db.session.add(author_object)
    db.session.commit()
    return jsonify(BlogAuthorSchema().dump(author))
