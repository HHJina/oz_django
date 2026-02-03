from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Blog, Comment

admin.site.register(Comment)


class CommentInline(admin.TabularInline):
    model = Comment
    fields = ['content', 'author']
    extra = 1


@admin.register(Blog)
class BlogAdmin(SummernoteModelAdmin):
    inlines = [
        CommentInline
    ]