# !/usr/bin/env python
# encoding: utf-8

from ..extensions import ma
from ..models import BlogTag, BlogPost, BlogAuthor
from marshmallow import INCLUDE, EXCLUDE


class BlogAuthorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BlogAuthor
        unknown = EXCLUDE
        dump_only = ['gravatar', 'pronouns', 'posts', 'name']
        include_fk = True

    name = ma.String()
    pronouns = ma.String()
    email = ma.String(attribute='public_email')
    gravatar = ma.String()
    posts = ma.List(ma.HyperlinkRelated('blog.get_post_by_id', url_key='post_id'))


class BlogTagSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BlogTag


class BlogPostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BlogPost
        unknown = INCLUDE

    tags = ma.List(ma.Nested(BlogTagSchema))
    author = ma.Nested(BlogAuthorSchema)


class BlogSummarySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BlogPost
        exclude = ['body']

    tags = ma.List(ma.Nested(BlogTagSchema))
    author = ma.Nested(BlogAuthorSchema, only=['id', 'name', 'gravatar'])
