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


LOGGER = FIX_Log()

hertbeat_interval = 0
##############################################################################################################################

def process_trfix(msg, self = None):
  #time.sleep(1)
  if (fix.get_tag(msg,  35) == '0'):
    msg = fix.generate_message( OrderedDict([ ('35',  '0'), ('49', sender), ('56' , target)]) )
  #elif (fix.get_tag(msg,  35) == '8'):
    #fix.set_LastOrderID_37(fix.get_tag(msg,  37))    
    #print ('TAG 37 = '+fix.get_tag(msg,  37))
    #print ('MSG WAS: '+msg)
  elif (fix.get_tag(msg,  35) == '1'):
    reqId = fix.get_tag(msg,  112) 
    msg = fix.generate_message( OrderedDict([ ('35',  '0'), ('49', sender), ('56' , target), ('112', reqId)]) )
  elif (fix.get_tag(msg,  35) == '5'):
    msg = None
  elif (fix.get_tag(msg,  35) == '4'):
    fix.set_seqNum( fix.get_tag(msg,  36) )
  elif (fix.get_tag(msg,  35) == 'A'):
    tagClOrdID_11 = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
    #msg = fix.generate_message( OrderedDict([ ('35',  'D'), ('11', str(random.randint(100, 1000000))), ('1', 'S01-00000F00'), ('386',  '1'), ('336', 'EQBR'), ('55', 'SBER03'), ('54', 1), ('38', 500), ('40', 2), ('44', 100) , ('111', 100)]) )
    #self.send(msg)
    #time.sleep(2)
    
    #tagClOrdID_11 = str(random.randint(100, 1000000))
    #!!!! Simple Test Worked 35=D Request
    input("\nPress Enter to continue...\n")    
    for i in range (0, 1):
      tagClOrdID_11 = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
      tagClOrdID_526 = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(5))
      tagClOrdID_11_old = tagClOrdID_11
      #msg = fix.generate_message( OrderedDict([ ('35',  'D'),('11', tagClOrdID_11), ('1','S01-00000F00'), ('38', 2),('40', 2), ('44', 76), ('54', 1), ('55', 'SBER'),   ('386', '1'), ('336', 'EQBR'), ('59', 0) ] ) )
      msg = fix.generate_message( OrderedDict([ ('35',  'D'),('11', tagClOrdID_11), ('1','S01-00000F00'), ('38', 10),('40', 2), ('44', 42), ('54', 1), ('55', 'AFLT'), ('526',tagClOrdID_526 ),  ('386', '1'), ('336', 'EQBR'), ('59', 0) ] ) )
      self.send(msg)
      #time.sleep(10)
      #input("\nPress Enter to Continue...\n")    
      #tagClOrdID_11 = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
      #msg = fix.generate_message( OrderedDict([ ('35',  'q'),('11', tagClOrdID_11), ('530',  1 ), ('336', 'EQBR'),('526',tagClOrdID_526 ) ] ) )
      #msg = fix.generate_message( OrderedDict([ ('35',  'q' ),('11', tagClOrdID_11 ), ('530',  7 ) ] ) ) 
      #, ('526', tagClOrdID_526 )
      #self.send(msg)
      
      #msg = fix.generate_message( OrderedDict([ ('35',  'q'),('11', tagClOrdID_11), ('530',  1 ), ('336', 'EQBR'),('526',tagClOrdID_526 ) ] ) )
      #msg = fix.generate_message( OrderedDict([ ('35',  'BE' ), ('11', tagClOrdID_11),('923', tagClOrdID_11 ), ('924',  4 ), ('553', sender), ('554', ' '), ('925', '123456789011') ] ) ) 
      #, ('526', tagClOrdID_526 )
      #self.send(msg)
      
      '''input("\nPress Enter to Cancel...\n")    
      tagOrigClOrdID_41 =  tagClOrdID_11
      tagClOrdID_11 = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
      msg = fix.generate_message( OrderedDict([ ('35',  'F'), ('41',tagOrigClOrdID_41 ), ('11', tagClOrdID_11), ('54', 2), ('60', fix.getLastSendingTime())]) )
      self.send(msg)
      input("\nPress Enter to continue...\n")    '''
    
    #EQBS
    #tagClOrdID_11 = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
    #msg = fix.generate_message( OrderedDict([ ('35',  'D'),('11', tagClOrdID_11), ('1','S01-00000F00'), ('38', 2),('40', 2), ('44', 101), ('54', 1), ('55', 'UTEL'),   ('386', '1'), ('336', 'EQBS'), ('59', 0) ] ) )
    #self.send(msg)
    
    #EQNE
    #tagClOrdID_11 = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
    #msg = fix.generate_message( OrderedDict([ ('35',  'D'),('11', tagClOrdID_11), ('1','S01-00000F00'), ('38', 2),('40', 2), ('44', 338.5), ('54', 1), ('55', 'PMNGP'),   ('386', '1'), ('336', 'EQNE'), ('59', 0) ] ) )
    #self.send(msg)
    
    #tagClOrdID_11 = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
    #msg = fix.generate_message( OrderedDict([ ('35',  'D'),('11', tagClOrdID_11), ('1','S01-00000F00'), ('38', 10),('40', 2), ('44', 1.5569), ('54', 1), ('55', 'URSI'),   ('386', '1'), ('336', 'EQBR'), ('59', 0) ] ) )
    #self.send(msg)
    #time.sleep(3)
    #tagClOrdID_11 = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
    #msg = fix.generate_message( OrderedDict([ ('35',  'D'),('11', tagClOrdID_11), ('1','S01-00000F00'), ('38', 2),('40', 20), ('44', 101), ('54', 1), ('55', 'SBER'),   ('386', '1'), ('336', 'EQBR'), ('59', 0) ] ) )
    #self.send(msg)
    '''tagClOrdID_11 = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
    msg = fix.generate_message( OrderedDict([ ('35',  'D'),('11', tagClOrdID_11), ('1','S01-00000F00'), ('38', 10),('40', 2), ('44', 32.795), ('54', 1), ('55', 'SPTL'),   ('386', '1'), ('336', 'EQBR'), ('59', 0) ] ) )
    self.send(msg)'''
    '''tagClOrdID_11 = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
    msg = fix.generate_message( OrderedDict([ ('35',  'D'),('11', tagClOrdID_11), ('1','S01-00000F00'), ('38', 10),('40', 2), ('44', 75), ('54', 1), ('55', 'AFLT'),   ('386', '1'), ('336', 'EQBR'), ('59', 0) ] ) )
    self.send(msg)'''
    '''input("\nPress Enter to continue...\n")
    tagClOrdID_11 = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
    msg = fix.generate_message( OrderedDict([ ('35',  'D'),('11', tagClOrdID_11), ('1','S01-00000F00'), ('38', 20),('40', 2), ('44', 2001), ('54', 1), ('55', 'LKOH'),   ('386', '1'), ('336', 'EQBR'), ('59', 0) ] ) )          
    self.send(msg)'''
    '''input("\nPress Enter to continue...\n")
    tagClOrdID_11 = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
    msg = fix.generate_message( OrderedDict([ ('35',  'D'),('11', tagClOrdID_11), ('1','S01-00000F00'), ('38', 20),('40', 2), ('44', 3.86), ('54', 1), ('55', 'MSNG'),   ('386', '1'), ('336', 'EQBR'), ('59', 0) ] ) )
    self.send(msg)
    tagClOrdID_11 = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))'''
    '''msg = fix.generate_message( OrderedDict([ ('35',  'D'),('11', tagClOrdID_11), ('1','S01-00000F00'), ('38', 20),('40', 2), ('44', 30.6), ('54', 1), ('55', 'IRGZ'),   ('386', '1'), ('336', 'EQBR'), ('59', 0) ] ) )          
    self.send(msg)'''
    '''tagClOrdID_11 = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
    msg = fix.generate_message( OrderedDict([ ('35',  'D'),('11', tagClOrdID_11), ('1','S01-00000F00'), ('38', 1000),('40', 2), ('44', 120), ('54', 1), ('55', 'RTKM'),   ('386', '1'), ('336', 'EQBR'), ('59', 0) ] ) )          
    self.send(msg)'''
    #Dark Pool
    #tagClOrdID_11 = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
    #msg = fix.generate_message( OrderedDict([ ('35',  'D'),('11', tagClOrdID_11), ('1','S01-00000F00'), ('38', 15175),('40', 2), ('44', 100.85), ('54', 1), ('55', 'SBER'), ('386', '1'), ('336', 'EQBR'), ('625', 'D'), ('59', 0) ] ) )      
    #msg = fix.generate_message( OrderedDict([ ('35',  'D'),('11', tagClOrdID_11), ('1','S01-00000F00'), ('38', 20),('40', 1), ('54', 1), ('55', 'IRGZ'),   ('386', '1'), ('336', 'EQBR'), ('59', 0) ] ) )          
    #self.send(msg)
    
    #for i in range (1):
      #tagClOrdID_11 = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
      #msg = fix.generate_message( OrderedDict([ ('35',  'D'),('11', tagClOrdID_11), ('1','S01-00000F00'), ('38', 2),('40', 2), ('44', 2381), ('54', 1), ('55', 'LKOH'),   ('386', '1'), ('336', 'EQBR'), ('59', 0) ] ) )      
      #self.send(msg)
      
      #t_msg = '8=FIX.4.4^A9=182^A35=D^A49=MU0055600001^A56=MFIXTradeID^A34=583^A52=20111215-14:52:19^A1=S01-00000F00^A423=2^A386=1^A336=EQDP^A60=20111215-14:52:19^A40=2^A11=A14002825012150081^A54=1^A44=171^A55=GAZP^A38=10000^A59=0^A10=130^A'
      #self.send(fix.parce(t_msg,'^A'))
      #time.sleep(10)
    '''for i in range(0, 1000):
      tagClOrdID_11 = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
      msg = fix.generate_message( OrderedDict([ ('35',  'D'),('11', tagClOrdID_11), ('1','S01-00000F00'), ('38', 10),('40', 2), ('44', 53), ('54', 1), ('55', 'SBERP03'),   ('386', '1'), ('336', 'EQBR'), ('59', 0) ] ) )
      self.send(msg)
      time.sleep(0.5)
      tagClOrdID_11 = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
      msg = fix.generate_message( OrderedDict([ ('35',  'D'),('11', tagClOrdID_11), ('1','S01-00000F00'), ('38', 10),('40', 2), ('44', 53), ('54', 2), ('55', 'SBERP03'),   ('386', '1'), ('336', 'EQBR'), ('59', 0) ] ) )
      self.send(msg)      '''
    '''tagClOrdID_11 = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
    msg = fix.generate_message( OrderedDict([ ('35',  'D'),('11', tagClOrdID_11), ('1','S01-00000F00'), ('38', 10),('40', 2), ('44', 53), ('54', 2), ('55', 'SBERP03'),   ('386', '1'), ('336', 'EQBR'), ('59', 0) ] ) )
    self.send(msg)'''
    
    
    #tagClOrdID_11 = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
    #msg = fix.generate_message( OrderedDict([ ('35',  'D'),('11', tagClOrdID_11), ('1','S01-00000F00'), ('423', 2), ('38',10000), ('40', 2), ('44', 171), ('54', 1), ('55', 'GAZP'),  ('386', '1'), ('336', 'EQDP'), ('59', 0) ] ) )
    #self.send(msg)
    #time.sleep(3)
    #8=FIX.4.49=17435=D49=MU005700000156=MFIXTradeID34=252=20111216-09:47:321=S01-00000F00423=2386=1336=EQDP60=20111215-14:52:1940=211=EI5C31RMO6 54=144=17155=GAZP38=1000059=010=013
    #t_msg = '8=FIX.4.4^A9=182^A35=D^A49=MU0055600001^A56=MFIXTradeID^A34=583^A52=20111215-14:52:19^A1=S01-00000F00^A423=2^A386=1^A336=EQDP^A60=20111215-14:52:19^A40=2^A11=A14002825012150081^A54=1^A44=171^A55=GAZP^A38=10000^A59=0^A10=130^A'
    #self.send(fix.parce(t_msg,'^A'))
    '''for i in range(0, 25):
      tagClOrdID_11 = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
      tagClOrdID_11_1 = tagClOrdID_11
      msg = fix.generate_message( OrderedDict([ ('35',  'D'),('11', tagClOrdID_11), ('1','S01-00000F00'), ('38', 50),('40', 2), ('44', 2001), ('54', 2), ('55', 'LKOH'),   ('386', '1'), ('336', 'EQBR'), ('59', 0) ] ) )
      self.send(msg)      
      time.sleep(3)      
      #input("\nPress Enter to continue...\n")
      msg = fix.generate_message( OrderedDict([ ('35',  'F'), ('41',tagClOrdID_11_1 ), ('11', ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))), ('54', 2), ('60', fix.getLastSendingTime())]) )
      #msg = fix.generate_message( OrderedDict([ ('35',  'F'), ('41', '61L54GSTDL'), ('11', tagClOrdID_11), ('54', 2), ('60', fix.getLastSendingTime())]) )
      self.send(msg)
      #time.sleep(0.1)    '''
    
    '''tagClOrdID_11 = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
    msg = fix.generate_message( OrderedDict([ ('35',  'D'),('11', tagClOrdID_11), ('1','S01-00000F00'), ('38', 10),('40', 2), ('44', 2080), ('54', 2), ('55', 'LKOH'),   ('386', '1'), ('336', 'EQBR'), ('59', 0) ] ) )
    self.send(msg)
    
    time.sleep(1)
    input("\nPress Enter to continue...\n")
    
    msg = fix.generate_message( OrderedDict([ ('35',  'F'), ('41',tagClOrdID_11 ), ('11', ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))), ('54', 2), ('60', fix.getLastSendingTime())]) )
    #msg = fix.generate_message( OrderedDict([ ('35',  'F'), ('41', '61L54GSTDL'), ('11', tagClOrdID_11), ('54', 2), ('60', fix.getLastSendingTime())]) )
    self.send(msg)
    time.sleep(3)
    input("\nPress Enter to continue...\n")
    msg = fix.generate_message( OrderedDict([ ('35',  'F'), ('41',tagClOrdID_11_1 ), ('11', ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))), ('54', 2), ('60', fix.getLastSendingTime())]) )
    #msg = fix.generate_message( OrderedDict([ ('35',  'F'), ('41', '61L54GSTDL'), ('11', tagClOrdID_11), ('54', 2), ('60', fix.getLastSendingTime())]) )
    self.send(msg)
    input("\nPress Enter to continue...\n")'''
    
    
    #iceberg
    '''tagClOrdID_11 = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
    msg = fix.generate_message( OrderedDict([ ('35',  'D'),('11', tagClOrdID_11), ('1','S01-00000F00'), ('38', 100),('40', 2), ('44', 76), ('111', 40), ('54', 2), ('55', 'SBER'),   ('386', '1'), ('336', 'EQBR'), ('59', 0) ] ) )
    self.send(msg)'''
    
    '''for i in range (1):
      tagClOrdID_11 = ''.join(random.choice(string.digits) for x in range(4))
      tagClOrdID_11 = tagClOrdID_11+'_'
      tagClOrdID_11 = tagClOrdID_11+''.join(random.choice(string.digits) for x in range(2))    
      tagClOrdID_11 = tagClOrdID_11+'_'
      tagClOrdID_11 = tagClOrdID_11+''.join(random.choice(string.digits) for x in range(1))
      tagClOrdID_11 = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
      FIX44.date_long_encode(self,  datetime.now())
      msg = fix.generate_message( OrderedDict([ ('35',  'D'),('11', tagClOrdID_11), ('1','S01-00000F00'), ('38', 1),('40', 2), ('44', '1720.00000'), ('54', 1), ('55', 'LKOH'), ('60', FIX44.date_long_encode(self,  datetime.now())), ('386', '1'), ('336', 'EQBR'), ('59', 0) ] ) )
      self.send(msg)
      #time.sleep(random.randint(5, 5))
      #time.sleep(20)'''
    '''tagClOrdID_11_2 = ''.join(random.choice(string.digits) for x in range(4))
      tagClOrdID_11_2 = tagClOrdID_11+'_'
      tagClOrdID_11_2 = tagClOrdID_11+''.join(random.choice(string.digits) for x in range(2))    
      tagClOrdID_11_2 = tagClOrdID_11+'_'
      tagClOrdID_11_2 = tagClOrdID_11+''.join(random.choice(string.digits) for x in range(1))
      #input("\nPress Enter to continue...\n")    
      msg = fix.generate_message( OrderedDict([ ('35',  'F'), ('41',tagClOrdID_11 ), ('11', tagClOrdID_11_2), ('54', 1), ('60', fix.getLastSendingTime())]) )    
      msg = fix.generate_message( OrderedDict([ ('35',  'F'), ('37',fix.set_LastOrderID_37()), ('11', ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))), ('54', 1), ('60', fix.getLastSendingTime())]) )      
      self.send(msg)'''    
    
    '''msgs_list = fix.get_fix_messages_from_file('MFIXTradeID-MU0005500003_09300651508381.in', split_symbol = FIX44.SOH)
    print(msgs_list)
    for msgs_item in msgs_list:
      print ('ITEM: '+str(msgs_item))
      msgs_item = fix.parce(msgs_item)
      self.send(msg)
      time.sleep(2)
    '''
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
    main()
