#!/usr/bin/env python3

import unittest
from collections import OrderedDict
import sys
from datetime import datetime, date
from fix.fix44  import  FIX44
from fix.log  import  FIX_Log
from fix.network  import  Client  
from cfg import app, host, port, sender, target, password
import random
import time
import threading,  _thread
from threading import Thread, Lock
import string



LOGGER = FIX_Log()

hertbeat_interval = 0
###############################################################################################################################
class Processor:
  def __init__(self):
    self.test_passed = False
    self.processed = False
    self.finish = False
    pass

  def process(self, msg, network_self = None):
    if (fix.get_tag(msg,  35) == '0'):
      msg = fix.generate_message( OrderedDict([ ('35',  '0'), ('49', sender), ('56' , target)]) )
    elif (fix.get_tag(msg,  35) == '8'):
      self.test(msg)
      self.finish_test()
      pass
    elif (fix.get_tag(msg,  35) == '1'):
      reqId = fix.get_tag(msg,  112) 
      msg = fix.generate_message( OrderedDict([ ('35',  '0'), ('49', sender), ('56' , target), ('112', reqId)]) )
    elif (fix.get_tag(msg,  35) == '5'):
      msg = None
    elif (fix.get_tag(msg,  35) == '4'):
      fix.set_seqNum( fix.get_tag(msg,  36) )
    elif (fix.get_tag(msg,  35) == 'A'):
      return self.processor(msg, network_self)
      msg=None
    else:
      msg = None
    return msg

  def processor(self, msg, network_self = None):
    self.network_self = network_self
    #input("\nPress Enter to continue...\n")
    self.tagClOrdID_11 = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
    self.tag_11 = self.tagClOrdID_11
    self.tagClOrdID_526 = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(5))
    self.tagClOrdID_11_old = self.tagClOrdID_11
    msg = fix.generate_message( OrderedDict([ ('35',  'D'),('11', self.tagClOrdID_11), ('1','S01-00000F00'), ('38', 5),('40', 2), ('44', 42), ('54', 1), ('55', 'AFLT'), ('526',self.tagClOrdID_526 ),  ('386', '1'), ('336', 'EQBR'), ('59', 0) ] ) )
    network_self.send(msg)
    self.processed = True

  def finish_test(self):
    if(True == self.finish):
      input("\nPress Enter to Logout...\n")
      self.network_self.send(fix.generate_Logout_35_5())
    
  def test(self, msg):
    print('TEST msg = :',msg)
    self.test_passed =  (fix.get_tag(msg, 11) == self.tag_11)
    print('fix.get_tag(msg, 11) = ',fix.get_tag(msg, 11), ' self.tag_11 = ',self.tag_11)
    self.finish = True
    pass


class TestSequenceFunctions(unittest.TestCase):
  def setUp(self):
    self.processor = Processor()
    self.process = self.processor.process 
    
    self.cl = Client(host, port, self.process)
    self.cl.send(logon_msg)    
    
  def test_1(self):
    '''Test 1 failed'''
    while(False == self.processor.processed):
      print('test_1 waiting 5 sec')
      time.sleep(5)
    self.assert_(True == self.processor.test_passed)    
    


fix=FIX44()
fix.init(sender , target )
#logon_msg = fix.generate_Login_35_A(0, password,OrderedDict([ ('98', 0), ('141', 'N'),('554', ' '), ('925', 'newpass')]) )
logon_msg = fix.generate_Login_35_A(0, password,OrderedDict([ ('98', 0), ('141', 'Y')]) )

##############################################################################################################################


def local_main():
    cl = Client(host, port,  process)
    cl.send(logon_msg)  



if __name__ == '__main__':
    unittest.main()
