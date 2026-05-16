from django.contrib import admin
from django.utils.html import format_html

from .models import Bookmark, Post, PostAnalytics, PostReaction, PostStatus
from .services import archive_post, publish_post


class PostAnalyticsInline(admin.StackedInline):
    model = PostAnalytics
    readonly_fields = ("unique_views", "total_shares")
    can_delete = False


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title", "author", "status", "is_featured", "published_at",
        "view_count", "reading_time", "created_at",
    )
    list_filter = ("status", "is_featured", "allow_comments", "tags")
    search_fields = ("title", "slug", "author__email", "author__username")
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ("author",)
    readonly_fields = ("id", "body_html", "reading_time", "view_count", "created_at", "updated_at")
    date_hierarchy = "published_at"
    ordering = ("-published_at",)
    actions = ["publish_selected", "archive_selected"]
    inlines = [PostAnalyticsInline]

    fieldsets = (
        (None, {"fields": ("id", "author", "title", "slug", "status", "is_featured")}),
        ("Content", {"fields": ("excerpt", "body", "body_html", "cover_image")}),
        ("Publishing", {"fields": ("published_at", "allow_comments", "reading_time")}),
        ("SEO / OpenGraph", {"fields": ("og_title", "og_description", "og_image"), "classes": ("collapse",)}),
        ("Meta", {"fields": ("view_count", "created_at", "updated_at", "deleted_at"), "classes": ("collapse",)}),
    )

    @admin.action(description="Publish selected posts")
    def publish_selected(self, request: object, queryset: object) -> None:
        for post in queryset.filter(status__in=[PostStatus.DRAFT, PostStatus.SCHEDULED]):
            publish_post(post)

    @admin.action(description="Archive selected posts")
    def archive_selected(self, request: object, queryset: object) -> None:
        for post in queryset.filter(status=PostStatus.PUBLISHED):
            archive_post(post)

    def cover_preview(self, obj: Post) -> str:
        if obj.cover_image:
            return format_html('<img src="{}" height="50" />', obj.cover_image.url)
        return "-"
    cover_preview.short_description = "Cover"


@admin.register(PostReaction)
class PostReactionAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "reaction", "created_at")
    list_filter = ("reaction",)
    raw_id_fields = ("post", "user")


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "created_at")
    raw_id_fields = ("user", "post")
