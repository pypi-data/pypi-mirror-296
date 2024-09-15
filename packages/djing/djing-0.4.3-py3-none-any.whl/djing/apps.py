from django.apps import AppConfig
from djing.core.application import Application


class DjingAdminConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"

    name = "djing"

    def ready(self):
        application = Application()

        application.run()
