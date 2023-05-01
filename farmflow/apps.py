from django.apps import AppConfig


class FarmflowConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'farmflow'

    def ready(self):
        import farmflow.signals  # noqa
