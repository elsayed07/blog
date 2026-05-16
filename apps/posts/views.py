from __future__ import annotations

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from taggit.models import Tag

from shared.pagination import paginate

from .models import Post, PostReaction
from .selectors import (
    get_featured_posts,
    get_post_by_slug,
    get_posts_by_tag,
    get_published_posts,
    get_related_posts,
    get_trending_posts,
    get_user_bookmarks,
    search_posts,
)
from .services import record_view, toggle_bookmark, toggle_reaction


def post_list(request: HttpRequest, tag_slug: str | None = None) -> HttpResponse:
    queryset = get_published_posts()
    active_tag = None
    if tag_slug:
        active_tag = get_object_or_404(Tag, slug=tag_slug)
        queryset = get_posts_by_tag(tag_slug)

    result = paginate(queryset, request, per_page=12)
    featured = get_featured_posts(limit=3) if not tag_slug else []
    trending = get_trending_posts(limit=5)

    return render(request, "posts/list.html", {
        "result": result,
        "active_tag": active_tag,
        "featured": featured,
        "trending": trending,
    })


def post_detail(request: HttpRequest, slug: str) -> HttpResponse:
    post = get_object_or_404(
        Post.objects.select_related("author", "author__author_profile").prefetch_related("tags"),
        slug=slug,
    )
    related = get_related_posts(post)

    user_reactions: set[str] = set()
    is_bookmarked = False
    if request.user.is_authenticated:
        user_reactions = set(
            PostReaction.objects.filter(post=post, user=request.user).values_list("reaction", flat=True)
        )
        is_bookmarked = post.bookmarks.filter(user=request.user).exists()

    reaction_counts = {
        r: post.reactions.filter(reaction=r).count()
        for r in ("like", "love", "insightful")
    }

    record_view(post, request.META.get("REMOTE_ADDR", ""))

    return render(request, "posts/detail.html", {
        "post": post,
        "related": related,
        "user_reactions": user_reactions,
        "is_bookmarked": is_bookmarked,
        "reaction_counts": reaction_counts,
    })


def post_search(request: HttpRequest) -> HttpResponse:
    query = request.GET.get("q", "").strip()
    results = search_posts(query) if query else []
    result = paginate(results, request) if query else None

    if request.headers.get("HX-Request"):
        return render(request, "posts/partials/search_results.html", {
            "query": query,
            "result": result,
        })

    return render(request, "posts/search.html", {"query": query, "result": result})


@login_required
@require_POST
def toggle_post_reaction(request: HttpRequest, slug: str) -> JsonResponse:
    post = get_object_or_404(Post, slug=slug)
    reaction = request.POST.get("reaction", "like")
    if reaction not in ("like", "love", "insightful"):
        return JsonResponse({"error": "Invalid reaction"}, status=400)

    added = toggle_reaction(post, request.user, reaction)
    count = post.reactions.filter(reaction=reaction).count()
    return JsonResponse({"added": added, "count": count, "reaction": reaction})


@login_required
@require_POST
def toggle_post_bookmark(request: HttpRequest, slug: str) -> JsonResponse:
    post = get_object_or_404(Post, slug=slug)
    bookmarked = toggle_bookmark(post, request.user)
    return JsonResponse({"bookmarked": bookmarked})


@login_required
def bookmarks(request: HttpRequest) -> HttpResponse:
    result = paginate(get_user_bookmarks(request.user.id), request, per_page=12)
    return render(request, "posts/bookmarks.html", {"result": result})
