# !/usr/bin/env python
# encoding: utf-8

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, current_user

from ..extensions import db
from ..models import BlogPost, BlogAuthor
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


@bp.route('/summaries')
def get_summaries():
    post_query = BlogPost.query
    author_id = request.args.get('author')
    tags = request.args.get('tags')
    if author_id:
        post_query = post_query.filter_by(author_id=author_id)
    return jsonify(BlogSummarySchema(many=True).dump(post_query.order_by(BlogPost.posted.desc()).all()))


@bp.route('/author/<author_id>')
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
