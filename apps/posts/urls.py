from django.urls import path

from . import views

app_name = "posts"

urlpatterns = [
    path("", views.post_list, name="list"),
    path("search/", views.post_search, name="search"),
    path("bookmarks/", views.bookmarks, name="bookmarks"),
    path("tag/<slug:tag_slug>/", views.post_list, name="list_by_tag"),
    path("<slug:slug>/", views.post_detail, name="detail"),
    path("<slug:slug>/react/", views.toggle_post_reaction, name="react"),
    path("<slug:slug>/bookmark/", views.toggle_post_bookmark, name="bookmark"),
]
