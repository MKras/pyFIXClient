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
    pass
    
  def test_1(self):  
    '''Test 1 failed'''
    self.processor = Processor(self.fix)
    self.process = self.processor.process 
    
    self.cl = Client(host, port, self.process, silent = True)
    self.cl.send(self.logon_msg)
    while(False == self.processor.finished):
      print('test_1 waiting 5 sec')
      time.sleep(5)
    self.assert_(True == self.processor.test_passed)    
    

##############################################################################################################################


def local_main():
    cl = Client(host, port,  process)
    cl.send(logon_msg)  



if __name__ == '__main__':
    unittest.main()
