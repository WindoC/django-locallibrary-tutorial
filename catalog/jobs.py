from threading import Thread
import time
from django.core.cache import cache

class TestThread(Thread):

    daemon = True

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
        


from django.core.checks.database import check_database_backends

class CheckDB(Thread):

    daemon = True

    def run(self):

        databases = ['default','test1']
        
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
        
