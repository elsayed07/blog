from django.contrib import admin

from .models import AuthorProfile


@admin.register(AuthorProfile)
class AuthorProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "location", "is_verified", "created_at")
    list_filter = ("is_verified",)
    search_fields = ("user__email", "user__username", "location")
    raw_id_fields = ("user",)
