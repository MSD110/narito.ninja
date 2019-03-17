from django import template
from django.utils import timezone
from markdown import markdown
from markdownx.utils import markdownify

register = template.Library()


@register.simple_tag
def url_replace(request, field, value):
    """GETパラメータの一部を置き換える。"""
    url_dict = request.GET.copy()
    url_dict[field] = str(value)
    return url_dict.urlencode()


@register.simple_tag
def by_the_time(dt):
    """その時間が今からどのぐらい前か、人にやさしい表現で返す。"""
    result = timezone.now() - dt
    s = result.total_seconds()
    hours = int(s / 3600)
    if hours >= 24:
        day = int(hours / 24)
        return '約{0}日前'.format(day)
    elif hours == 0:
        minute = int(s / 60)
        return '約{0}分前'.format(minute)
    else:
        return '約{0}時間前'.format(hours)


@register.filter
def markdown_to_html(text):
    """マークダウンをhtmlに変換する。"""
    return markdownify(text)


@register.filter
def markdown_to_html_simple(text):
    """マークダウンをhtmlに変換する。

    拡張を含めない、シンプルな変換を行います。
    コメント欄で[TOC]を勝手に作られると困る、といった場合に有効かもしれません。

    """
    return markdown(text=text)
