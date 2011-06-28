#!/usr/bin/python3
'''Network manager class for FIX'''

from socket import *
from fix.log import *

'''from fix.fix44  import  FIX44
from collections import OrderedDict'''

import threading,  _thread
from threading import Thread

'''Thread for decorator'''


'''class Thread(threading.Thread):
    def __init__(self, f, *args, **kw):
        threading.Thread.__init__(self)
        #self.run = f(*args, **kw)
        self.run = f()

    def run (self):
        self.run()
        pass
    
    def start (self):
        self.run()
        pass'''

'''
vlock = threading .allocate_lock()
vlock.acquire()
v += k
vlock.release()
'''


class NetWork ():
  HOST='127.0.0.1'
  PORT=9120
  BUF = 10240
  LOGGER = FIX_Log()
  ADDR = (HOST,int(PORT))
#  _initialized = False
  
  def __init__ (self, host = '127.0.0.1',  port = 9120 ):
      NetWork.HOST = host
      NetWork.PORT = int(port)
      NetWork.ADDR = (NetWork.HOST, NetWork.PORT)
      NetWork.BUF = 10240

  def get_addr(self):
      return NetWork.ADDR
  
  def get_logger(self):
      return self.LOGGER
  
  def run(self):
      listen(self)

  def listen(self):
      pass

########################################################################

class Client(NetWork,  Thread):
  def __init__(self, host = '127.0.0.1',  port = 9120,  process_function = None ):
      Thread.__init__(self)
      super().__init__(host,  int(port))
      self.LOGGER = FIX_Log('client_fix_log.in',  'client_fix_log.out')
      self.soc = socket(AF_INET, SOCK_STREAM) # create a TCP socket
      self.soc.connect(NetWork.ADDR)
      self.data=''
      self.process_function = process_function
      self.BUF = NetWork.BUF
      self.begin_listening()

  def begin_listening(self):
      try:
          thr_list = threading.Thread(target=self.listen,  args=()).start()
      except Exception as e:
          print ('Exception is '+str (e) ) 
  
  def send(self,  msg):
      self.soc.send(msg.encode())
      #print (('Client OUT: '+msg))
      self.LOGGER.log_out_msg(msg)

  def listen(self):
      #print ('Start Listening')
      while True:
          self.data = self.soc.recv(self.BUF )          
          if not self.data:
              break
          else:
              #print('Client rec: '+self.data.decode('utf-8'))
              #self.process(self.data.decode('UTF-8'))
              self.process(self.data.decode('CP1251'))
  
  def process(self,  msg):
      #print ('Client IN: '+ msg)
      self.LOGGER.log_in_msg(msg)
      msg = self.process_function(msg)
      if msg is not None:
        #print ('Client Processed: '+ msg)
        self.send(msg)  
  
  def run(self):
      self.listen()

##########################################################################

#@Thread
class Server(NetWork,  Thread):
  def __init__(self, host = '127.0.0.1',  port=9120 ):
      Thread.__init__(self)
      super().__init__(host,  port)
      self.LOGGER = FIX_Log('server_fix_log.in',  'server_fix_log.out')
      self.soc = socket(AF_INET, SOCK_STREAM)
      self.soc.bind(super().get_addr())      
      self.soc.listen(5)        
      self.BUF = NetWork.BUF
      #self.begin_listening()
      #process_queue = queue.Queue()

  def begin_listening(self):
      thr_list = threading.Thread(target=self.listen,  args=()).start()

  def run(self):
      self.listen()

  def process(self,  msg):
      '''fix=FIX44()
      fix.init('Sender',  'Target')
      msg =OrderedDict([('35',  'A') ])
      msg= fix.generate_message(msg) 
      #msg = str(msg)'''
      self.LOGGER .log_in_msg('Server: '+msg) 
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
                #_thread.start_new_thread(self.process,  (self.data.decode(), ) )

  def send(self,  msg):
      self.connect.send(msg.encode())
      self.LOGGER.log_out_msg('Server: '+msg)
      print('Data sended: '+msg)


