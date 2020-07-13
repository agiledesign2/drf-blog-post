from django.urls import path, include
#from rest_framework.routers import DefaultRouter
from post.api import views

# Create a router and register viewsets with it.
#router = DefaultRouter()
#router.register(r"posts", PostViewSet)
#router.register(r"users", UserViewSet)

# The API URLs are now determined automatically by the router.
#urlpatterns = [path("", include(router.urls))]
app_name = 'post'

urlpatterns = [
    path('post/',
        views.Post.as_view(),
        name=views.Post.name
    ),
    path('post-detail/<str:slug>/',
        views.PostDetail.as_view(),
        name=views.PostDetail.name
    ),
]