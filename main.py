#!/usr/bin/env python3

from collections import OrderedDict
import sys
from datetime import datetime, date
from fix.fix44  import  FIX44
from fix.log  import  FIX_Log
from fix.network  import  Client  
import random
import time
import threading,  _thread
from threading import Thread, Lock

LOGGER = FIX_Log()

#hostname = '194.84.44.1' #telis
#hostname = 'evbyminsd0991' #evbyminsd0991
#hostname = '10.6.17.70'  #build machene
hostname = '127.0.0.1'  #local
#hostname = '194.84.44.42'  #robot

#self.thr_proc = threading.Thread(target=self.process, args=(self.data.decode('CP1251'),)).start() 

def threading_deco():
    ''' Threading decorator. '''

    def wrap(f,*args, **kw):
        thr_proc = threading.Thread(target=f, args=(args,)).start()
        '''def newFunction(*args, **kw):
            thr_proc = threading.Thread(target=f, args=(args,)).start()
            return thr_proc
        return newFunction'''
    return wrap
    
def synchronized(lock):
    ''' Synchronization decorator. '''

    def wrap(f):
        def newFunction(*args, **kw):
            lock.acquire()
            try:
                return f(*args, **kw)
   
            finally:
                lock.release()
        return newFunction
    return wrap
    
myLock = Lock()

app='trfix'
#app='trcap'
#app='mdfix'

if app == 'trfix':
  host = hostname
  port = 9120 
  target = 'MFIXTradeID'
if app == 'trcap':
  host = hostname
  port = 9121
  target = 'MFIXTradeCaptureID'
if app == 'mdfix':
  host = hostname
  port = 9111
  target = 'MicexFixBridge'
  
  
hertbeat_interval = 0

if hostname == '194.84.44.1': # telis
  sender = 'MU0059000001'
  if app == 'mdfix':
    sender = 'Test001'

if hostname == '194.84.44.42': # robot
  sender = 'MD8058300164'
  if app == 'mdfix':
    sender = 'Test001'

if hostname == '10.6.17.70': #build machene
  sender = 'MU0057000001'  
  if app == 'mdfix':
    sender = 'Test001'

if hostname == '127.0.0.1': #local
  sender = 'MU0057000001' 
  if app == 'mdfix':
    sender = 'Test001'

if hostname == 'evbyminsd0991': #local  
  sender = 'MU0057000001'  
  if app == 'mdfix':
    sender = 'Test001'


#port = 9001
#sender = 'MD0154300001'
#sender = 'MD0004400002'
#target = 'MFIXTradeID'


##!!!!!
#sender = 'Test001'


#sender = 'MU0057000001'
#sender = 'MU0059000002' # telis
#sender = 'MU0000800002' # telis

#sender = 'MU0059000001' # for telis
#sender = 'MU0057000002' # telis


password=' '

