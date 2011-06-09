#!/usr/bin/python3
'''Network manager class for FIX'''

from socket import *



class NetWork (object):
  HOST='127.0.0.1'
  PORT='9120'
  BUF = 1024
  ADDR = (HOST,PORT)
  def __init__ (self, host = '127.0.0.1',  port='9120' ):
      NetWork.HOST = host
      NetWork.PORT = port
      NetWork.ADDR = (NetWork.HOST, NetWork.PORT)
      self.LOGGER = FIX_Log()


class Client(NetWork):
  '''HOST='127.0.0.1'
  PORT='9120'''
  def __init__(self, host = '127.0.0.1',  port='9120' ):
      super().__init__(host,  port)
      self.soc = socket(AF_INET, SOCK_STREAM) # create a TCP socket
      self.soc.connect(NetWork.ADDR)
  
class Server(NetWork):
  '''HOST='127.0.0.1'
  PORT='9120'''
  def __init__(self, host = '127.0.0.1',  port='9120' ):
      super().__init__(host,  port)
      self.soc = socket(AF_INET, SOCK_STREAM) # create a TCP socket
      self.soc.bind(supre().NetWork.ADDR)
      self.soc.listen(5)
      self.connect, self.addr = self.soc.accept()   
      
  def start(self):
      while True:
          self.data = connect.recv(supre().NetWork.ADDR)
          if not data:
              continue
          else:
              process(self.data.decode())
    
  def process(self,  msg):
      super().LOGGER.log_in_msg(msg) 

  def send(self,  msg):
      soc.send(msg.encode())
      
      '''while True:
          data = input("Enter something: ")
          soc.send(data.encode())
          if (data == "exit"):
              break'''

  
  
  '''Client - import sys
from socket import *
import pickle  

host = "localhost"
port = 21567
buf = 1024
addr = (host,port)

soc = socket(AF_INET, SOCK_STREAM) # create a TCP socket

soc.connect(addr)

while True:
    data = input("Enter something: ")
    soc.send(data.encode())
    if (data == "exit"):
        break'''


'''Server -from socket import *
import pickle  

host = "localhost"
port = 21567
buf = 1024
addr = (host,port)

soc = socket(AF_INET, SOCK_STREAM) # create a TCP socket
soc.bind(addr)
soc.listen(5)
connect, addr = soc.accept()   

while True:
    
    data = connect.recv(buf)   
    
    if not data:
        continue
    else:
        file = open('server.in', encoding='utf-8',  mode='a')
        file.write("from "+str(addr)+" message: "+data.decode())
        file.write('\n')
        file.close()
        
        if (str(data.decode()) == "exit" ):
            break

soc.close()'''
