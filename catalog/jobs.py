from threading import Thread
import time
from django.core.cache import cache

import logging
logger = logging.getLogger(__name__)


class TestThread(Thread):

    daemon = True         # to fix the django cmd hang issue

    def run(self):
        # cache.add('thread_running',0)
        while True:
            #print('Thread run %s time(s)' % cache.get('thread_running'))
            try:
                cache.incr('thread_running')
                #print('thread_running %s time(s)' % cache.get('thread_running'), file=sys.stderr)
                logger.debug('increasing cache count thread_running')
            except:
                logger.error('cache thread_running not found, create a new one.')
                cache.add('thread_running',0)
            time.sleep(5)
