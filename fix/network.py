#!/usr/bin/env python3
'''Network manager class for FIX'''

from socket import *
from fix.log import *
import threading,  _thread
from threading import Thread, Lock
import time
import functools

def threading_deco(func):
    ''' Threading decorator. '''    
    @functools.wraps(func)
    def wrap(*args, **kw):
        thr_proc = threading.Thread(target = func, args = args, kwargs = kw).start()
    return wrap

def synchronized(lock):
    ''' Synchronization decorator. '''
    #@functools.wraps(lock)
    def wrap(func):
        def sync_function(*args, **kw):
            lock.acquire()
            try:
                return func(*args, **kw)   
            finally:
                lock.release()
        return sync_function
    return wrap
    
client_locker = Lock()
process_locker = Lock()
server_locker = Lock()
  
HOST='127.0.0.1'
PORT=9121
BUF = 10240

########################################################################

class Client(Thread):
  def __init__(self, host = HOST,  port = PORT,  process_function = None, silent = False, log_in = 'client_fix_log.in', log_out = 'client_fix_log.out' ):
      Thread.__init__(self) 
      self.mutex = Lock()
      self.LOGGER = FIX_Log(silent, log_in, log_out)
      self.addr = (host,  port)
      self.soc = socket(AF_INET, SOCK_STREAM) # create a TCP socket
      self.soc.connect(self.addr)
      self.data=''
      self.process_function = process_function
      self.BUF = BUF
      self.begin_listening()
      self.silent = silent

  def print(self, text):
    if (self.silent is False):
      print (text)
  def set_process_function(self, process_function):
    self.process_function = process_function

  def begin_listening(self):
      try:
          self.listen()
      except Exception as e:
          print ('Exception is '+str (e) ) 
          
  def get_self(self):
    return self

  @synchronized(client_locker)
  def send(self,  msg):
      self.soc.send(msg.encode())
      self.print (' Client OUT: '+msg)
      self.LOGGER.log_out_msg(msg)

  @threading_deco
  def listen(self):
      #self.print ('Start Listening')
      while True:
          self.data = self.soc.recv(self.BUF )          
          if not self.data:
              break
          else:
              self.print(' Client IN: '+self.data.decode('CP1251'))
              self.process(self.data.decode('CP1251'))

  @threading_deco  
  #@synchronized(process_locker)
  def process(self, msg):
      msgs = self.LOGGER.log_in_msg(msg)
      if len(msgs) > 0:
       for msg_iter in msgs:
         if not msg_iter == '':
           msg = self.process_function(msg_iter, self)
      else:
        msg = self.process_function(msg_iter, self)
      #sending messege implemented in process_function
      #if msg is not None:
        #self.print ('Client Processed: '+ msg)
        #self.send(msg)  
    
  def run(self):
      self.listen()

##########################################################################

#@Thread
class Server( Thread):
  def __init__(self, host = HOST,  port=PORT, process_function = None  ):
      Thread.__init__(self)
      self.LOGGER = FIX_Log('server_fix_log.in',  'server_fix_log.out')
      self.addr = (host,  port)
      self.soc = socket(AF_INET, SOCK_STREAM)
      self.soc.bind(self.addr)      
      self.soc.listen(5)  
      self.process_function = process_function      
      self.BUF = BUF
      self.begin_listening()

  def begin_listening(self):
      self.listen()

  def run(self):
      self.listen()
  
  @threading_deco
  def process(self,  msg):
      time.sleep(1)
      self.LOGGER.log_in_msg(msg) 
      msg = self.process_function(msg, self)
      if msg is not None:
        #self.print ('Client Processed: '+ msg)
        self.send(msg)

  @threading_deco
  def listen(self):
      while True:
          self.connect, self.addr = self.soc.accept()
          while True:
            if self.connect == None:
                break 
            self.data = self.connect.recv(self.BUF )
            if not self.data:
                break
            else:
                self.print(' Server IN: '+self.data.decode('CP1251'))
                self.process(self.data.decode())
  
  @synchronized(server_locker)
  def send(self,  msg):
      self.connect.send(msg.encode())
      self.LOGGER.log_out_msg(msg)
      self.print (' Server OUT: '+msg)


