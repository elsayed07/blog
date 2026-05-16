from __future__ import annotations

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Post, PostAnalytics, PostStatus


@receiver(post_save, sender=Post)
def create_post_analytics(sender: type[Post], instance: Post, created: bool, **kwargs: object) -> None:
    if created:
        PostAnalytics.objects.get_or_create(post=instance)
