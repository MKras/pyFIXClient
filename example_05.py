
from collections import OrderedDict
import sys
from datetime import datetime, date
from fix.fix44  import  FIX44
from fix.log  import  FIX_Log
from fix.network  import  Client, threading_deco
from cfg import app, host, port, client_sender, client_target, password
import random
import time
import threading,  _thread
from threading import Thread, Lock
import string
import logging

''' Parce and send from file'''

@threading_deco 
def do_smth_05(msg, self):
  #!!!! Simple Test Worked 35=D Request
  #input("\nPress Enter to continue...\n")
  
  filename = 'msgs_list.txt'
  msgs_list = self.fix.get_parsed_fix_messages_from_file( filename, split_symbol = '', encod = 'utf-8')
  for msg in msgs_list:
    self.send(msg)
    time.sleep(1)
  
  input("\nPress Enter to Logout...\n")
  #self.send(fix.generate_Logout_35_5())
  msg = self.fix.generate_Logout_35_5()
  self.send(msg)
  self.run_hertbeats = False
  