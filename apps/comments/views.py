from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from apps.posts.models import Post

from .forms import CommentForm
from .models import Comment
from .services import create_comment


@require_POST
def post_comment(request: HttpRequest, slug: str) -> HttpResponse:
    post = get_object_or_404(Post, slug=slug)
    form = CommentForm(request.POST)
    comment = None
    errors = None

    if form.is_valid():
        data = form.cleaned_data
        parent = None
        if data.get("parent_id"):
            parent = Comment.objects.filter(pk=data["parent_id"], post=post).first()

        comment = create_comment(
            post=post,
            body=data["body"],
            author=request.user if request.user.is_authenticated else None,
            guest_name=data.get("guest_name", ""),
            guest_email=data.get("guest_email", ""),
            parent=parent,
        )
    else:
        errors = form.errors

    if request.headers.get("HX-Request"):
        return render(request, "comments/partials/comment.html", {
            "comment": comment,
            "errors": errors,
            "post": post,
        })

    return render(request, "comments/partials/comment.html", {
        "comment": comment,
        "errors": errors,
        "post": post,
    })
