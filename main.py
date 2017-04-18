#!/usr/bin/env python3

from collections import OrderedDict
import sys
from datetime import datetime, date
from fix.fix44  import  FIX44
from fix.log  import  FIX_Log
from fix.network  import  Client, threading_deco
from fix.baseprocessor  import  BaseProcessor
from cfg import app, host, port, client_sender, client_target, password
import random
import time
import threading,  _thread
from threading import Thread, Lock
import string
import logging
from queue import Queue

import examples

##############################################################################################################################



    
class processor(BaseProcessor):
    
    def __init__(self):
        self.counter = 0
        #fix_self.run_hertbeats = False
        self.process_queue = Queue()
        self.run_processot = True
        self.listten_thread = threading.Thread(target = self.messages_processor).start()
    
    #@threading_deco 
    def do_smth(self, msg, fix_self):
      for i in range (0, 5):
        tagClOrdID_11 = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
        tagClOrdID_526 = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(5))
        tagClOrdID_11_old = tagClOrdID_11
        #msg = fix.generate_message( OrderedDict([ ('35',  'D'),('11', tagClOrdID_11), ('1','S01-00000F00'), ('38', 2),('40', 2), ('44', 76), ('54', 1), ('55', 'SBER'),   ('386', '1'), ('336', 'EQBR'), ('59', 0) ] ) )
        msg = fix.generate_message( OrderedDict([ ('35',  'D'),('11', tagClOrdID_11), ('1','S01-00000F00'), ('38', 10),('40', 2), ('44', 42), ('54', 1), ('55', 'AFLT'), ('526',tagClOrdID_526 ),  ('386', '1'), ('336', 'EQBR'), ('59', 0) ] ) )
        fix_self.send(msg)
        time.sleep(1)
        
      #time.sleep(5)    
      input("\nPress Enter to Logout...\n")
      #fix_self.send(fix.generate_Logout_35_5())
      msg = fix.generate_Logout_35_5()
      fix_self.send(msg)
      fix_self.run_hertbeats = False
      self.run_processot = False
      self.listten_thread.join()
      
    
    def accept_message(self, msg, fix_self = None):
      logging.debug(' processor msg: '+ str(msg))
      logging.debug(' processor PUT msg to queue: '+ str(self.process_queue.qsize()))
      self.process_queue.put((msg, fix_self)) 

    
    #@threading_deco 
    def messages_processor(self):
        while self.run_processot:
            (msg, fix_self)  = self.process_queue.get() 
            if (msg is not None and fix_self is not None):
                logging.debug(' messages_processor msg: '+ str(msg))
                logging.debug(' messages_processor GET msg from queue: '+ str(self.process_queue.qsize()))
                self.process(msg, fix_self)
            else:
                logging.debug(' messages_processor msg is NONE '+ str(msg))


    
    
    def process(self, msg, fix_self = None):
      #global run_hertbeats
      #self.counter += 1
      self.counter += 1
      print ("\nself.counter = "+str(self.counter)+"\n")
      #time.sleep(1)
      logging.debug('processor -> process msg: '+msg)
      msgtype= fix.get_tag(msg,  35)
      if (msgtype == '0'):
        msg = fix.generate_message( OrderedDict([ ('35',  '0'), ('49', client_sender), ('56' , client_target)]) )
        #fix_self.send(msg)
        #msg = None
      elif (msgtype == '8'):
        fix.set_LastOrderID_37(fix.get_tag(msg,  37))    
        #print ('TAG 37 = '+fix.get_tag(msg,  37))
        #print ('MSG WAS: '+msg)
        msg = None
      elif (msgtype == '1'):
        reqId = fix.get_tag(msg,  112) 
        msg = fix.generate_message( OrderedDict([ ('35',  '0'), ('49', client_sender), ('56' , client_target), ('112', reqId)]) )
        #fix_self.send(msg)
        #msg = None
      elif (msgtype == '5'):
        msg = None
      elif (msgtype == '4'):
        fix.set_seqNum( fix.get_tag(msg,  36) )
        msg = None
      elif (msgtype == 'A'):    
        fix_self.run_hertbeats = True      
        #examples.do_smth(msg, fix_self)
        #10 35=D
        #examples.do_smth_01(msg, fix_self)
        #examples.do_smth_02(msg, fix_self)
        #examples.do_smth_03(msg, fix_self)
        #examples.do_smth_04(msg, fix_self)
        #examples.do_smth_05(msg, fix_self)
        #examples.do_smth_06(msg, fix_self)
        #examples.do_smth_07(msg, fix_self)
        self.do_smth(msg, fix_self)
        #msg=None
      else:
        msg = None
      return msg
##############################################################################################################################

processor_inst = processor()

fix=FIX44()
#fix.init(client_sender , client_target, processor_inst.process)
fix.init(client_sender , client_target, processor_inst.accept_message)
#logon_msg = fix.generate_Login_35_A(0, password,OrderedDict([ ('98', 0), ('141', 'N'),('554', ' '), ('925', 'newpass')]) )
#logon_msg = fix.generate_Login_35_A(0, password,OrderedDict([ ('98', 0), ('141', 'Y')]) )
if 0 == fix.get_seqNum():
    logon_msg = fix.generate_Login_35_A(0, password,OrderedDict([ ('98', 0), ('141', 'Y')]) )
else:
    logon_msg = fix.generate_Login_35_A(0, password,OrderedDict([ ('98', 0), ('141', 'N')]) )

'''#fix_msg='8=FIX.4.4^9=105^35=AD^49=MU0055600003^56=MFIXTradeCaptureID^34=3^52=20110711-16:41:58^568=20110711-17:41:583^569=0^569=1^263=1^10=59'
#fix.parce(fix_msg)
#test_file.txt
print (fix.get_fix_messages_from_file('test_file.txt', FIX44.SOH))
print (fix.get_parsed_fix_messages_from_file('test_file.txt', FIX44.SOH))
#print (fix_msg)
print("Exiting!!!!")
#time.sleep(15)
sys.exit(0)'''


##############################################################################################################################


def main():
    #cl = Client(host, port,  silent=False, fix = fix, log_level = logging.CRITICAL)
    cl = Client(host, port,  silent=False, fix = fix, log_level = logging.DEBUG)
    cl.send(logon_msg)
    

if __name__ == '__main__':
    main()
