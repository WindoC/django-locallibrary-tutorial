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
        
