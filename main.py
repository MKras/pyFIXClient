#!/usr/bin/env python3

from collections import OrderedDict
from datetime import datetime, date
from fix.fix44  import  FIX44
from fix.log  import  FIX_Log
from fix.network  import  Client  
from cfg import app, host, port, sender, target, password
import random
import time
import sys
import string
import threading,  _thread
from threading import Thread, Lock

LOGGER = FIX_Log()

hertbeat_interval = 0
##############################################################################################################################
def process_trcap(msg, self = None):
  #time.sleep(1)
  if (fix.get_tag(msg,  35) == '0'):
    msg = fix.generate_message( OrderedDict([ ('35',  '0'), ('49', sender), ('56' , target)]) )
  elif (fix.get_tag(msg,  35) == '1'):
    reqId = fix.get_tag(msg,  112) 
    msg = fix.generate_message( OrderedDict([ ('35',  '0'), ('49', sender), ('56' , target), ('112', reqId)]) )
  elif (fix.get_tag(msg,  35) == '5'):
    msg = None
  elif (fix.get_tag(msg,  35) == '4'):
    fix.set_seqNum( fix.get_tag(msg,  36) )
  elif (fix.get_tag(msg,  35) == '5'):
    print ('Logout trecieved. I will Exit!')
    sys.exit(0)
  elif (fix.get_tag(msg,  35) == 'A'):    
    #msg = fix.generate_message( OrderedDict([ ('35',  'AD'), ('568', '555' ), ('569', '0'), ('263',  '1') ]) )
    #8=FIX.4.4^9=105^35=AD^49=MU0055600003^56=MFIXTradeCaptureID^34=3^52=20110711-16:41:58^568=20110711-17:41:583^569=0^263=1^10
    #20110811-14:30:12.964 : 8=FIX.4.49=10235=AD49=MU009370038256=MFIXTradeCaptureID34=352=20110811-14:30:13568=201108111530133569=0263=110=148
    #msg = fix.generate_message( OrderedDict([ ('35',  'AD'), ('568', '2907363150' ), ('569', '0'), ('263',  '1') ]) )
    #@network.say Fix::generate_message({ 35 => "AD", 568=> "555", 569=> "0",  263=> "1"})#, 44=>"27.270000" })
    msg = fix.generate_message( OrderedDict([ ('35',  'AD'), ('568', '555' ), ('569', '0'), ('263',  '1') ]) )    
    #msg = fix.generate_message( OrderedDict([ ('35',  'AD'), ('568', '555' ), ('569', '0'), ('263',  '1') ]) )
    #time.sleep(3)
    #msg = fix.generate_message( OrderedDict([ ('35',  'AD'), ('568', '434857' ), ('569', '0'), ('263',  '1') ]) )
    self.send(msg)
    #msg = fix.generate_message( OrderedDict([ ('35',  'AD'), ('568', '444' ), ('569', '0'), ('263',  '1') ]) )
    #self.send(msg)
    #time.sleep(15)
    #logout_msg =fix.generate_message ( OrderedDict([('35',  '5'), ('49', sender), ('56' , target)]) )
    #logout_msg =fix.generate_Logout_35_5()
    #self.send(logout_msg)    
    msg=None
  else:
    msg = None
  return msg


