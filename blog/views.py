import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, resolve_url, redirect
from django.urls import reverse_lazy
from django.views import generic
from .forms import (
    PostSearchForm, CommentCreateForm, ReplyCreateForm, PostCreateForm,
    TITLE_CONTAIN, TEXT_CONTAIN, TITLE_OR_TEXT_CONTAIN
)
from .models import Post, Tag, Comment, Reply
from .templatetags.blog import by_the_time


class PublicPostIndexView(generic.ListView):
    """公開記事の一覧を表示する。"""
    paginate_by = 10
    model = Post

    def get_queryset(self):
        queryset = super().get_queryset()
        self.form = form = PostSearchForm(self.request.GET)
        form.is_valid()

        tags = form.cleaned_data.get('search_tags')
        search_kind = form.cleaned_data.get('search_kind')
        key_word = form.cleaned_data.get('key_word')

        # タグを選択していれば、それで絞り込む
        if tags:
            for tag in tags:
                queryset = queryset.filter(tags=tag)

        # キーワードが入力されていれば、いずれかの方法で絞り込む
        # キーワードが半角スペースで区切られていれば、その回数だけfilterします。つまりANDです。
        if key_word:
            # タイトルに含む
            if search_kind == TITLE_CONTAIN:
                for word in key_word.split():
                    queryset = queryset.filter(title__icontains=word)

            # 本文に含む
            elif search_kind == TEXT_CONTAIN:
                for word in key_word.split():
                    queryset = queryset.filter(text__icontains=word)

            # タイトルか本文に含む
            elif search_kind == TITLE_OR_TEXT_CONTAIN:
                for word in key_word.split():
                    queryset = queryset.filter(Q(title__icontains=word) | Q(text__icontains=word))

        queryset = queryset.filter(
            is_public=True
        ).order_by('-created_at').prefetch_related('tags')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.form
        return context


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    """記事を作成する。"""
    model = Post
    form_class = PostCreateForm

    def get_success_url(self):
        return resolve_url('blog:post_update', pk=self.object.pk)

    def form_valid(self, form):
        messages.info(self.request, '作成しました。')
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    """記事を更新する。"""
    model = Post
    form_class = PostCreateForm

    def get_success_url(self):
        return resolve_url('blog:post_update', pk=self.object.pk)

    def form_valid(self, form):
        messages.info(self.request, '更新しました。')
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    """記事を削除する。"""
    model = Post
    success_url = reverse_lazy('blog:top')

    def post(self, request, *args, **kwargs):
        messages.info(self.request, '削除しました。')
        return super().post(request, *args, **kwargs)


class PrivatePostIndexView(LoginRequiredMixin, generic.ListView):
    """非公開の記事一覧を表示する。"""
    model = Post

    def get_queryset(self):
        queryset = Post.objects.filter(
            is_public=False
        ).order_by('-created_at').prefetch_related('tags')
        return queryset


class PostDetailView(generic.DetailView):
    """記事詳細ページを表示する。"""
    model = Post

    def get_queryset(self):
        return super().get_queryset().prefetch_related('tags', 'comment_set__reply_set')

    def get_object(self, queryset=None):
        """その記事が公開か、ユーザがログインしていれば表示する。"""
        post = super().get_object()
        if post.is_public or self.request.user.is_authenticated:
            return post
        else:
            raise Http404


class CommentCreate(generic.CreateView):
    """記事へのコメント作成ビュー。"""
    model = Comment
    form_class = CommentCreateForm

    def form_valid(self, form):
        post_pk = self.kwargs['pk']
        post = get_object_or_404(Post, pk=post_pk)
        comment = form.save(commit=False)
        comment.target = post
        comment.request = self.request
        comment.save()
        messages.info(self.request, 'コメントしました。')
        return redirect('blog:post_detail', pk=post_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])
        return context


class ReplyCreate(generic.CreateView):
    """コメントへの返信作成ビュー。"""
    model = Reply
    form_class = ReplyCreateForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        comment_pk = self.kwargs['pk']
        comment = get_object_or_404(Comment, pk=comment_pk)
        reply = form.save(commit=False)
        reply.target = comment
        reply.request = self.request
        reply.save()
        messages.info(self.request, '返信しました。')
        return redirect('blog:post_detail', pk=comment.target.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment_pk = self.kwargs['pk']
        comment = get_object_or_404(Comment, pk=comment_pk)
        context['post'] = comment.target
        return context


def api_tags_suggest(request):
    """サジェスト候補のタグをJSONで返す。"""
    keyword = request.GET.get('keyword')
    if keyword:
        tag_list = [{'pk': tag.pk, 'name': tag.name, 'name_with_count': f'{tag.name}({tag.post_count})'} for tag in Tag.objects.filter(name__icontains=keyword).annotate(post_count=Count('post'))]
    else:
        tag_list = []
    return JsonResponse({'tag_list': tag_list})


def api_posts_suggest(request):
    """サジェスト候補の記事をJSONで返す。"""
    keyword = request.GET.get('keyword')
    if keyword:
        post_list = [{'pk': post.pk, 'title': post.title} for post in Post.objects.filter(title__icontains=keyword)]
    else:
        post_list = []
    return JsonResponse({'post_list': post_list})


class APIPostList(PublicPostIndexView):
    """記事の一覧をJSONで返す。"""
    paginate_by = 10
    model = Post

    def get(self, request, *args, **kwargs):
        json_post_list = []
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        for post in context['post_list']:
            json_post = {
                'pk': post.pk,
                'title': post.title,
                'tags': [tag.name for tag in post.tags.all()],
                'updated_at': post.updated_at.strftime('%Y-%m-%d'),
                'updated_display': by_the_time(post.updated_at),
            }
            json_post_list.append(json_post)
        return JsonResponse({
            'post_list': json_post_list,
            'max_page': context['page_obj'].paginator.num_pages
        })
