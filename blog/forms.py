from django import forms
from .fields import SimpleCaptchaField
from .models import Comment, Reply, Tag, Post
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
        widget=forms.TextInput(
            attrs={'class': 'input'}
        ),
        help_text='スペース区切りでAND検索'
    )

    search_tags = forms.ModelMultipleChoiceField(
        label='検索タグ',
        required=False,
        queryset=Tag.objects,
        widget=SuggestTagWidget,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.help_text


class PostCreateForm(forms.ModelForm):

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
        widgets = {
            'name': forms.TextInput(attrs={
                'class': "input",
            }),
            'email': forms.EmailInput(attrs={
                'class': "input",
            }),
            'text': MarkdownxWidget(attrs={
                'class': 'textarea',
            })
        }


class ReplyCreateForm(forms.ModelForm):
    """返信コメント投稿フォーム"""

    captcha = SimpleCaptchaField(
        widget=forms.TextInput(attrs={'class': 'input'}),
    )

    class Meta:
        model = Reply
        fields = ('name', 'text')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': "input",
            }),
            'text': MarkdownxWidget(attrs={
                'class': 'textarea',
            })
        }
