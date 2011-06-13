#!/usr/bin/python3
'''Network manager class for FIX'''

from socket import *
from fix.log import *

'''from fix.fix44  import  FIX44
from collections import OrderedDict'''

import threading
'''Thread for decorator'''
#@Thread

def deco (f):
    class Thread(threading.Thread):
        def __init__(self, f, *args, **kw):
            threading.Thread.__init__(self)
            #self.run = f(*args, **kw)
            self.run = f()


class NetWork (threading.Thread):
  HOST='127.0.0.1'
  PORT=9120
  BUF = 10240
  LOGGER = FIX_Log()
  ADDR = (HOST,int(PORT))
  def __init__ (self, host = '127.0.0.1',  port=9120 ):
      NetWork.HOST = host
      NetWork.PORT = int(port)
      NetWork.ADDR = (NetWork.HOST, NetWork.PORT)

  def get_addr(self):
      return NetWork.ADDR
  
  def get_logger(self):
      return self.LOGGER


class Client(NetWork):
        
  def __init__(self, host = '127.0.0.1',  port=9120 ):
      super().__init__(host,  int(port))
      self.soc = socket(AF_INET, SOCK_STREAM) # create a TCP socket
      self.soc.connect(NetWork.ADDR)
      self.data=''
      
  def run(self):
      listen(self)
  
  def send(self,  msg):
      self.soc.send(msg.encode())
      NetWork.LOGGER.log_out_msg('Client: '+msg)
    
  #@deco
  def listen(self):
      while True:
          self.data = self.soc.recv(NetWork.BUF)
          if not self.data:
              continue
          else:
              self.process(self.data.decode())
  
  def process(self,  msg):
      super().LOGGER.log_in_msg('Client: '+msg) 
      #self.send(msg)  

class Server(NetWork):
  def __init__(self, host = '127.0.0.1',  port=9120 ):
      super().__init__(host,  port)
      self.soc = socket(AF_INET, SOCK_STREAM)
      self.soc.bind(super().get_addr())      
      self.soc.listen(5)
      self.connect, self.addr = self.soc.accept()
      self.listen()

  def process(self,  msg):
      '''fix=FIX44()
      fix.init('Sender',  'Target')
      msg =OrderedDict([('35',  'A') ])
      msg= fix.generate_message(msg) 
      #msg = str(msg)'''
      super().LOGGER.log_in_msg('Server: '+msg) 
      self.send(msg)

  #@Thread
  #@deco
  def listen(self):
      while True:
          self.data = self.connect.recv(NetWork.BUF)
          if not self.data:
              continue
          else:
              self.process(self.data.decode())


  #@Thread
  def send(self,  msg):
      self.connect.send(msg.encode())
      NetWork.LOGGER.log_out_msg('Server: '+msg)


