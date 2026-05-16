from django.contrib import admin

from .models import Comment, CommentStatus
from .services import approve_comment, mark_spam, reject_comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("display_name", "post", "status", "is_pinned", "created_at")
    list_filter = ("status", "is_pinned")
    search_fields = ("author__email", "guest_name", "guest_email", "body")
    raw_id_fields = ("post", "author", "parent")
    readonly_fields = ("id", "created_at", "updated_at")
    actions = ["approve_selected", "reject_selected", "mark_spam_selected"]

    @admin.action(description="Approve selected comments")
    def approve_selected(self, request: object, queryset: object) -> None:
        for c in queryset.filter(status=CommentStatus.PENDING):
            approve_comment(c)

    @admin.action(description="Reject selected comments")
    def reject_selected(self, request: object, queryset: object) -> None:
        for c in queryset:
            reject_comment(c)

    @admin.action(description="Mark selected as spam")
    def mark_spam_selected(self, request: object, queryset: object) -> None:
        for c in queryset:
            mark_spam(c)
