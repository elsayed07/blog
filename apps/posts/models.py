from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from taggit.managers import TaggableManager
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase

from shared.models import BaseModel, SoftDeleteManager, SoftDeleteModel
from shared.utils import estimate_reading_time, render_markdown

if TYPE_CHECKING:
    pass


class UUIDTaggedItem(GenericUUIDTaggedItemBase, TaggedItemBase):
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"


class PostStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    PUBLISHED = "published", "Published"
    SCHEDULED = "scheduled", "Scheduled"
    ARCHIVED = "archived", "Archived"


class Reaction(models.TextChoices):
    LIKE = "like", "Like"
    LOVE = "love", "Love"
    INSIGHTFUL = "insightful", "Insightful"
    BOOKMARK = "bookmark", "Bookmark"


class PublishedPostManager(SoftDeleteManager):
    def get_queryset(self) -> models.QuerySet[Post]:
        return (
            super()
            .get_queryset()
            .filter(status=PostStatus.PUBLISHED, published_at__lte=timezone.now())
            .select_related("author", "author__author_profile")
            .prefetch_related("tags")
        )


class Post(BaseModel, SoftDeleteModel):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="posts",
        db_index=True,
    )
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True, db_index=True)
    excerpt = models.TextField(max_length=500, blank=True)
    body = models.TextField()
    body_html = models.TextField(blank=True, editable=False)
    cover_image = models.ImageField(upload_to="posts/covers/%Y/%m/", blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=PostStatus.choices,
        default=PostStatus.DRAFT,
        db_index=True,
    )
    published_at = models.DateTimeField(null=True, blank=True, db_index=True)
    reading_time = models.PositiveSmallIntegerField(default=1, editable=False)
    view_count = models.PositiveIntegerField(default=0)
    og_title = models.CharField(max_length=300, blank=True)
    og_description = models.TextField(max_length=160, blank=True)
    og_image = models.ImageField(upload_to="posts/og/%Y/%m/", blank=True, null=True)
    is_featured = models.BooleanField(default=False, db_index=True)
    allow_comments = models.BooleanField(default=True)
    search_vector = SearchVectorField(null=True, blank=True)

    objects = PublishedPostManager()
    all_objects = models.Manager()
    tags = TaggableManager(through=UUIDTaggedItem, blank=True)

    class Meta:
        db_table = "posts"
        ordering = ["-published_at"]
        indexes = [
            models.Index(fields=["status", "published_at"]),
            models.Index(fields=["author", "status"]),
            models.Index(fields=["-published_at", "status"]),
            GinIndex(fields=["search_vector"], name="post_search_vector_idx"),
        ]

    def __str__(self) -> str:
        return self.title

    def save(self, *args: object, **kwargs: object) -> None:
        if not self.slug:
            base = slugify(self.title)
            slug = base
            n = 1
            while Post.all_objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        self.body_html = render_markdown(self.body)
        self.reading_time = estimate_reading_time(self.body)
        if self.status == PostStatus.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("posts:detail", kwargs={"slug": self.slug})

    @property
    def effective_og_title(self) -> str:
        return self.og_title or self.title

    @property
    def effective_og_description(self) -> str:
        return self.og_description or self.excerpt


class PostAnalytics(BaseModel):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name="analytics")
    unique_views = models.PositiveIntegerField(default=0)
    total_shares = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "post_analytics"


class PostReaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="reactions")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="post_reactions",
    )
    reaction = models.CharField(max_length=20, choices=Reaction.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "post_reactions"
        unique_together = ("post", "user", "reaction")
        indexes = [models.Index(fields=["post", "reaction"])]


class Bookmark(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookmarks",
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="bookmarks")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "post_bookmarks"
        unique_together = ("user", "post")
        ordering = ["-created_at"]
