from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from ninja import NinjaAPI

from apps.posts.api.views import router as posts_router
from apps.posts.feeds import LatestPostsAtomFeed, LatestPostsFeed
from apps.posts.sitemaps import PostSitemap

api = NinjaAPI(title="Blog API", version="1.0", urls_namespace="api")
api.add_router("/posts/", posts_router)

sitemaps = {"posts": PostSitemap}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", api.urls),
    path("posts/", include("apps.posts.urls", namespace="posts")),
    path("comments/", include("apps.comments.urls", namespace="comments")),
    path("authors/", include("apps.authors.urls", namespace="authors")),
    path("feed/rss/", LatestPostsFeed(), name="rss_feed"),
    path("feed/atom/", LatestPostsAtomFeed(), name="atom_feed"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path("", include("apps.posts.urls")),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
