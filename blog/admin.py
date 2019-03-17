from django.contrib import admin
from .models import Post, Comment, Reply, Tag
from markdownx.admin import MarkdownxModelAdmin


class ReplyInline(admin.StackedInline):
    model = Reply
    extra = 5


class CommentAdmin(MarkdownxModelAdmin):
    inlines = [ReplyInline]


admin.site.register(Post, MarkdownxModelAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Reply, MarkdownxModelAdmin)
admin.site.register(Tag)
