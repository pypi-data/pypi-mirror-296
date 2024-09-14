from django.apps import AppConfig

from djing.core.application import Application
from djing.core.inertia_app import InertiaApp


class DjingAdminConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"

    name = "djing"

    def ready(self):
        inertia_app = InertiaApp()

        inertia_app.boot()

        application = Application()

        application.run()
