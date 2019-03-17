from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = 'blog'

    def ready(self):
        # シグナルのロード
        # デコレーターで登録しているので、signals.pyを読み込む必要があるため
        import blog.signals

