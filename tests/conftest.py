import pytest
from django.test import Client

from tests.factories import PostFactory, UserFactory


@pytest.fixture
def client() -> Client:
    return Client()


@pytest.fixture
def user(db):
    return UserFactory()


@pytest.fixture
def author(db):
    return UserFactory(is_staff=False)


@pytest.fixture
def staff_user(db):
    return UserFactory(is_staff=True)


@pytest.fixture
def published_post(db, author):
    return PostFactory(author=author, status="published")


@pytest.fixture
def draft_post(db, author):
    return PostFactory(author=author, status="draft")


@pytest.fixture
def auth_client(client, user):
    client.force_login(user)
    return client
