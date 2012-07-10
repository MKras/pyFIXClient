#!/usr/bin/env python3

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
import unittest


LOGGER = FIX_Log()

hertbeat_interval = 0
###############################################################################################################################
class TestSequenceFunctions(unittest.TestCase):
  def setUp(self):
    main();
    

##############################################################################################################################

def process_trfix(msg, self = None):
  tagClOrdID_11 = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
  #time.sleep(1)
  if (fix.get_tag(msg,  35) == '0'):
    msg = fix.generate_message( OrderedDict([ ('35',  '0'), ('49', sender), ('56' , target)]) )
  elif (fix.get_tag(msg,  35) == '8'):
    #fix.set_LastOrderID_37(fix.get_tag(msg,  37))    
    print ('TAG 37 = '+fix.get_tag(msg,  37))
    print ('MSG WAS: '+msg)
  elif (fix.get_tag(msg,  35) == '1'):
    reqId = fix.get_tag(msg,  112) 
    msg = fix.generate_message( OrderedDict([ ('35',  '0'), ('49', sender), ('56' , target), ('112', reqId)]) )
  elif (fix.get_tag(msg,  35) == '5'):
    msg = None
  elif (fix.get_tag(msg,  35) == '4'):
    fix.set_seqNum( fix.get_tag(msg,  36) )
  elif (fix.get_tag(msg,  35) == 'A'):
    tagClOrdID_11 = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
    #!!!! Simple Test Worked 35=D Request
    input("\nPress Enter to continue...\n")    
    for i in range (0, 1):      
      tagClOrdID_526 = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(5))
      tagClOrdID_11_old = tagClOrdID_11
      #msg = fix.generate_message( OrderedDict([ ('35',  'D'),('11', tagClOrdID_11), ('1','S01-00000F00'), ('38', 2),('40', 2), ('44', 76), ('54', 1), ('55', 'SBER'),   ('386', '1'), ('336', 'EQBR'), ('59', 0) ] ) )
      msg = fix.generate_message( OrderedDict([ ('35',  'D'),('11', tagClOrdID_11), ('1','S01-00000F00'), ('38', 150),('40', 2), ('44', 42), ('54', 1), ('55', 'AFLT'), ('526',tagClOrdID_526 ),  ('386', '1'), ('336', 'EQBR'), ('59', 0) ] ) )
      self.send(msg)

    time.sleep(5)    
    input("\nPress Enter to Logout...\n")
    self.send(fix.generate_Logout_35_5())

    #time.sleep(30)
    
    #logout_msg =fix.generate_Logout_35_5()
    #self.send(logout_msg)
    msg=None
  else:
    msg = None
  return msg
##############################################################################################################################

process = process_trfix


fix=FIX44()
fix.init(sender , target )
#logon_msg = fix.generate_Login_35_A(0, password,OrderedDict([ ('98', 0), ('141', 'N'),('554', ' '), ('925', 'newpass')]) )
logon_msg = fix.generate_Login_35_A(0, password,OrderedDict([ ('98', 0), ('141', 'Y')]) )

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
    cl = Client(host, port,  process)
    cl.send(logon_msg)  



if __name__ == '__main__':
    unittest.main()