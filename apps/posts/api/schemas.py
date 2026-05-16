from __future__ import annotations

import uuid
from datetime import datetime

from ninja import Schema


class AuthorOut(Schema):
    username: str
    display_name: str


class PostListOut(Schema):
    id: uuid.UUID
    title: str
    slug: str
    excerpt: str
    author: AuthorOut
    published_at: datetime | None
    reading_time: int
    view_count: int
    tags: list[str]

    @staticmethod
    def resolve_tags(obj: object) -> list[str]:
        return [t.name for t in obj.tags.all()]

    @staticmethod
    def resolve_author(obj: object) -> dict:
        return {"username": obj.author.username, "display_name": obj.author.name}


class PostDetailOut(PostListOut):
    body_html: str
    allow_comments: bool
    og_title: str
    og_description: str


class PostSearchOut(Schema):
    id: uuid.UUID
    title: str
    slug: str
    excerpt: str
    published_at: datetime | None


class PaginatedPostsOut(Schema):
    count: int
    total_pages: int
    page: int
    results: list[PostListOut]
