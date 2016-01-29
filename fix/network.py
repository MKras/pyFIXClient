#!/usr/bin/env python3
'''Network manager class for FIX'''

from socket import *
from fix.log import *
import threading,  _thread
from threading import Thread, Lock
import time
import functools
from queue import Queue
import logging
#from  multiprocessing import Queue

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
            try:
              lock.acquire()
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

  def connect(self):
    print('connecting to:' ,self.addr)
    self.soc = socket(AF_INET, SOCK_STREAM) # create a TCP socket
    self.soc.connect(self.addr)
    self.begin_listening()

  def __init__(self, host = HOST,  port = PORT,  process_function = None, silent = False, fix = None, log_level = logging.CRITICAL ):
      Thread.__init__(self) 
      self.mutex = Lock()
      self.log_in = fix.SenderCompId +'.in'
      self.log_out = fix.SenderCompId +'.out'  
      self.LOGGER = FIX_Log(silent, self.log_in, self.log_out)
      self.addr = (host,  port)
      #self.soc = socket(AF_INET, SOCK_STREAM) # create a TCP socket
      #self.soc.connect(self.addr)
      self.data=''
      self.process_function = process_function
      self.BUF = BUF
      #self.begin_listening()
      self.silent = silent
      self.process_queue = Queue()
      self.send_queue = Queue()
      
      self.fix = fix
      
      # Connect
      self.connect()
      
      #HeartBeat
      self.run_hertbeats = False
      self.hertbeats_running = False
      self.hertbeat_interval = 30
      
      self.log_level = log_level
      logging.basicConfig(filename='Client.log',level = self.log_level)
       

  def print(self, text):
    if (self.silent is False):
      print (text)

  def set_process_function(self, process_function):
    self.fix.customer_processor = process_function

  def begin_listening(self):
      try:
          self.listen()
      except Exception as e:
          print ('Exception is '+str (e) ) 

  def get_self(self):
    return self

  def send(self,  msg):
    try:
      self.send_queue.put(msg)
    except Exception as exc:
     print('Queue Exception: ', exc)
      
  def send_msg(self,  msg):
    try:
      self.soc.send(msg.encode())
      logging.debug(' Client OUT: '+msg)
      self.LOGGER.log_out_msg(msg)
    except Exception as exc:
     print('Socket Exception: ', exc)
   
  def send_x_times(self,  msg, x = 1):
    for k in range(x):
      try:
        self.soc.send(msg.encode())
        print (' Client OUT: '+msg)
        self.LOGGER.log_out_msg(msg)
      except Exception as exc:
       print('Socket Exception: ', exc)
  
  @threading_deco
  def listen(self):
      threading.Thread(target = self.processor).start()
      threading.Thread(target = self.sender).start()
      threading.Thread(target = self.start_heart_beats).start()
      while True:
          self.data = self.soc.recv(self.BUF )          
          if self.data:
              data = self.data.decode('CP1251')
              self.print(' Client IN: '+str(data))
              if  data is not '':
                logging.debug(' put '+str(data)+' IN process_queue')
                self.process_queue.put(data)
                logging.debug(' PUT process_queue size = '+ str(self.process_queue.qsize()))

  def sender(self):  
    while True:
        try:
          logging.debug(' start_loop send_queue size = '+ str(self.send_queue.qsize()))          
          to_send = self.send_queue.get()
          if to_send is not None:
              self.send_msg(to_send)         
          logging.debug(' end_loop send_queue size = '+ str(self.send_queue.qsize()))   
        except Exception as exc:
            print('sender Exception: ', exc)
             
  def processor(self):  
    while True:
        try:
          logging.debug(' start_loop process_queue size = '+ str(self.process_queue.qsize()))
          to_process = self.process_queue.get() #block=False
          logging.debug(' end_loop process_queue size = '+ str(self.process_queue.qsize()))
          reply = self.process(to_process)
        except Exception as exc:
            print('processor Exception: ', exc)
    
  def process(self, msg):
      self.LOGGER.log_in_msg(msg)
      self.fix.customer_processor(msg, self) 
    
  def run(self):
      self.listen()
  
  def start_heart_beats(self):
      if(self.hertbeats_running is False):          
          self.hertbeats_running = True            
          while(True):
            if (self.run_hertbeats is True):
              logging.debug('self.run_hertbeats is True')  
              msg = self.fix.generate_Heartbeat_35_0()
              self.send(msg)
              time.sleep(self.hertbeat_interval)

##########################################################################

#@Thread
class Server( Client ):  
  def __init__(self, host = '',  port = PORT,  process_function = None, silent = False, log_in = 'server_fix_log.in', log_out = 'server_fix_log.out', sleep = 0.5 ):
      Thread.__init__(self) 
      self.mutex = Lock()
      self.LOGGER = FIX_Log(silent, log_in, log_out)
      self.addr = (host,  port)
      #self.soc = socket(AF_INET, SOCK_STREAM) # create a TCP socket
      #self.soc.connect(self.addr)
      self.data=''
      self.process_function = process_function
      self.BUF = BUF
      #self.begin_listening()
      self.silent = silent
      self.sleep = sleep
      self.connect()
      

  def begin_listening(self):
      self.listen()

  def print(self, text):
    if (self.silent is False):
      print (text)
  def set_process_function(self, process_function):
    self.process_function = process_function
      
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
      print('listen for connection')
      while True:      
          self.connect, self.addr = self.soc.accept()
          self.print('new connection detected: '+str(self.addr))
          while True:
            try:
              if self.connect == None:
                self.print(' Server self.connect == None ')
                break
              self.data = self.connect.recv(self.BUF )
              if not self.data:
                self.print(' Server NO  self.data ')
                time.sleep(self.sleep)
                break
              else:
                self.print(' Server IN: '+self.data.decode('CP1251'))
                #print(' Server IN: '+self.data.decode('CP1251'))
                self.process(self.data.decode())
            except Exception as exc:
              print('Socket Exception: ', exc)
              self.soc.close()
      self.print(' Server STOPPED listening')
  
  @synchronized(client_locker)
  def send(self, msg):
    try:
      self.connect.send(msg.encode())
      print (' Server OUT: '+msg)
      self.LOGGER.log_out_msg(msg)
    except Exception as exc:
     print('Socket Exception: ', exc)

  def connect(self):
    self.soc = socket(AF_INET, SOCK_STREAM)
    #self.soc.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    self.soc.bind(self.addr)      
    self.soc.listen(5)  
    self.begin_listening()


