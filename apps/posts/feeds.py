from __future__ import annotations

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed

from .selectors import get_published_posts


class LatestPostsFeed(Feed):
    title = "Blog — Latest Posts"
    link = "/posts/"
    description = "The latest posts from our blog."

    def items(self) -> object:
        return get_published_posts()[:20]

    def item_title(self, item: object) -> str:
        return item.title

    def item_description(self, item: object) -> str:
        return item.excerpt or item.body[:300]

    def item_pubdate(self, item: object) -> object:
        return item.published_at


class LatestPostsAtomFeed(LatestPostsFeed):
    feed_type = Atom1Feed
    subtitle = LatestPostsFeed.description
