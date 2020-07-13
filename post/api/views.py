from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import F
from .permissions import IsOwnerOrReadOnly
from post.models import Post
from .serializers import *
from .pagination import *

"""
class PostViewSet(viewsets.ModelViewSet):
    #
    #This viewset automatically provides `list`, `create`, `retrieve`,
    #`update` and `destroy` actions.
    #

    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    lookup_field = "slug"

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["category__name", "author__username", "title", "content"]

    # pagination_class = PostPageNumberPagination # works fine

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PostDetailSerializer
        elif self.action == "create" or self.action == "update":
            return PostCreateUpdateSerializer
        else:
            return PostListSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)
"""

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    serializer_class = PostCreateSerializer
    name = 'post-list'
    filter_fields = (
        'title',
        )
    search_fields = (
        '^title',
        )
    ordering_fields = (
        'title',
        )

    def list(self, request):
        #super.(PostList, self).list()
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        context={'request': request}
        serializer = PostListSerializer(queryset, many=True, context=context)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'
    name = 'post-detail'
    filter_fields = (
        'title',
        )
    search_fields = (
        '^title',
        )
    ordering_fields = (
        'title',
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        Post.objects.filter(pk=instance.id).update(views_count=F('views_count') + 1)
        instance.refresh_from_db()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

"""
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["username"]

    pagination_class = UserPageNumberPagination
"""