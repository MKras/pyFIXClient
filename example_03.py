
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

''' Order cancel by origClOrderID'''

@threading_deco 
def do_smth_03(msg, self):
  #!!!! Simple Test Worked 35=D Request
  #input("\nPress Enter to continue...\n")    
  tagClOrdID_11 = self.fix.get_randomID()
  tagClOrdID_526 = self.fix.get_randomID(5)
  tagClOrdID_11_old = tagClOrdID_11
    
  msg = self.fix.generate_message( OrderedDict([ ('35',  'D'),('11', tagClOrdID_11), ('1','S01-00000F00'), ('38', 10),('40', 2), ('44', 42), ('54', 1), ('55', 'AFLT'), ('60', FIX44.date_long_encode(self,  datetime.now())), ('526',tagClOrdID_526 ),  ('386', '1'), ('336', 'EQBR'), ('59', 0) ] ) )
  self.send(msg)
  time.sleep(1)
  
  tagClOrdID_11 = self.fix.get_randomID()
  msg = self.fix.generate_message( OrderedDict([ ('35',  'F'),('11', tagClOrdID_11), ('41', tagClOrdID_11_old), ('54', 1), ('55', 'AFLT'), ('60', FIX44.date_long_encode(self,  datetime.now())) ] ) )
  self.send(msg)
  input("\nPress Enter to Logout...\n")
  #self.send(fix.generate_Logout_35_5())
  msg = self.fix.generate_Logout_35_5()
  self.send(msg)
  self.run_hertbeats = False