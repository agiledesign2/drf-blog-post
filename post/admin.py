from django.contrib import admin
from django.utils import timezone
from django.db import models
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from django.forms import TextInput, Textarea
from django.utils.safestring import mark_safe
#from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from .models import Category, Post

#@admin.register(Article)
class PostAdmin(admin.ModelAdmin):	#(ImportExportModelAdmin):
    list_display = (
        'title', 'author', 'content', 'description', 'allow_comments', 
        'tags', 'status', 'views_count', 'created', 'updated', 'published',
        'cover_admin' 
    )
    search_fields = ('title', 'author', 'description', 'content', 'published')
    list_filter = ('status', 'category', 'author', 'tags', 'published')
    list_editable = ('allow_comments',)
    date_hierarchy = 'published'
    readonly_fields = ['cover_admin']
    list_display_links = ["title","published"]
    raw_id_fields = ('author',)
    ordering = ('status', 'published')
    list_per_page = 15
    
    fieldsets = (
        ('Post', {
            'fields': ('title', 'category', 'cover_admin', 'cover', 'content', 'description', 'allow_comments', 'tags', 'status')
        }),
        ('Admin Posts', {
            'classes': ('collapse', ),
            'fields': ( 
            	'published',
            ),
        }),
    )
    

    def cover_admin(self, obj):
        return mark_safe(f'<img width="100px" height="100px" src="{obj.get_cover}">') # noqa

    cover_admin.allow_tags = True
    cover_admin.short_description = 'Cover'

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '59'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 59})},
    }
    """
    form = PostAdminForm
    prepopulated_fields = {'slug': ('title',)}
    """

    def save_model(self, request, obj, form, change):
        obj.slug = slugify(obj.title)
        # check if there exists a post with existing slug
        q = Post.objects.filter(slug=obj.slug)
        if q.exists():
            obj.slug = "-".join([obj.slug, get_random_string(4, "0123456789")])

        obj.author = request.user

        if (obj.published is None
                and obj.status in [Post.STATUS_PUBLISHED]):
            obj.published = timezone.now()
        #if change:
        else:
            obj.updated = timezone.now()
        super(PostAdmin, self).save_model(request, obj, form, change)

    #class Meta:
    #    model = Article


# Register your models here.
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
