from django.urls import path, include
#from rest_framework.routers import DefaultRouter
from posts.api import Views

# Create a router and register viewsets with it.
#router = DefaultRouter()
#router.register(r"posts", PostViewSet)
#router.register(r"users", UserViewSet)

# The API URLs are now determined automatically by the router.
#urlpatterns = [path("", include(router.urls))]
urlpatterns = [
    path('post-list/',
        views.PostList.as_view(),
        name=views.PostList.name
    ),
    path('post-detail/<int:pk>/',
        views.PostDetail.as_view(),
        name=views.PostDetail.name
    ),
]