#@network.say Micex::generate_35_D( cl_ord_id_1, "S01-00000F00", "EQBR", "SBER03", 2, 2 , 125, 800, {111=>150} )
##############################################################################################################################
#@synchronized(myLock)
def process_trfix(msg, self = None):
  #time.sleep(1)
  if (fix.get_tag(msg,  35) == '0'):
    msg = fix.generate_message( OrderedDict([ ('35',  '0'), ('49', sender), ('56' , target)]) )
  elif (fix.get_tag(msg,  35) == '1'):
    reqId = fix.get_tag(msg,  112) 
    msg = fix.generate_message( OrderedDict([ ('35',  '0'), ('49', sender), ('56' , target), ('112', reqId)]) )
  elif (fix.get_tag(msg,  35) == '5'):
    msg = None
  elif (fix.get_tag(msg,  35) == '4'):
    fix.set_seqNum( fix.get_tag(msg,  36) )
  elif (fix.get_tag(msg,  35) == 'A'):
    #msg = fix.generate_message( OrderedDict([ ('35',  'D'), ('11', str(random.randint(100, 1000000))), ('1', 'S01-00000F00'), ('386',  '1'), ('336', 'EQBR'), ('55', 'SBER03'), ('54', 1), ('38', 500), ('40', 2), ('44', 100) , ('111', 100)]) )
    #self.send(msg)
    #time.sleep(2)
    
    #tagClOrdID_11 = str(random.randint(100, 1000000))
    tagClOrdID_11 = tagClOrdID_11 = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
    #!!!! Simple Test Worked 35=D Request
    #input("\nPress Enter to continue...\n")
    msg = fix.generate_message( OrderedDict([ ('35',  'D'),('11', tagClOrdID_11), ('1','S01-00000F00'), ('38', 20000),('40', 2), ('44', 2386), ('54', 1), ('55', 'LKOH'),   ('386', '1'), ('336', 'EQBR'), ('59', 0) ] ) )
    self.send(msg)
    
   
    '''for i in range(0, 100):
      msg = fix.generate_message( OrderedDict([ ('35',  'D'),('11', tagClOrdID_11), ('1','S01-00000F00'), ('38', 2000),('40', 2), ('44', 2386), ('54', 2), ('55', 'LKOH'),   ('386', '1'), ('336', 'EQBR'), ('59', 3) ] ) )
      self.send(msg)
      time.sleep(0.15)
      msg = fix.generate_message( OrderedDict([ ('35',  'F'), ('41', tagClOrdID_11), ('11', str(random.randint(100, 1000000))), ('54', 2), ('60', fix.getLastSendingTime())]) )
      self.send(msg)'''
    #iceberg
    #@network.say Micex::generate_35_D( cl_ord_id_1, "S01-00000F00", "EQBR", "SBER03", 2, 2 , 125, 800, {111=>300} )
    #8=FIX.4.49=17535=D49=MU005700000156=MFIXTradeID34=252=20110624-10:35:3811=5429627202641=S01-00000F00386=1336=EQBR55=SBER0354=160=20110624-10:35:38.00038=35040=244=100111=15010=040
    #msg = fix.generate_message( OrderedDict([ ('35',  'D'),('11', tagClOrdID_11), ('1','S01-00000F00'), ('386', '1'), ('336', 'EQBR'), ('55', 'SBER03'),('54', 2),('38', 350),('40', 2), ('44', 100) ] ) )
    
    #time.sleep(15)  
    #input("\nPress Enter to continue...\n")
    
    #Send: 8=FIX.4.4, 9=0109, 35=F, 49=MU0059100002, 56=MFIXTradeID, 34=000000495, 52=20110729-16:10:11.726, 11=4, 41=3, 60=20110729-16:10:11.726, 10=156,
    #msg = fix.generate_message( OrderedDict([ ('35',  'F'), ('41', tagClOrdID_11), ('11', str(random.randint(100, 1000000))), ('54', 2), ('60', fix.getLastSendingTime())]) )
    #, ('60', fix.getLastSendingTime())
    #self.send(msg)
    #20110817-08:37:25.231 : 8=FIX.4.49=013535=F49=MD805830018656=MFIXTradeIDCurr34=00000104652=20110817-08:35:54.25111=SESELT1//91641=SESELT1//87960=20110817-08:35:54.25110=224

    #time.sleep(90)
    '''for i in range (1,12):
      msg = fix.generate_message( OrderedDict([ ('35',  'F'), ('41', tagClOrdID_11), ('11', 'SESELT1//'+str(i)), ('54', 2), ('60', fix.getLastSendingTime())]) )
      self.send(msg)  '''
    
    #msg = fix.generate_message( OrderedDict([ ('35',  'F'), ('41', 563844), ('11', tagClOrdID_11), ('54', 2), ('60', fix.getLastSendingTime())]) )
    #msg = fix.generate_message( OrderedDict([ ('35',  'F'), ('41', 2885719910), ('11', tagClOrdID_11), ('54', 2), ('60', fix.getLastSendingTime())]) )
    #self.send(msg)

    #time.sleep(30)
    
    #logout_msg =fix.generate_Logout_35_5()
    #self.send(logout_msg)
    msg=None
  else:
    msg = None
  return msg
