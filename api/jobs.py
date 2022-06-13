from threading import Thread
import time
from django.core.cache import cache


from django.core.checks.database import check_database_backends

class CheckDB(Thread):

    daemon = True   # to fix the django cmd hang issue

    def run(self):

        databases = ['aaa-1','aaa-2']
        
        while True:
            for db in databases:
                try:
                    checkresult = check_database_backends([db])
                    if not checkresult:
                        cache.set('jobs_CheckDB_%s' % db,True)
                    else:
                        cache.set('jobs_CheckDB_%s' % db,False)
                except:
                    cache.set('jobs_CheckDB_%s' % db,False)
            time.sleep(5)
