from __future__ import annotations

import structlog
from django.db import transaction

from apps.posts.models import Post

from .models import Comment, CommentStatus

logger = structlog.get_logger(__name__)


@transaction.atomic
def create_comment(
    post: Post,
    body: str,
    author: object = None,
    guest_name: str = "",
    guest_email: str = "",
    parent: Comment | None = None,
) -> Comment:
    if not author and not guest_name:
        raise ValueError("Either author or guest_name is required")
    if not post.allow_comments:
        raise ValueError("Comments are disabled for this post")

    status = CommentStatus.APPROVED if author else CommentStatus.PENDING

    comment = Comment.objects.create(
        post=post,
        author=author,
        guest_name=guest_name,
        guest_email=guest_email,
        body=body,
        status=status,
        parent=parent,
    )
    logger.info("comment.created", comment_id=str(comment.id), post_id=str(post.id))
    return comment


def approve_comment(comment: Comment) -> Comment:
    comment.status = CommentStatus.APPROVED
    comment.save(update_fields=["status", "updated_at"])
    return comment


def reject_comment(comment: Comment) -> Comment:
    comment.status = CommentStatus.REJECTED
    comment.save(update_fields=["status", "updated_at"])
    return comment


def mark_spam(comment: Comment) -> Comment:
    comment.status = CommentStatus.SPAM
    comment.save(update_fields=["status", "updated_at"])
    return comment