##############################################################################################################################

##############################################################################################################################
def process_mdfix(msg, self = None):
  #time.sleep(1)
  if (fix.get_tag(msg,  35) == '0'):
    msg = fix.generate_message( OrderedDict([ ('35',  '0'), ('49', sender), ('56' , target)]) )
  elif (fix.get_tag(msg,  35) == '1'):
    reqId = fix.get_tag(msg,  112) 
    msg = fix.generate_message( OrderedDict([ ('35',  '0'), ('49', sender), ('56' , target), ('112', reqId)]) )
  elif (fix.get_tag(msg,  35) == '5'):
    msg = None
  elif (fix.get_tag(msg,  35) == '4'):
    fix.set_seqNum( fix.get_tag(msg,  36) )
  elif (fix.get_tag(msg,  35) == '5'):
    print ('Logout trecieved. I will Exit!')
    sys.exit(0)
  elif (fix.get_tag(msg,  35) == 'A'):    
    #msg = fix.generate_message( OrderedDict([ ('35',  'AD'), ('568', '555' ), ('569', '0'), ('263',  '1') ]) )
    #8=FIX.4.4^9=105^35=AD^49=MU0055600003^56=MFIXTradeCaptureID^34=3^52=20110711-16:41:58^568=20110711-17:41:583^569=0^263=1^10
    msg = fix.generate_message( OrderedDict([ ('35',  'AD'), ('568', '20110711-17:41:583' ), ('569', '0'), ('263',  '1') ]) )
    self.send(msg)
    #msg = fix.generate_message( OrderedDict([ ('35',  'AD'), ('568', '444' ), ('569', '0'), ('263',  '1') ]) )
    #self.send(msg)
    #time.sleep(15)
    #logout_msg =fix.generate_message ( OrderedDict([('35',  '5'), ('49', sender), ('56' , target)]) )
    #logout_msg =fix.generate_Logout_35_5()
    #self.send(logout_msg)    
    msg=None
  else:
    msg = None
  return msg
  
##############################################################################################################################

if app == 'trfix':
  process = process_trfix

if app == 'trcap':
  process = process_trcap
if app == 'mdfix':
  process = process_mdfix

fix=FIX44()
fix.init(sender , target )
logon_msg = fix.generate_Login_35_A(0, ' ',OrderedDict([ ('98', 0), ('141', 'N')]) )

#fix_trfix=FIX44()
#fix_trfix.init('MU0057000002' , target )
#logon_msg_trfix = fix_trfix.generate_Login_35_A(0, ' ',OrderedDict([ ('98', 0), ('141', 'N')]) )
#fix_msg='8=FIX.4.4^9=105^35=AD^49=MU0055600003^56=MFIXTradeCaptureID^34=3^52=20110711-16:41:58^568=20110711-17:41:583^569=0^263=1^10'
#fix.parce(fix_msg)
#print (fix_msg)
#print("Exiting!!!!")
#time.sleep(15)
#sys.exit(0)
##############################################################################################################################


def main():
    cl = Client(host, port,  process)
    cl.send(logon_msg)  
    
#    time.sleep(20)
#    cl_trfix = Client(host, port,  process_trfix)
#    cl_trfix.send(logon_msg_trfix)  



if __name__ == '__main__':
    main()
