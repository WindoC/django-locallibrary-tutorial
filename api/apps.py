from django.apps import AppConfig

from .jobs import CheckDB

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        CheckDB().start()
