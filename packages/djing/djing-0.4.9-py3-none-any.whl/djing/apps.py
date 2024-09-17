from django.apps import AppConfig
from djing.core.application import Application
from djing.core.inertia_application import InertiaApplication


class DjingAdminConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"

    name = "djing"

    def ready(self):
        inertia_application = InertiaApplication()

        inertia_application.boot()

        application = Application()

        if application.is_published():
            application.boot()
            application.run()
