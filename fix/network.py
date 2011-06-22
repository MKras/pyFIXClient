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
      #NetWork.BUF = 10240

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
  def __init__(self, host = '127.0.0.1',  port = 9120 ):
      Thread.__init__(self)
      super().__init__(host,  int(port))
      self.soc = socket(AF_INET, SOCK_STREAM) # create a TCP socket
      self.soc.connect(NetWork.ADDR)
      self.data=''
      self.BUF = NetWork.BUF
      #self.begin_listening()

  def begin_listening(self):
      _thread.start_new_thread(self.listen, ())
  
  def send(self,  msg):
      self.soc.send(msg.encode())
      print (('Client: '+msg))
      super().LOGGER.log_out_msg('Client: '+msg)
    
  def listen(self):
      while True:
          self.data = self.soc.recv(self.BUF )
          if not self.data:
              continue
          else:
              self.process(self.data.decode())
  
  def process(self,  msg):
      super().LOGGER.log_in_msg('Client: '+msg) 
      #self.send(msg)  
  
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
      self.connect, self.addr = self.soc.accept()
      self.BUF = NetWork.BUF
      #self.begin_listening()

  def begin_listening(self):
      _thread.start_new_thread(self.listen,  ( ))

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
          self.data = self.connect.recv(self.BUF )
          if not self.data:
              continue
          else:
              self.process(self.data.decode())
              #_thread.start_new_thread(self.process,  (self.data.decode(), ) )

  def send(self,  msg):
      self.connect.send(msg.encode())
      self.LOGGER.log_out_msg('Server: '+msg)


