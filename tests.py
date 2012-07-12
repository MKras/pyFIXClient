#!/usr/bin/env python3

import unittest
from collections import OrderedDict
import sys
from datetime import datetime, date
from fix.fix44  import  FIX44
from fix.log  import  FIX_Log
from fix.network  import  Client  
from fix.tests_processors import *
from cfg import app, host, port, sender, target, password
import random
import time
import threading,  _thread
from threading import Thread, Lock
import string



LOGGER = FIX_Log()

hertbeat_interval = 0
class TestSequenceFunctions(unittest.TestCase):
  def setUp(self):    
    self.fix=FIX44()
    self.fix.init(sender , target )
    #logon_msg = fix.generate_Login_35_A(0, password,OrderedDict([ ('98', 0), ('141', 'N'),('554', ' '), ('925', 'newpass')]) )
    self.logon_msg = self.fix.generate_Login_35_A(0, password,OrderedDict([ ('98', 0), ('141', 'Y')]) )  
    self.client = Client(host, port, None, silent = False)
    pass
    
  def test_1(self):  
    '''Test 1 failed'''
    self.test_case1 = Case_1(self.fix)
    self.client.set_process_function(self.test_case1.process)
    self.client.send(self.logon_msg)
    while(False == self.test_case1.finished):
      print('test_1 waiting 5 sec')
      time.sleep(5)    
    self.assert_(True == self.test_case1.test_passed)    
    
  def test_2(self):  
    '''Test 2 failed'''
    self.test_case2 = Case_2(self.fix)
    self.client.set_process_function(self.test_case2.process)
    self.client.send(self.logon_msg)
    while(False == self.test_case2.finished):
      print('test_2 waiting 5 sec')
      time.sleep(5)
    self.assert_(True == self.test_case2.test_passed)


##############################################################################################################################


def local_main():
    cl = Client(host, port,  process)
    cl.send(logon_msg)  



if __name__ == '__main__':
    unittest.main()

    