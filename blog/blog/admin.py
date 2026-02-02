from django.contrib import admin

from .models import Blog, Comment

admin.site.register(Comment)


class CommentInline(admin.TabularInline):
    model = Comment
    fields = ['content', 'author']
    extra = 1


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline
    ]