from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Post, Category
from taggit.models import Tag

from .forms import AddPostForm
#from .validator import group_required

# complex lookups (for searching)
from django.db.models import Q

from django.urls import reverse_lazy

# class based views
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView

from django.views import View
from django.utils.decorators import method_decorator

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView

from django.views.generic.dates import YearArchiveView, MonthArchiveView, DayArchiveView

from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
    PermissionRequiredMixin,
)

from django.db import transaction


class CategoryDatesMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        # get queryset of datetime objects for all published posts
        #context["dates"] = Post.objects.published().filter(tags__slug=self.kwargs['slug'])
        context["dates"] = Post.objects.published().datetimes(
            field_name="published", kind="month", order="DESC"
        )
        #context["dates"] = Post.objects.filter(status=Post.STATUS_PUBLISHED).datetimes(
        #    field_name="published", kind="month", order="DESC"
        #)
        context["recent_posts"] = Post.objects.published().order_by(
            "-published"
        )[:3]
        #context["recent_posts"] = Post.objects.filter(status=Post.STATUS_PUBLISHED).order_by(
        #    "-published"
        #)[:3]
        return context


class ListPosts(CategoryDatesMixin, ListView):
    model = Post
    template_name = "posts/index.html"
    context_object_name = "posts"
    ordering = ("-published",)
    paginate_by = 5

    def get_queryset(self):
        results = Post.objects.published()
        return results


class ListByAuthor(CategoryDatesMixin, ListView):
    model = Post
    context_object_name = "posts"
    template_name = "posts/post_by_author.html"
    paginate_by = 5
    ordering = ("-published",)

    def get_queryset(self):
        author = self.kwargs.get("author", None)
        results = []
        if author:
            results = Post.objects.published().filter(author__username=author)
        return results

    def get_context_data(self, **kwargs):
        """
        Pass author's name to the context
        """
        context = super().get_context_data(**kwargs)
        context["author"] = self.kwargs.get("author", None)
        return context


class ListByTag(CategoryDatesMixin, ListView):
    model = Post
    context_object_name = "posts"
    template_name = "posts/post_by_tag.html"
    paginate_by = 5
    ordering = ("-published",)

    def get_queryset(self):
        tag = self.kwargs.get("tag", None)
        results = []
        if tag:
            results = Post.objects.published().filter(tags__name=tag)
        return results

    def get_context_data(self, **kwargs):
        """
        Pass tag name to the context
        """
        context = super().get_context_data(**kwargs)
        context["tag"] = self.kwargs.get("tag", None)
        return context


class ListByCategory(CategoryDatesMixin, ListView):
    model = Post
    context_object_name = "posts"
    template_name = "posts/post_by_category.html"
    paginate_by = 5
    ordering = ("-published",)

    def get_queryset(self):
        category = self.kwargs.get("name", None)
        results = []
        if category:
            results = Post.objects.published().filter(category__name=category)
        return results

    def get_context_data(self, **kwargs):
        """
        Pass category's name to the context
        """
        context = super().get_context_data(**kwargs)
        context["category"] = self.kwargs.get("name", None)
        return context


class DetailsPost(CategoryDatesMixin, DetailView):
    model = Post
    template_name = "posts/post_detail.html"

    #def get_queryset(self, queryset=None):
        #item = super().get_object(self)
        #item.viewed()
        #return item

    def get(self, request, *args, **kwargs):
        res = super().get(request, *args, **kwargs)    
        self.object.viewed()
        return res


# Post archive views
class ArchiveMixin:
    model = Post
    date_field = "published"
    allow_future = False
    context_object_name = "posts"


class PostYearArchive(CategoryDatesMixin, ArchiveMixin, YearArchiveView):
    make_object_list = True


class PostYearMonthArchive(CategoryDatesMixin, ArchiveMixin, MonthArchiveView):
    pass


# Create, delete and update post views
# @group_required('Editors')
class AddPost(
    CategoryDatesMixin, PermissionRequiredMixin, LoginRequiredMixin, CreateView
):
    form_class = AddPostForm
    permission_required = "posts.add_post"
    template_name = "posts/post_form.html"

    # to process request.user in the form
    def form_valid(self, form):
        form.save(commit=False)
        form.instance.author = self.request.user

        if form.instance.status in [Post.STATUS_PUBLISHED]:
            form.instance.published = timezone.now()
        else:
            form.instance.updated = timezone.now()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        To use AddPostForm with 'Update' instead of 'Add' text in update view
        """
        context = super().get_context_data(**kwargs)
        context["update"] = False
        return context


class PostDraftsList(
    CategoryDatesMixin, PermissionRequiredMixin, LoginRequiredMixin, ListView
):
    template_name = "posts/list_drafts.html"
    permission_required = "posts.add_post"
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.draft().filter(
            author__username=self.request.user.username
        )


class DeletePost(
    CategoryDatesMixin, LoginRequiredMixin, UserPassesTestMixin, DeleteView
):
    model = Post
    success_url = reverse_lazy("posts:index")

    def test_func(self):
        """
        Only let the user delete object if they own the object being deleted
        """
        return self.get_object().author.username == self.request.user.username


class UpdatePost(
    CategoryDatesMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView
):
    model = Post
    form_class = AddPostForm

    def test_func(self):
        """
        Only let the user update object if they own the object being updated

        """
        return self.get_object().author.username == self.request.user.username

    def get_context_data(self, **kwargs):
        """
        To use AddPostForm with 'Update' instead of 'Add' text in update view
        """
        context = super().get_context_data(**kwargs)
        context["update"] = True
        return context


class SearchPosts(CategoryDatesMixin, ListView):
    context_object_name = "posts"
    template_name = "posts/post_search.html"
    paginate_by = 5
    ordering = ("-published",)

    def get_queryset(self):
        search_query = self.request.GET.get("q", None)
        results = []
        if search_query:
            results = Post.objects.filter(
                Q(category__name__icontains=search_query)
                | Q(author__username__icontains=search_query)
                | Q(title__icontains=search_query)
                | Q(content__icontains=search_query)
            ).distinct()
        return results
