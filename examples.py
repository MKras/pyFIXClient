
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
  price = 1
  for i in range (0, 10): 
    price += 1
    tagClOrdID_526 = self.fix.get_randomID(5)    
    order_new.update(OrderedDict([ ('11', self.fix.get_randomID()), ('526', tagClOrdID_526),(('44', price))]))
    self.send(self.fix.generate_message(order_new))
    time.sleep(1)
  
  input("\nPress Enter to Logout...\n")
  #self.send(fix.generate_Logout_35_5())
  msg = self.fix.generate_Logout_35_5()
  self.send(msg)
  self.run_hertbeats = False


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
  
''' Order cancel by origClOrderID'''
@threading_deco 
def do_smth_06(msg, self):
  #!!!! Simple Test Worked 35=D Request
  #input("\nPress Enter to continue...\n")    
  tagClOrdID_11 = self.fix.get_randomID()
  tagClOrdID_526 = self.fix.get_randomID(5)
  tagClOrdID_11_old = tagClOrdID_11
    
  msg = self.fix.generate_message( OrderedDict([ ('35',  'D'),('11', tagClOrdID_11), ('1','S01-00000F00'), ('38', 10),('40', 2), ('44', 42), ('54', 1), ('55', 'AFLT'), ('60', FIX44.date_long_encode(self,  datetime.now())), ('526',tagClOrdID_526 ),  ('386', '1'), ('336', 'EQBR'), ('59', 0) ] ) )
  self.send(msg)
  time.sleep(1)
  
  tagClOrdID_11 = self.fix.get_randomID()
  msg = self.fix.generate_message( OrderedDict([ ('35',  'F'),('11', tagClOrdID_11), ('37', self.fix.get_LastOrderID_37()), ('54', 1), ('55', 'AFLT'), ('60', FIX44.date_long_encode(self,  datetime.now())) ] ) )
  self.send(msg)
  input("\nPress Enter to Logout...\n")
  #self.send(fix.generate_Logout_35_5())
  msg = self.fix.generate_Logout_35_5()
  self.send(msg)
  self.run_hertbeats = False