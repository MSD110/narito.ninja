from django import forms


class SuggestTagWidget(forms.SelectMultiple):
    template_name = 'blog/widgets/suggest_tag.html'

    class Media:
        js = ['blog/tag_suggest.js']


class SuggestPostWidget(forms.SelectMultiple):
    template_name = 'blog/widgets/suggest_post.html'

    class Media:
        js = ['blog/post_suggest.js']
