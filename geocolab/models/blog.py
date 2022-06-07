# !/usr/bin/env python
# encoding: utf-8

from ..extensions import db
from sqlalchemy.orm import backref
from sqlalchemy import func
from .utils import gravatar


class BlogAuthor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    twitter = db.Column(db.String(50))
    github = db.Column(db.String(50))
    links = db.Column(db.JSON)
    email = db.Column(db.String(100))
    bio = db.Column(db.String())

    user = db.relationship('User', backref=backref('author', uselist=False))
    posts = db.relationship('BlogPost', backref='author')

    @property
    def public_email(self):
        if not self.email or self.email == '':
            return self.user.email
        return self.email

    @property
    def gravatar(self):
        return gravatar(self.public_email)

    @property
    def name(self):
        return self.user.name

    @property
    def pronouns(self):
        return self.user.pronouns


post_tags = db.Table('post_tags',
                     db.Model.metadata,
                     db.Column('tag_id', db.ForeignKey('blog_tag.id')),
                     db.Column('post_id', db.ForeignKey('blog_post.id')))


class BlogTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    posts = db.relationship('BlogPost', secondary=post_tags, back_populates='tags')


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(50), unique=True)
    title = db.Column(db.String(200))
    summary = db.Column(db.String())
    body = db.Column(db.String())
    posted = db.Column(db.DateTime, server_default=func.now())

    author_id = db.Column(db.Integer, db.ForeignKey('blog_author.id'), nullable=False)

    tags = db.relationship('BlogTag', secondary=post_tags, back_populates='posts')
