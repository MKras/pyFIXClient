
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

''' Group tags example'''

@threading_deco 
def do_smth_02(msg, self):
  #input("\nPress Enter to continue...\n")    
  grp_1 = self.fix.get_groupe('3',([('600', 'ACH7'),('623', 110),('624', 2),('566', 45.05),('600', 'ACM7'),('623', 777),('624', 2),('566', 85.30),('600', 'ACM6'),('623', 333),('624', 1),('566', 47.00)]))
    
  ord_35_d_sell = OrderedDict([ ('35',  'AB'),('11', self.fix.get_randomID()),('526', '3LegsTSM'), ('1','JPMNCLIENT4'), ('386', '1'), ('336', 'TAILORED'), ('625', 'SESSION'),('55', '[N/A]'), ('54', 'B'), ('167', 'MLEG'), ('762', '1'), ('555', grp_1),  ('60', FIX44.date_long_encode(self,  datetime.now())), ('38', 200), ('40', 2), ('10700', 'N'), ('5476', 'pyfixclient') ] )
  self.send(self.fix.generate_message(ord_35_d_sell))
  time.sleep(1)    
  
  
  input("\nPress Enter to Logout...\n")
  #self.send(fix.generate_Logout_35_5())
  msg = self.fix.generate_Logout_35_5()
  self.send(msg)
  self.run_hertbeats = False