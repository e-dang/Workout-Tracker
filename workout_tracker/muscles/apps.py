from django.apps import AppConfig


class MusclesConfig(AppConfig):
    name = 'muscles'

    def ready(self):
        import muscles.signals  # noqa
