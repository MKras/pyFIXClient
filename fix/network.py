#!/usr/bin/python3
'''Network manager class for FIX'''

from socket import *
from fix.log import *

import threading
'''Thread for decorator'''
#@Thread

class Thread(threading.Thread):
    def __init__(self, f, *args, **kw):
        threading.Thread.__init__(self)
        self.run = f(*args, **kw)

class NetWork (object):
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
  
  def send(self,  msg):
      self.soc.send(msg.encode())
      NetWork.LOGGER.log_out_msg(msg)
  
  
class Server(NetWork):
  def __init__(self, host = '127.0.0.1',  port=9120 ):
      super().__init__(host,  port)
      self.soc = socket(AF_INET, SOCK_STREAM)
      self.soc.bind(super().get_addr())      
      self.soc.listen(5)
      self.connect, self.addr = self.soc.accept()   

  def process(self,  msg):
      super().LOGGER.log_in_msg(msg) 
      self.send(msg)

  #@Thread
  def start(self):
      while True:
          self.data = self.connect.recv(NetWork.BUF)
          if not self.data:
              continue
          else:
              #self.data = str(self.data)
              #print (self.data)
              #self.connect.send(self.data)
              self.process(self.data.decode())

  #@Thread
  def send(self,  msg):
      self.connect.send(msg.encode())
      NetWork.LOGGER.log_in_msg(msg)


