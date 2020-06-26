from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
#from post.feeds import LastEntriesFeed
from django.contrib.sitemaps.views import sitemap
#from post.sitemaps import PostSitemap

#sitemaps = {
#    'post': PostSitemap,
#}

urlpatterns = [
    #path("admin/", admin.site.urls),
    #path("accounts/", include("accounts.urls", namespace="accounts")),
    #path("contact/", include("contact.urls", namespace="contact")),
    #path("latest/feed/", LastEntriesFeed(), name="feed"),
    #path("api/", include("post.api.urls")),  # REST api
    #path("", include("post.urls")),
    #path("markdownx/", include("markdownx.urls")),
    #path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
    #     name='django.contrib.sitemaps.views.sitemap')
]

# to load static/media files in development environment
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] \
            + urlpatterns
