from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
#from post.feeds import LastEntriesFeed
#from django.contrib.sitemaps.views import sitemap
#from post.sitemaps import PostSitemap

#sitemaps = {
#    'post': PostSitemap,
#}

urlpatterns = [
    path("admin/", admin.site.urls),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    #path("latest/feed/", LastEntriesFeed(), name="feed"),
    path("api/v1/", include("post.api.urls")),  # REST api
    path("markdownx/", include("markdownx.urls")),
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
