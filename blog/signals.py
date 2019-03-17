from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import get_template
from .models import Comment, Reply


@receiver(post_save, sender=Comment)
def send_mail_to_author(sender, instance, created, **kwargs):
    """コメントがあったことを管理者に伝える"""
    if created:
        # views.py側で、requestオブジェクトをインスタンスに格納しています。
        request = instance.request

        # コメントの投稿者を識別するため、投稿者のセッションにコメントのpkを入れておく
        request.session[str(instance.pk)] = True

        post = instance.target
        context = {
            'post': post,
            'comment': instance,
            'request': request,
        }

        subject_template = get_template('blog/mail/comment_notify_subject.txt')
        message_template = get_template('blog/mail/comment_notify_message.txt')
        subject = subject_template.render(context)
        message = message_template.render(context)

        from_email = settings.EMAIL_HOST_USER
        recipient_list = [settings.EMAIL_HOST_USER]
        send_mail(subject, message, from_email, recipient_list)


@receiver(post_save, sender=Reply)
def send_mail_to_comment_user(sender, instance, created, **kwargs):
    """コメントに返信があったことを、管理者とコメント者に伝える"""
    if created:
        # views.py側で、requestオブジェクトをインスタンスに格納しています。
        request = instance.request

        comment = instance.target
        post = comment.target
        context = {
            'post': post,
            'comment': comment,
            'reply': instance,
            'request': request,
        }

        subject_template = get_template('blog/mail/reply_notify_subject.txt')
        message_template = get_template('blog/mail/reply_notify_message.txt')
        subject = subject_template.render(context)
        message = message_template.render(context)

        from_email = settings.EMAIL_HOST_USER
        recipient_list = []
        bcc = [settings.EMAIL_HOST_USER]
        # コメント者がメールアドレスを入力しており
        # コメント者が返信者と同一でなければ、宛先にコメント者を追加(コメントへ返信がきたよ、というお知らせ)
        if comment.email and not request.session.get(str(comment.pk)):
            recipient_list.append(comment.email)
        email = EmailMessage(subject, message, from_email, recipient_list, bcc)
        email.send()
