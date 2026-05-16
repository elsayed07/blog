import pytest
from django.urls import reverse

from apps.posts.models import PostStatus
from apps.posts.selectors import get_post_by_slug, get_related_posts, search_posts
from apps.posts.services import publish_post, toggle_bookmark, toggle_reaction
from tests.factories import PostFactory, UserFactory


@pytest.mark.django_db
class TestPostModel:
    def test_slug_generated_from_title(self):
        post = PostFactory(title="Hello World Test Post", slug="")
        assert post.slug == "hello-world-test-post"

    def test_slug_unique_collision(self):
        PostFactory(title="Duplicate Title", slug="duplicate-title")
        post = PostFactory(title="Duplicate Title", slug="")
        assert post.slug == "duplicate-title-1"

    def test_reading_time_estimated(self):
        body = " ".join(["word"] * 400)
        post = PostFactory(body=body)
        assert post.reading_time == 2

    def test_body_html_rendered_from_markdown(self):
        post = PostFactory(body="**bold** text")
        assert "<strong>bold</strong>" in post.body_html

    def test_published_at_set_on_publish(self):
        post = PostFactory(status=PostStatus.DRAFT, published_at=None)
        published = publish_post(post)
        assert published.published_at is not None
        assert published.status == PostStatus.PUBLISHED


@pytest.mark.django_db
class TestPostSelectors:
    def test_get_post_by_slug(self):
        post = PostFactory(published=True)
        found = get_post_by_slug(post.slug)
        assert found.pk == post.pk

    def test_search_returns_matching_posts(self):
        PostFactory(title="Django for Professionals", published=True)
        PostFactory(title="Unrelated Post", published=True)
        results = list(search_posts("Django"))
        assert any("Django" in p.title for p in results)

    def test_related_posts_by_shared_tags(self):
        from taggit.models import Tag
        post1 = PostFactory(published=True)
        post2 = PostFactory(published=True)
        post1.tags.add("python", "django")
        post2.tags.add("python", "django")
        related = list(get_related_posts(post1))
        assert post2 in related


@pytest.mark.django_db
class TestPostServices:
    def test_toggle_reaction_adds_and_removes(self):
        user = UserFactory()
        post = PostFactory(published=True)
        added = toggle_reaction(post, user, "like")
        assert added is True
        removed = toggle_reaction(post, user, "like")
        assert removed is False

    def test_toggle_bookmark(self):
        user = UserFactory()
        post = PostFactory(published=True)
        bookmarked = toggle_bookmark(post, user)
        assert bookmarked is True
        removed = toggle_bookmark(post, user)
        assert removed is False


@pytest.mark.django_db
class TestPostViews:
    def test_post_list_returns_200(self, client, published_post):
        url = reverse("posts:list")
        response = client.get(url)
        assert response.status_code == 200

    def test_post_detail_returns_200(self, client, published_post):
        url = reverse("posts:detail", kwargs={"slug": published_post.slug})
        response = client.get(url)
        assert response.status_code == 200

    def test_post_detail_404_for_draft(self, client, draft_post):
        url = reverse("posts:detail", kwargs={"slug": draft_post.slug})
        response = client.get(url)
        assert response.status_code == 404

    def test_search_returns_results(self, client, published_post):
        url = reverse("posts:search") + f"?q={published_post.title[:10]}"
        response = client.get(url)
        assert response.status_code == 200

    def test_bookmark_requires_auth(self, client, published_post):
        url = reverse("posts:bookmark", kwargs={"slug": published_post.slug})
        response = client.post(url)
        assert response.status_code == 302

    def test_react_requires_auth(self, client, published_post):
        url = reverse("posts:react", kwargs={"slug": published_post.slug})
        response = client.post(url, {"reaction": "like"})
        assert response.status_code == 302
