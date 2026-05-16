from __future__ import annotations

from django.conf import settings
from django.db import models

from shared.models import BaseModel, SoftDeleteModel


class CommentStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    APPROVED = "approved", "Approved"
    REJECTED = "rejected", "Rejected"
    SPAM = "spam", "Spam"


class Comment(BaseModel, SoftDeleteModel):
    post = models.ForeignKey(
        "posts.Post",
        on_delete=models.CASCADE,
        related_name="comments",
        db_index=True,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="comments",
    )
    guest_name = models.CharField(max_length=100, blank=True)
    guest_email = models.EmailField(blank=True)
    body = models.TextField(max_length=2000)
    status = models.CharField(
        max_length=20,
        choices=CommentStatus.choices,
        default=CommentStatus.PENDING,
        db_index=True,
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies",
    )
    is_pinned = models.BooleanField(default=False)

    class Meta:
        db_table = "comments"
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["post", "status"]),
            models.Index(fields=["author", "status"]),
        ]

    def __str__(self) -> str:
        name = self.author.name if self.author else self.guest_name
        return f"Comment by {name} on {self.post_id}"

    @property
    def display_name(self) -> str:
        if self.author:
            return self.author.name
        return self.guest_name or "Anonymous"

    @property
    def is_reply(self) -> bool:
        return self.parent_id is not None
