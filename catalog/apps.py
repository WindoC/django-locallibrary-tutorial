from django.apps import AppConfig

from catalog.jobs.testthread import TestThread
from catalog.jobs.check import CheckDB

class CatalogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catalog'

    def ready(self):
        TestThread().start()
        CheckDB().start()
