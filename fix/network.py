#!/usr/bin/env python3
'''Network manager class for FIX'''

from socket import *
from fix.log import *
import threading,  _thread
from threading import Thread, Lock
import time


def synchronized(lock):
    ''' Synchronization decorator. '''

    def wrap(f):
        def newFunction(*args, **kw):
            lock.acquire()
            try:
                return f(*args, **kw)
   
            finally:
                lock.release()
        return newFunction
    return wrap
    

#myLock = Lock()
  
  
  


HOST='127.0.0.1'
PORT=9121
BUF = 10240

########################################################################

class Client(Thread):
  def __init__(self, host = HOST,  port = PORT,  process_function = None ):
      Thread.__init__(self) 
      self.mutex = Lock()
      self.LOGGER = FIX_Log('client_fix_log.in',  'client_fix_log.out')
      self.addr = (host,  port)
      self.soc = socket(AF_INET, SOCK_STREAM) # create a TCP socket
      self.soc.connect(self.addr)
      self.data=''
      self.process_function = process_function
      self.BUF = BUF
      self.begin_listening()

  def begin_listening(self):
      try:
          thr_list = threading.Thread(target=self.listen,  args=()).start()
      except Exception as e:
          print ('Exception is '+str (e) ) 
  #@synchronized(myLock)
  def send(self,  msg):
      self.mutex.acquire()
      self.soc.send(msg.encode())
      print (' Client OUT: '+msg)
      self.LOGGER.log_out_msg(msg)
      self.mutex.release()

  def listen(self):
      #print ('Start Listening')
      while True:
          self.data = self.soc.recv(self.BUF )          
          if not self.data:
              break
          else:
              print(' Client IN: '+self.data.decode('CP1251'))
              #self.process(self.data.decode('UTF-8'))
              #self.process(self.data.decode('CP1251'))
              self.thr_proc = threading.Thread(target=self.process, args=(self.data.decode('CP1251'),)).start() 

  def process(self, msg):
      #print ('local process\n')
      msgs = self.LOGGER.log_in_msg(msg)
      if len(msgs) > 0:
       for i in range(len(msgs)):
         msg = self.process_function(msg[i],  self)
      else:
        msg = self.process_function(msg,  self)
      if msg is not None:
        print ('Client Processed: '+ msg)
        self.send(msg)  
  
  def run(self):
      self.listen()

##########################################################################

#@Thread
class Server( Thread):
  def __init__(self, host = '127.0.0.1',  port=PORT, process_function = None  ):
      Thread.__init__(self)
      #self.LOGGER = FIX_Log('server_fix_log.in',  'server_fix_log.out')
      self.addr = (host,  port)
      self.soc = socket(AF_INET, SOCK_STREAM)
      self.soc.bind(self.addr)      
      self.soc.listen(5)  
      self.process_function = process_function      
      self.BUF = BUF
      self.begin_listening()
      #process_queue = queue.Queue()

  def begin_listening(self):
      self.thr_list = threading.Thread(target=self.listen,  args=()).start()

  def run(self):
      self.listen()

  def process(self,  msg):
      time.sleep(1)
      #self.LOGGER .log_in_msg('Server: '+msg) 
      msg = self.process_function(msg, self)
      if msg is not None:
        #print ('Client Processed: '+ msg)
        self.send(msg)

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
                print ('data Recieved ')
                self.process(self.data.decode())
                #self.thr_proc = threading.Thread(target=self.process(),  args=(self.data.decode())).start() 
                #_thread.start_new_thread(self.process,  (self.data.decode(), ) )

  def send(self,  msg):
      self.connect.send(msg.encode())
      #self.LOGGER.log_out_msg('Server: '+msg)
      print('Data sended: '+msg)


