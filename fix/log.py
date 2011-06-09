#!/usr/bin/python3
'''Log manager class for FIX'''

from threading import Thread, Lock

mutex = Lock()

'''from threading import Thread, Lock

mutex = Lock()

def processData(data):
    mutex.acquire()
    try:
        print('Do some stuff')
    finally:
        mutex.release()

'''

class FIX_Log(object):
    FIX_LOG_IN = 'fix_log.in'
    FIX_LOG_OUT = 'fix_log.out'
    
    def __init__(self,  log_in=None,  log_out=None):
        if (log_in is not None) and (log_out is not None):
            FIX_LOG_IN = log_in
            FIX_LOG_OUT = log_out
    
    def log_in_msg(self,  msg):
        mutex.acquire()
        file = open(FIX_Log.FIX_LOG_IN, encoding='utf-8',  mode='a')
        file.write( msg ) 
        file.write('\n')
        file.close()
        mutex.release()
    
    def log_out_msg(self,  msg):
        mutex.acquire()
        file = open(FIX_Log.FIX_LOG_OUT, encoding='utf-8',  mode='a')
        file.write( msg ) 
        file.write('\n')
        file.close()
        mutex.release()
