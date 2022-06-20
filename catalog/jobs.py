from threading import Thread
import time
# from django.core.cache import cache

import logging
logger = logging.getLogger(__name__)

thread_running = 0
class TestCounter:
    
    def increase(self):
        global thread_running
        thread_running += 1
    
    def get(self):
        global thread_running
        return thread_running

class TestThread(Thread):

    daemon = True         # to fix the django cmd hang issue

    def run(self):
        counter = TestCounter()
        # cache.add('thread_running',0)
        while True:
            counter.increase()
            logger.debug('Thread run %s time(s)' % counter.get())
            # #print('Thread run %s time(s)' % cache.get('thread_running'))
            # try:
            #     cache.incr('thread_running')
            #     #print('thread_running %s time(s)' % cache.get('thread_running'), file=sys.stderr)
            #     logger.debug('increasing cache count thread_running')
            # except:
            #     logger.error('cache thread_running not found, create a new one.')
            #     cache.add('thread_running',0)
            time.sleep(5)
