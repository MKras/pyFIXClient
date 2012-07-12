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

global next_seqNum
global client
client = Client(host, port, None, silent = False)

class TestSequenceFunctions(unittest.TestCase):
  def setUp(self):    
    self.fix=FIX44()
    self.fix.init(sender , target )
    #logon_msg = fix.generate_Login_35_A(0, password,OrderedDict([ ('98', 0), ('141', 'N'),('554', ' '), ('925', 'newpass')]) )
    self.logon_msg = self.fix.generate_Login_35_A(0, password,OrderedDict([ ('98', 0), ('141', 'Y')]) )      
    self.connection = None        
    global next_seqNum   
    global client    
    pass
    
  def test_1(self):  
    '''Test 1 failed'''
    global next_seqNum
    global client
    self.test_case1 = Case_1(self.fix)
    client.set_process_function(self.test_case1.process)
    client.send(self.logon_msg)
    while(False == self.test_case1.finished):
      print('test_1 waiting 5 sec')
      time.sleep(5)    
    self.assert_(True == self.test_case1.test_passed)
    #next_seqNum = self.test_case1.get_seqNum()
    next_seqNum = self.fix.get_seqNum()
    print('self.test_case1.get_next_seqNum() = ',self.test_case1.get_seqNum())
    print('self.next_seqNum = ',next_seqNum)
    
  def test_2(self):  
    '''Test 2 failed'''
    global next_seqNum
    global client
    print('self.next_seqNum = ',next_seqNum)
    self.fix.set_seqNum(next_seqNum)
    self.test_case2 = Case_2(self.fix)
    client.set_process_function(self.test_case2.process)
    self.test_case2.go_on(client.get_self())
    while(False == self.test_case2.finished):
      print('test_2 waiting 5 sec')
      time.sleep(5)
    self.assert_(True == self.test_case2.test_passed)
    #self.fix.set_seqNum('self.test_case2.get_next_seqNum() = ',self.test_case2.get_seqNum())
    #next_seqNum = self.test_case2.get_seqNum()
    next_seqNum = self.fix.get_seqNum()

##############################################################################################################################


def local_main():
    cl = Client(host, port,  process)
    cl.send(logon_msg)  



if __name__ == '__main__':
    unittest.main()

    