from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from apps.posts.selectors import get_posts_by_author
from shared.pagination import paginate

from .selectors import get_all_authors, get_author_profile


def author_detail(request: HttpRequest, username: str) -> HttpResponse:
    profile = get_author_profile(username)
    result = paginate(get_posts_by_author(username), request, per_page=10)
    return render(request, "authors/detail.html", {"profile": profile, "result": result})


def author_list(request: HttpRequest) -> HttpResponse:
    authors = get_all_authors()
    return render(request, "authors/list.html", {"authors": authors})
