from django.urls import path

from . import views

app_name = "authors"

urlpatterns = [
    path("", views.author_list, name="list"),
    path("<str:username>/", views.author_detail, name="detail"),
]
