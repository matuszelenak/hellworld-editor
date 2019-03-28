from django.apps import AppConfig


class SubmitConfig(AppConfig):
    name = 'submit'

    def ready(self):
        from . import signals
