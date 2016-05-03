#!/usr/bin/python3

from collections import OrderedDict

from fix.network  import  Server

from datetime import datetime, date
from fix.fix44  import  FIX44
from fix.log  import  FIX_Log
from fix.network  import  Client,  Thread
import random
import time
import string
from cfg import app, host, port, server_sender, server_target, password
import logging

LOGGER = FIX_Log()

#host = '127.0.0.1'
#port = 9121
hertbeat_interval = 0

#password=' '

print (str(server_sender)+' '+str(port))

def get_input_num(text = 'Input number'):
  select_Count = input("\n"+text+": ")
  select_Count = select_Count.strip()
  if ('' == select_Count.strip()):
    select_Count = 0
  select_Count = int(select_Count)
  return select_Count

hertbeat_interval = 0

def get_randomID(length=10):
  return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(length))
  

def process(msg,  self = None):
  #time.sleep(1)  
  msgtype= fix.get_tag(msg,  35)
  target = fix.get_tag(msg,  49)
  if (msgtype == '0'):
    msg = fix.generate_message( OrderedDict([ ('35',  '0'), ('49', server_sender), ('56' , target)]) )
  elif (msgtype == '1'):
    reqId = fix.get_tag(msg,  112) 
    msg = fix.generate_message( OrderedDict([ ('35',  '0'), ('49', server_sender), ('56' , target), ('112', reqId)]) )
  elif (msgtype == '5'):
    self.send(fix.generate_Logout_35_5())    
    msg = None
  elif (msgtype == '4'):
    fix.set_seqNum( fix.get_tag(msg,  36) )
  elif (msgtype == 'A'):
    msg =fix.generate_message ( OrderedDict([('35',  'A'), ('49', server_sender), ('56' , target), ('98', 0), ('108',  hertbeat_interval), ('141', 'N'), ('554', password)]) )
    self.send(msg)
    #msg=None
  elif (msgtype == 'AD'):
    msg =fix.generate_message ( OrderedDict([('35',  'AE'), ('49', server_sender), ('56' , target), ('98', 0), ('108',  hertbeat_interval), ('141', 'N'), ('554', password)]) )
    msg =fix.generate_message ( OrderedDict([('35', 'AQ'), ('49', server_sender), ('56' , target), ('568', '555'), ('569', '0') ]) )
    self.send(msg)
    msg =fix.generate_message ( OrderedDict([('35', 'AQ'), ('49', server_sender), ('56' , target), ('568', '555'), ('569', '1') ]) )
    self.send(msg)
    msg=None
  elif (msgtype == 'D'):
    tag_37 = ''.join(random.choice(string.digits) for x in range(10))
    msg =fix.generate_message ( OrderedDict([('35',  '8'), ('49', server_sender), ('56' , target), ('37',tag_37)]) )
    tag_37 = ''.join(random.choice(string.digits) for x in range(10))
    msg2 =fix.generate_message ( OrderedDict([('35',  '8'), ('49', server_sender), ('56' , target), ('37',tag_37)]) )
    self.send(msg+msg2)
    '''time.sleep(1)
    tag_37 = ''.join(random.choice(string.digits) for x in range(10))
    msg =fix.generate_message ( OrderedDict([('35', '8'), ('49', server_sender), ('56' , target), ('568', '555'), ('569', '0'), ('37',tag_37) ]) )
    self.send(msg)'''
    msg=None    
  else:
    msg = None
  return msg
  
fix=FIX44()
fix.init(server_sender , server_target, process )

def main():
  #fix.init(server_sender , server_target, process )
  #fix.set_seqNum(get_input_num('Input initial SuqNum'))  
  fix.set_seqNum(1)  
  srv = Server(host, port,  silent=False, fix = fix, sleep = 0.5, log_level = logging.CRITICAL)
  #srv.connect()
  #srv.listen()
  #srv.begin_listening()
  #srv.start()
    
if __name__ == '__main__':
    main()

