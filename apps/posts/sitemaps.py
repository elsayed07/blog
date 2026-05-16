from __future__ import annotations

from django.contrib.sitemaps import Sitemap

from .models import Post


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self) -> object:
        return Post.objects.order_by("-published_at")

    def lastmod(self, obj: Post) -> object:
        return obj.updated_at

    def location(self, obj: Post) -> str:
        return obj.get_absolute_url()
