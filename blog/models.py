from django.contrib.sites.models import Site
from django.db import models
from markdownx.models import MarkdownxField


class Tag(models.Model):
    name = models.CharField('タグ名', max_length=255, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    """記事"""
    title = models.CharField('タイトル', max_length=255)
    text = MarkdownxField('本文')
    tags = models.ManyToManyField(Tag, verbose_name='タグ', blank=True)

    relation_posts = models.ManyToManyField('self', verbose_name='関連記事', blank=True)
    is_public = models.BooleanField('公開可能か?', default=True)
    description = models.TextField('記事の説明')
    keywords = models.CharField('記事のキーワード', max_length=255, default='記事のキーワード')
    created_at = models.DateTimeField('作成日', auto_now_add=True)
    updated_at = models.DateTimeField('更新日', auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """記事に紐づくコメント"""
    name = models.CharField('名前', max_length=255, default='名無し')
    text = MarkdownxField('本文', help_text='Markdownに対応しています。')
    email = models.EmailField('メールアドレス', blank=True, help_text='入力しておくと、返信があった際に通知します。コメント欄には表示されません。')
    target = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='対象記事')
    created_at = models.DateTimeField('作成日', auto_now_add=True)

    def __str__(self):
        return self.text[:20]


class Reply(models.Model):
    """コメントに紐づく返信"""
    name = models.CharField('名前', max_length=255, default='名無し')
    text = MarkdownxField('本文', help_text='Markdownに対応しています。')
    target = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name='対象コメント')
    created_at = models.DateTimeField('作成日', auto_now_add=True)

    def __str__(self):
        return self.text[:20]
