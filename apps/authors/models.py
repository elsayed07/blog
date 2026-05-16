from __future__ import annotations

from django.conf import settings
from django.db import models
from django.urls import reverse

from shared.models import BaseModel


class AuthorProfile(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="author_profile",
    )
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="authors/avatars/%Y/%m/", blank=True, null=True)
    website = models.URLField(blank=True)
    twitter_handle = models.CharField(max_length=50, blank=True)
    github_handle = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=100, blank=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        db_table = "author_profiles"
        verbose_name = "author profile"

    def __str__(self) -> str:
        return f"{self.user.name} profile"

    def get_absolute_url(self) -> str:
        return reverse("authors:detail", kwargs={"username": self.user.username})
