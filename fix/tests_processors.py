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



###############################################################################################################################
class Processor:
  #def __init__(self, fix, test_case):
  def __init__(self):
    #self.fix = fix
    
    '''self.processor = test_case.processor
    self.finish_test = test_case.finish_test
    self.test = test_case.test'''
    
    pass

  def process(self, msg, network_self = None):
    if (self.fix.get_tag(msg,  35) == '0'):
      msg = self.fix.generate_message( OrderedDict([ ('35',  '0'), ('49', sender), ('56' , target)]) )
    elif (self.fix.get_tag(msg,  35) == '8'):
      self.test(msg)
      self.finish_test()
      pass
    elif (self.fix.get_tag(msg,  35) == '1'):
      reqId = self.fix.get_tag(msg,  112) 
      msg = self.fix.generate_message( OrderedDict([ ('35',  '0'), ('49', sender), ('56' , target), ('112', reqId)]) )
    elif (self.fix.get_tag(msg,  35) == '5'):
      msg = None
    elif (self.fix.get_tag(msg,  35) == '4'):
      self.fix.set_seqNum( self.fix.get_tag(msg,  36) )
    elif (self.fix.get_tag(msg,  35) == 'A'):
      return self.processor(msg, network_self)
      msg=None
    else:
      msg = None
    return msg


class Case_1(Processor):
  def __init__(self, fix):
    self.fix = fix 
    self.test_passed = False
    self.processed = False
    self.finish = False
    self.finished = False
    self.tag_151 = -1
    super(Processor, self).__init__()
    pass
    
  def processor(self, msg, network_self = None):
    self.network_self = network_self
    #input("\nPress Enter to continue...\n")
    self.tagClOrdID_11 = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
    self.tag_11 = self.tagClOrdID_11
    self.tagClOrdID_526 = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(5))
    self.tagClOrdID_11_old = self.tagClOrdID_11
    msg = self.fix.generate_message( OrderedDict([ ('35',  'D'),('11', self.tagClOrdID_11), ('1','S01-00000F00'), ('38', 5),('40', 2), ('44', 52), ('54', 1), ('55', 'AFLT'), ('526',self.tagClOrdID_526 ),  ('386', '1'), ('336', 'EQBR'), ('59', 0) ] ) )
    network_self.send(msg)
    self.processed = True

  def finish_test(self):
    if(True == self.finish):
      #self.network_self.send(self.fix.generate_Logout_35_5())
      self.finished = True
    
  def test(self, msg):
    print('TEST msg = :',msg)
    if ( self.fix.get_tag(msg, 11) == self.tag_11):
      #self.tag_151 = self.tag_151 + int(self.fix.get_tag(msg, 151))
      #if(self.tag_151 == int(self.fix.get_tag(msg, 38))):
      print('TAG 151 = '+self.fix.get_tag(msg, 151))
      if(int(self.fix.get_tag(msg, 151)) == 0):
        self.test_passed = True
        self.finish = True
        print ('TESTS FINISHED')
    pass
    