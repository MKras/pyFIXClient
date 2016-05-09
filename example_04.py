
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

''' Generate from original message'''

@threading_deco 
def do_smth_04(msg, self):
  #!!!! Simple Test Worked 35=D Request
  #input("\nPress Enter to continue...\n")    
  tagClOrdID_11 = self.fix.get_randomID()
  tagClOrdID_526 = self.fix.get_randomID(5)
  tagClOrdID_11_old = tagClOrdID_11
  #20160322-13:47:31.583 : 8=FIX.4.49=23435=D49=epam756=MFIXTradeID34=2052=20160322-13:47:31.58311=Tarass511=JPMNCLIENT4386=1336=AUST625=SESSION55=ACH7-H8.sr167=MLEG762=954=160=20160322-15:12:3338=240=244=-0.1858=Spread_Order5426=Limit_Session5476=SC_Ref10=140 
  
  msg = self.fix.parce('8=FIX.4.49=23435=D49=epam756=MFIXTradeID34=2052=20160322-13:47:31.58311=Tarass511=JPMNCLIENT4386=1336=AUST625=SESSION55=ACH7-H8.sr167=MLEG762=954=160=20160322-15:12:3338=240=244=-0.1858=Spread_Order5426=Limit_Session5476=SC_Ref10=140', split_symbol='')
  self.send(msg)
  time.sleep(1)
  
  input("\nPress Enter to Logout...\n")
  #self.send(fix.generate_Logout_35_5())
  msg = self.fix.generate_Logout_35_5()
  self.send(msg)
  self.run_hertbeats = False
  