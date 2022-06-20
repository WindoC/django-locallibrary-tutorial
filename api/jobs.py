from threading import Thread
import time
# from django.core.cache import cache

from django.core.checks.database import check_database_backends

import logging
logger = logging.getLogger(__name__)

db_status = {}
class DBStatus:
    
    def set(self,db,status):
        global db_status
        db_status[db] = status
    
    def get(self,db):
        global db_status
        return db_status.get(db,None)

    def dblist(self):
        global db_status
        return [db for db in db_status.keys() if db_status[db]==True]

class CheckDB(Thread):

    daemon = True   # to fix the django cmd hang issue

    def run(self):
        databases = ['aaa-1','aaa-2']
        dbstatus = DBStatus()
        while True:
            for db in databases:
                try:
                    logger.debug('jobs_CheckDB_%s check' % db)
                    checkresult = check_database_backends([db])
                    if not checkresult:
                        # cache.set('jobs_CheckDB_%s' % db,True)
                        dbstatus.set(db,True)
                        logger.debug('jobs_CheckDB_%s success' % db)
                    else:
                        # cache.set('jobs_CheckDB_%s' % db,False)
                        dbstatus.set(db,False)
                        logger.error('jobs_CheckDB_%s fail. Error: %s' % ( db , str(checkresult) ))
                except Exception as e:
                    # cache.set('jobs_CheckDB_%s' % db,False)
                    dbstatus.set(db,False)
                    logger.error('jobs_CheckDB_%s fail. Exception: %s' % ( db , str(e) ))
            time.sleep(5)
