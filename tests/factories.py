from __future__ import annotations

import factory
from django.utils import timezone
from factory.django import DjangoModelFactory

from apps.authors.models import AuthorProfile
from apps.comments.models import Comment, CommentStatus
from apps.posts.models import Post, PostStatus
from core.users.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    username = factory.Sequence(lambda n: f"user{n}")
    display_name = factory.Faker("name")
    is_active = True
    is_staff = False

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)


class AuthorProfileFactory(DjangoModelFactory):
    class Meta:
        model = AuthorProfile

    user = factory.SubFactory(UserFactory)
    bio = factory.Faker("paragraph")
    location = factory.Faker("city")
    is_verified = False


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post
        django_get_or_create = ("slug",)
        exclude = ("_tags",)

    author = factory.SubFactory(UserFactory)
    title = factory.Faker("sentence", nb_words=6)
    slug = factory.LazyAttribute(lambda o: __import__("django").utils.text.slugify(o.title)[:280])
    excerpt = factory.Faker("paragraph")
    body = factory.Faker("text", max_nb_chars=2000)
    status = PostStatus.DRAFT
    allow_comments = True

    class Params:
        published = factory.Trait(
            status=PostStatus.PUBLISHED,
            published_at=factory.LazyFunction(timezone.now),
        )


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment

    post = factory.SubFactory(PostFactory, published=True)
    author = factory.SubFactory(UserFactory)
    body = factory.Faker("paragraph")
    status = CommentStatus.APPROVED
