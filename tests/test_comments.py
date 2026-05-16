import pytest

from apps.comments.models import CommentStatus
from apps.comments.services import approve_comment, create_comment, mark_spam
from tests.factories import CommentFactory, PostFactory, UserFactory


@pytest.mark.django_db
class TestCommentService:
    def test_authenticated_user_comment_auto_approved(self):
        user = UserFactory()
        post = PostFactory(published=True)
        comment = create_comment(post, "Great post!", author=user)
        assert comment.status == CommentStatus.APPROVED
        assert comment.author == user

    def test_guest_comment_pending_moderation(self):
        post = PostFactory(published=True)
        comment = create_comment(post, "Nice!", guest_name="Alice", guest_email="alice@example.com")
        assert comment.status == CommentStatus.PENDING
        assert comment.guest_name == "Alice"

    def test_comment_requires_author_or_guest_name(self):
        post = PostFactory(published=True)
        with pytest.raises(ValueError, match="author or guest_name"):
            create_comment(post, "Body without author")

    def test_comment_blocked_when_comments_disabled(self):
        post = PostFactory(published=True, allow_comments=False)
        with pytest.raises(ValueError, match="disabled"):
            create_comment(post, "Should fail", guest_name="Bob")

    def test_approve_comment(self):
        comment = CommentFactory(status=CommentStatus.PENDING)
        approved = approve_comment(comment)
        assert approved.status == CommentStatus.APPROVED

    def test_mark_spam(self):
        comment = CommentFactory()
        spammed = mark_spam(comment)
        assert spammed.status == CommentStatus.SPAM