#sys.exit(0)
##############################################################################################################################
def process_trcap(msg,  self = None):
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
    #msg = fix.generate_message( OrderedDict([ ('35',  'AD'), ('568', '201108111530133' ), ('569', '0'), ('263',  '1') ]) )
    msg = fix.generate_message( OrderedDict([ ('35',  'AD'), ('568', '556' ), ('569', '0'), ('263',  '1') ]) )
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
def process_trfix(msg,  self = None):
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
    
    tagClOrdID_11 = str(random.randint(100, 1000000))
    #msg = fix.generate_message( OrderedDict([ ('35',  'D'), ('11', tagClOrdID_11), ('1', 'S01-00000F00'), ('386',  '1'), ('336', 'EQBR'), ('55', 'SBER03'), ('54', 2), ('38', 500000), ('40', 1), ('44', 0) , ('111', 500000)]) )
    #self.send(msg)    
    #msg = fix.generate_message( OrderedDict([ ('35',  'D'), ('11', str(random.randint(100, 1000000))), ('1', 'S01-00000F00'), ('386',  '1'), ('336', 'EQBR'), ('55', 'SBER03'), ('54', 2), ('38', 1000), ('40', 2), ('44', 100) , ('111', 100)]) )
    #msg = fix.generate_message( OrderedDict([ ('35',  'D'), ('11', str(random.randint(100, 1000000))), ('1', 'S01-00000F00'), ('386',  '1'), ('336', 'EQBR'), ('55', 'SBER03'), ('54', 1), ('38', 200), ('40', 2), ('44', 100) , ('111', 50)]) )
    #self.send(msg)
    #time.sleep(15)    
    #msg = fix.generate_message( OrderedDict([ ('35',  'D'), ('1', 'S01-00000F00'),('423','2'),('386', '1'), ('336', '1'), ('60', FIX44.date_long_encode(self,  datetime.now())),('40', 2),('11', 'A14001015907120091') ,('54', 2),('44',30), ('55', 'SNGS'),('38', 10), ('59', 0)]) )
    #msg = fix.generate_message( OrderedDict([ ('35',  'D'), ('54', 1), ('55', 'EUR/JPY'),('11', tagClOrdID_11),('38', 1000000),('40', 1), ('59', 0), ('167', 'FOR'), ('60', '20110711-15:51:13'), ('15', 'EUR'), ('386', '1'), ('336', '1')]) )    
    #self.send(msg)
    
    #msg = fix.generate_message( OrderedDict([ ('35',  'F'), ('41', tagClOrdID_11), ('11', str(random.randint(100, 1000000))), ('54', 2), ('60', fix.getLastSendingTime()),('38', 800)]) )
    
    #Send: 8=FIX.4.4, 9=0172, 35=D, 49=MU0059100002, 56=MFIXTradeID, 34=000000494, 52=20110729-16:09:58.943, 11=3, 55=GAZP, 54=2, 38=10, 1=S01-00000F00, 386=1, 336=EQNE, 40=2, 44=195.5, 59=3, 60=20110729-16:09:58.943, 10=251,
    #msg = fix.generate_message( OrderedDict([ ('35',  'D'),('11', tagClOrdID_11), ('55', 'GAZP'), ('54', 2),('38', 1000), ('1','S01-00000F00'), ('386', '1'), ('336', 'EQNE'), ('40', 2), ('44', 195.5), ('59', 3) ] ) )
    #, ('60', fix.getLastSendingTime()) 
    #20110801-12:18:17.268 : 8=FIX.4.4.9=168.35=D.34=7.49=MU0000800002.52=20110801-12:18:17.370.56=MFIXTradeID.1=S01-00000F00.11=16150_2.38=2000.40=2.44=19100.54=1.55=LKOH.59=3.60=20110801-12:18:17.386=1.336=EQBR.10=248.
    #msg = fix.generate_message( OrderedDict([ ('35',  'D'),('11', tagClOrdID_11), ('1','S01-00000F00'), ('38', 2000),('40', 2), ('44', 19100), ('54', 2), ('55', 'LKOH'),   ('386', '1'), ('336', 'EQBR'), ('59', 3) ] ) )
    #iceberg
    #@network.say Micex::generate_35_D( cl_ord_id_1, "S01-00000F00", "EQBR", "SBER03", 2, 2 , 125, 800, {111=>300} )
    #8=FIX.4.49=17535=D49=MU005700000156=MFIXTradeID34=252=20110624-10:35:3811=5429627202641=S01-00000F00386=1336=EQBR55=SBER0354=160=20110624-10:35:38.00038=35040=244=100111=15010=040
    #msg = fix.generate_message( OrderedDict([ ('35',  'D'),('11', tagClOrdID_11), ('1','S01-00000F00'), ('386', '1'), ('336', 'EQBR'), ('55', 'SBER03'),('54', 2),('38', 350),('40', 2), ('44', 100) ] ) )
    #msg = fix.generate_message( OrderedDict([ ('35',  'D'),('11', '556'), ('1','S01-00000F00'), ('386', '1'), ('336', 'EQBR'), ('55', 'SBER03'),('54', 2),('38', 2000),('40', 2), ('44', 100) ] ) )
    
    #msg = fix.generate_message( OrderedDict([ ('35',  'D'),('11', 'TSESELT1//890'), ('1','S01-00000F00'), ('38', 1000),('40', 2), ('44', 1910), ('54', 1), ('55', 'LKOH'),   ('386', '1'), ('336', 'EQBR'), ('59', 3) ] ) )
    #55=USD000000TOD.54=1.38=1.1=MB00134CURR0.386=1.336=CETS.40=2.44=30.5.59=0.60=20110801-13:05:49.288.10=038.
    #time.sleep(15)  
    #input("\nPress Enter to continue...\n")
    
    #Send: 8=FIX.4.4, 9=0109, 35=F, 49=MU0059100002, 56=MFIXTradeID, 34=000000495, 52=20110729-16:10:11.726, 11=4, 41=3, 60=20110729-16:10:11.726, 10=156,
    #msg = fix.generate_message( OrderedDict([ ('35',  'F'), ('41', tagClOrdID_11), ('11', str(random.randint(100, 1000000))), ('54', 2), ('60', fix.getLastSendingTime())]) )
    #, ('60', fix.getLastSendingTime())
    #self.send(msg)
    #20110817-08:37:25.231 : 8=FIX.4.49=013535=F49=MD805830018656=MFIXTradeIDCurr34=00000104652=20110817-08:35:54.25111=SESELT1//91641=SESELT1//87960=20110817-08:35:54.25110=224
    d_clID = 'TSESELT1//'+tagClOrdID_11+'0'
    #msg = fix.generate_message( OrderedDict([ ('35',  'D'),('11', d_clID), ('1','S01-00000F00'), ('38', 1000000000),('40', 2), ('44', 2386), ('54', 1), ('55', 'LKOH'),   ('386', '1'), ('336', 'EQBR'), ('59', 3) ] ) )
    msg = fix.generate_message( OrderedDict([ ('35',  'D'),('11', d_clID), ('1','S01-00000F00'), ('38', 10000),('40', 2), ('44', 2386), ('54', 1), ('55', 'LKOH'),   ('386', '1'), ('336', 'EQBR'), ('59', 3) ] ) )
    self.send(msg)
    time.sleep(1)
    '''for i in range (1,12):
      msg = fix.generate_message( OrderedDict([ ('35',  'F'), ('41', tagClOrdID_11), ('11', 'SESELT1//'+str(i)), ('54', 2), ('60', fix.getLastSendingTime())]) )
      self.send(msg)  '''
    
    msg = fix.generate_message( OrderedDict([ ('35',  'F'), ('41', d_clID), ('11', tagClOrdID_11), ('54', 2), ('60', fix.getLastSendingTime())]) )
    self.send(msg)

    #time.sleep(30)
    
    #logout_msg =fix.generate_Logout_35_5()
    #self.send(logout_msg)
    msg=None
  else:
    msg = None
  return msg
##############################################################################################################################

##############################################################################################################################
def process_mdfix(msg,  self = None):
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


##############################################################################################################################



def main():
    cl = Client(host, port,  process)
    cl.send(logon_msg)    


if __name__ == '__main__':
    main()
