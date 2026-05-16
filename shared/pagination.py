from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import QuerySet
from django.http import HttpRequest


@dataclass
class PaginatedResult:
    items: Any
    page: int
    total_pages: int
    total_count: int
    has_next: bool
    has_previous: bool
    next_page: int | None
    previous_page: int | None


def paginate(
    queryset: QuerySet,
    request: HttpRequest,
    per_page: int = 12,
    page_param: str = "page",
) -> PaginatedResult:
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get(page_param, 1)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return PaginatedResult(
        items=page_obj,
        page=page_obj.number,
        total_pages=paginator.num_pages,
        total_count=paginator.count,
        has_next=page_obj.has_next(),
        has_previous=page_obj.has_previous(),
        next_page=page_obj.next_page_number() if page_obj.has_next() else None,
        previous_page=page_obj.previous_page_number() if page_obj.has_previous() else None,
    )
