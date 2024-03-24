from django.apps import AppConfig


class EdusystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'edusystem'

    def ready(self):
        from edusystem import signals
