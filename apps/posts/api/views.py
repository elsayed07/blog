from __future__ import annotations

from django.http import HttpRequest
from ninja import Query, Router
from ninja.pagination import paginate as ninja_paginate, PageNumberPagination

from apps.posts.selectors import get_post_by_slug, get_published_posts, search_posts

from .schemas import PostDetailOut, PostListOut, PostSearchOut

router = Router(tags=["posts"])


@router.get("/", response=list[PostListOut])
@ninja_paginate(PageNumberPagination, page_size=12)
def list_posts(request: HttpRequest, tag: str | None = None) -> object:
    qs = get_published_posts()
    if tag:
        from apps.posts.selectors import get_posts_by_tag
        qs = get_posts_by_tag(tag)
    return qs


@router.get("/search/", response=list[PostSearchOut])
def search(request: HttpRequest, q: str = Query(..., min_length=2)) -> object:
    return search_posts(q)[:20]


@router.get("/{slug}/", response=PostDetailOut)
def get_post(request: HttpRequest, slug: str) -> object:
    from django.shortcuts import get_object_or_404
    from apps.posts.models import Post
    return get_object_or_404(Post, slug=slug)
