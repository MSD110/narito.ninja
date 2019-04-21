from django import forms
from .fields import SimpleCaptchaField
from .models import Comment, Reply, Tag, Post, EmailPush
from .widgets import SuggestTagWidget, SuggestPostWidget

from markdownx.widgets import MarkdownxWidget

TITLE_CONTAIN = '1'
TEXT_CONTAIN = '2'
TITLE_OR_TEXT_CONTAIN = '3'


class PostSearchForm(forms.Form):
    """記事検索フォーム。"""
    search_kind = forms.ChoiceField(
        label='検索タイプ',
        required=False,
        choices=[(TITLE_CONTAIN, 'タイトルに含む'), (TEXT_CONTAIN, '本文に含む'), (TITLE_OR_TEXT_CONTAIN, 'タイトルor本文に含む')],
    )

    key_word = forms.CharField(
        label='検索キーワード',
        required=False,
        help_text='スペース区切りでAND検索'
    )

    search_tags = forms.ModelMultipleChoiceField(
        label='検索タグ',
        required=False,
        queryset=Tag.objects,
        widget=SuggestTagWidget,
    )


class PostCreateForm(forms.ModelForm):
    """記事の作成・更新フォーム"""

    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'tags': SuggestTagWidget,
            'text': MarkdownxWidget,
            'relation_posts': SuggestPostWidget,
        }


class CommentCreateForm(forms.ModelForm):
    """コメント投稿フォーム"""
    captcha = SimpleCaptchaField(
        widget=forms.TextInput(attrs={'class': 'input'}),
    )

    class Meta:
        model = Comment
        fields = ('name', 'text', 'email')


class ReplyCreateForm(forms.ModelForm):
    """返信コメント投稿フォーム"""

    captcha = SimpleCaptchaField(
        widget=forms.TextInput(attrs={'class': 'input'}),
    )

    class Meta:
        model = Reply
        fields = ('name', 'text')


class EmailForm(forms.ModelForm):
    """Eメール通知の登録用フォーム"""

    class Meta:
        model = EmailPush
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data['email']
        EmailPush.objects.filter(email=email, is_active=False).delete()
        return email
