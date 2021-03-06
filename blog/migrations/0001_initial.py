# Generated by Django 2.1.7 on 2019-03-08 05:18

from django.db import migrations, models
import django.db.models.deletion
import markdownx.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='名無し', max_length=255, verbose_name='名前')),
                ('text', markdownx.models.MarkdownxField(help_text='Markdownに対応しています。', verbose_name='本文')),
                ('email', models.EmailField(blank=True, help_text='入力しておくと、返信があった際に通知します。コメント欄には表示されません。', max_length=254, verbose_name='メールアドレス')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='タイトル')),
                ('text', markdownx.models.MarkdownxField(verbose_name='本文')),
                ('is_public', models.BooleanField(default=True, verbose_name='公開可能か?')),
                ('description', models.TextField(verbose_name='記事の説明')),
                ('keywords', models.CharField(default='記事のキーワード', max_length=255, verbose_name='記事のキーワード')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日')),
                ('relation_posts', models.ManyToManyField(blank=True, related_name='_post_relation_posts_+', to='blog.Post', verbose_name='関連記事')),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='名無し', max_length=255, verbose_name='名前')),
                ('text', markdownx.models.MarkdownxField(help_text='Markdownに対応しています。', verbose_name='本文')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日')),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Comment', verbose_name='対象コメント')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='タグ名')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, to='blog.Tag', verbose_name='タグ'),
        ),
        migrations.AddField(
            model_name='comment',
            name='target',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Post', verbose_name='対象記事'),
        ),
    ]
