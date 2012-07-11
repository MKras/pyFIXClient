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
class Base_Case:

  def __init__(self):    
    pass
  def processor(self, msg, connection = None):
    pass
  def finish_test(self):
    if(True == self.finish):
      msg = self.fix.generate_Logout_35_5()
      self.connection.send(msg)
      self.finished = True
  
  def test(self, msg):
    pass
  def go_on(self, connection = None):
    raise Exception("Method go_on() is not redefined!")

  def process(self, msg, connection = None):
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
      return self.processor(msg, connection)
      msg=None
    else:
      msg = None
    return msg
  
  def get_network(self):
    if(self.connection is None):
      raise Exception("connection not defined in", self.__mane__)
    return self.connection
  


class Case_1(Base_Case):
  def __init__(self, fix):
    self.fix = fix 
    self.test_passed = False
    self.finish = False
    self.finished = False
    self.tag_151 = -1
    pass
    
  def processor(self, msg, connection = None):
    self.connection = connection
    #input("\nPress Enter to continue...\n")
    self.tagClOrdID_11 = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
    self.tag_11 = self.tagClOrdID_11
    self.tagClOrdID_526 = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(5))
    self.tagClOrdID_11_old = self.tagClOrdID_11
    msg = self.fix.generate_message( OrderedDict([ ('35',  'D'),('11', self.tagClOrdID_11), ('1','S01-00000F00'), ('38', 5),('40', 2), ('44', 52), ('54', 1), ('55', 'AFLT'), ('526',self.tagClOrdID_526 ),  ('386', '1'), ('336', 'EQBR'), ('59', 0) ] ) )
    self.connection.send(msg)

  def go_on(self, connection = None):
    pass
    
  def finish_test(self):
    if(True == self.finish):
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

class Case_2(Base_Case):
  def __init__(self, fix):
    self.fix = fix 
    self.test_passed = False
    self.finish = False
    self.finished = False
    self.tag_151 = -1
    pass
    
  def processor(self, msg, connection = None):
    pass

  def go_on(self, connection = None):
    self.connection = connection
    #input("\nPress Enter to continue...\n")
    self.tagClOrdID_11 = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
    self.tag_11 = self.tagClOrdID_11
    self.tagClOrdID_526 = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(5))
    self.tagClOrdID_11_old = self.tagClOrdID_11
    msg = self.fix.generate_message( OrderedDict([ ('35',  'D'),('11', self.tagClOrdID_11), ('1','S01-00000F00'), ('38', 5),('40', 2), ('44', 52), ('54', 1), ('55', 'LKOH'), ('526',self.tagClOrdID_526 ),  ('386', '1'), ('336', 'EQBR'), ('59', 0) ] ) )
    self.connection.send(msg)
    
  def finish_test(self):
    if(True == self.finish):
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