
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

@threading_deco 
def do_smth_01(msg, self):
  #!!!! Simple Test Worked 35=D Request
  #input("\nPress Enter to continue...\n")    
  order_new = OrderedDict([ ('35',  'D'),('11', self.fix.get_randomID()), ('1','S01-00000F00'), ('38', 10),('40', 2), ('44', 42), ('54', 1), ('55', 'AFLT'), ('526','' ),  ('386', '1'), ('336', 'EQBR'), ('59', 0) ] ) 
  for i in range (0, 10):    
    tagClOrdID_526 = self.fix.get_randomID(5)    
    order_new.update(OrderedDict([ ('11', self.fix.get_randomID()), ('526', tagClOrdID_526)]))
    self.send(self.fix.generate_message(order_new))
    time.sleep(1)
  
  input("\nPress Enter to Logout...\n")
  #self.send(fix.generate_Logout_35_5())
  msg = self.fix.generate_Logout_35_5()
  self.send(msg)
  self.run_hertbeats = False