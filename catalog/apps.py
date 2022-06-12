from django.apps import AppConfig

from .jobs import TestThread, CheckDB

class CatalogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catalog'

    def ready(self):
        TestThread().start()
        CheckDB().start()
