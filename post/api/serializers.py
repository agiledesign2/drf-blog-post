from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from rest_framework import serializers
from django.utils.crypto import get_random_string
from rest_framework.fields import CurrentUserDefault
from post.models import Post, Category
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)


# model listings
class CategoryListingField(serializers.RelatedField):
    def to_representation(self, value):
        return f"{value.name}"

    def to_internal_value(self, value):
        obj = Category.objects.filter(name=value)
        if obj and (len(obj)) == 1:
            return obj.get().id
        else:
            raise ValidationError(f"Category with name {value} does not exist")


class AuthorListingField(serializers.RelatedField):
    def to_representation(self, value):
        return f"{value.username.capitalize()}"

    def to_internal_value(self, value):
        return value


# model serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name",)


class PostListSerializer(TaggitSerializer, serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="post:post-detail", lookup_field="slug"
    )
    author = AuthorListingField(queryset=User.objects.all())
    category = CategoryListingField(queryset=Category.objects.all(), many=True)
    published = serializers.DateTimeField(format="%a, %d %b  %I:%M %p")
    tags = TagListSerializerField()

    class Meta:
        model = Post
        fields = [
            "url",
            "title",
            "category",
            "content",
            "description",
            "cover",
            "published",
            "allow_comments",
            "author",
            "status",
            "views_count",
            "tags",
        ]
        #read_only_fields = ["views_count"]


class PostCreateSerializer(TaggitSerializer, serializers.ModelSerializer):
    #author = AuthorListingField(queryset=User.objects.all())
    category = CategoryListingField(queryset=Category.objects.all(), many=True)
    #published = serializers.DateTimeField(format="%a, %d %b  %I:%M %p")
    tags = TagListSerializerField()

    class Meta:
        model = Post
        fields = [
            "title",
            "category",
            "content",
            "description",
            "cover",
            "allow_comments",
            "status",
            "tags",
        ]
        #read_only_fields = ["published"]

    def create(self, validated_data):
        title = validated_data.get("title", "")
        slug = slugify(title)
        # check if there exists a post with existing slug
        q = Post.objects.filter(slug=slug)
        if q.exists():
            slug = "-".join([slug, get_random_string(4, "0123456789")])

        validated_data["slug"] = slug

        if validated_data.get("status", "") in [Post.STATUS_PUBLISHED]:
            validated_data["published"] = timezone.now()
        else:
            validated_data["updated"] = timezone.now()
        # pops out the list of categories
        #categories = validated_data.pop("category")
        # and saves the rest of the data
        #post = Post.objects.create(**validated_data)
        # add categories separately
        #for category in categories:
        #    post.category.add(category)
        #return post
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        slug = slugify(instance.title)
        # check if there exists a post with existing slug
        if instance.slug not in slug:
            q = Post.objects.filter(slug=slug)
            if q.exists():
                slug = "-".join([slug, get_random_string(4, "0123456789")])
        
        instance.slug = slug
        
        if validated_data.get("status", "") in [Post.STATUS_PUBLISHED]:
            instance.published = timezone.now()
        else:
            instance.updated = timezone.now()

        #categories = validated_data.get("category")
        # deassociate existing categories from instance
        #instance.category.clear()
        #for category in categories:
        #    instance.category.add(category)

        #instance.author = self.context.get("request").user
        #instance.content = validated_data.get("content", instance.content)
        #instance.save()
        return super(PostCreateSerializer, self).update(instance, validated_data)


class PostDetailSerializer(TaggitSerializer, serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="post:post-detail", lookup_field="slug"
    )
    author = AuthorListingField(queryset=User.objects.all())
    category = CategoryListingField(queryset=Category.objects.all(), many=True)
    published = serializers.DateTimeField(format="%a, %d %b  %I:%M %p", read_only=True)
    tags = TagListSerializerField()

    class Meta:
        model = Post
        fields = (
            "url",
            "title",
            "category",
            "content",
            "description",
            "cover",
            "published",
            "allow_comments",
            "author",
            "status",
            "views_count",
            "tags",
        )

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        slug = slugify(instance.title)
        # check if there exists a post with existing slug
        q = Post.objects.filter(slug=slug)
        if q.exists():
            slug = "-".join([slug, get_random_string(4, "0123456789")])
        
        instance.slug = slug

        if validated_data.get("status", "") in [Post.STATUS_PUBLISHED]:
            instance.published = timezone.now()
        else:
            instance.updated = timezone.now()

        categories = validated_data.get("category")
        # deassociate existing categories from instance
        instance.category.clear()
        for category in categories:
            instance.category.add(category)

        instance.author = self.context.get("request").user
        instance.content = validated_data.get("content", instance.content)
        instance.save()
        return instance