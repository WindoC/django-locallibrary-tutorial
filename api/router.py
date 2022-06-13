import random

from django.core.cache import cache

class Router:
    """
    A router to control all database operations on models in the
    auth and contenttypes applications.
    """
    route_app_labels = [ 'api' ]
    router_db =  [ 'aaa-1' , 'aaa-2' ]
    default_db_module = ['accounting']

    def _checkdb_result(self):
        list_db = []
        for db in self.router_db:
            try:
                if cache.get('jobs_CheckDB_%s' % db):
                    list_db.append(db)
            except:
                pass
        return list_db

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels and model._meta.model_name not in self.default_db_module:
            return random.choice(self._checkdb_result())
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels and model._meta.model_name not in self.default_db_module:
            return random.choice(self._checkdb_result())
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (obj1._meta.app_label in self.route_app_labels
                or obj2._meta.app_label in self.route_app_labels):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if ( db in self.router_db or app_label in self.route_app_labels ) and model_name not in self.default_db_module:
            return False  # we're not using syncdb on our legacy database
        else:  # but all other models/databases are fine
            return None
