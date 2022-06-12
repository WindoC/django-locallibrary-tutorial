from django.apps import AppConfig


class CatalogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catalog'

    def ready(self):
        TestThread().start()
        

from threading import Thread
import time
from django.core.cache import cache

class TestThread(Thread):

    def run(self):
        cache.add('thread_running',0)
        while True:
            #print('Thread run %s time(s)' % cache.get('thread_running'))
            try:
                cache.incr('thread_running')
                #print('thread_running %s time(s)' % cache.get('thread_running'), file=sys.stderr)
            except:
                cache.add('thread_running',0)
            time.sleep(5)
        
