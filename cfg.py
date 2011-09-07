#!/usr/bin/env python3

from collections import OrderedDict
import sys
from datetime import datetime, date

''' Tne next values should be setted:
app, host, port, sender, target, password'''

#hostname = '194.84.44.1' #telis
#hostname = 'evbyminsd0991' #evbyminsd0991
#hostname = '10.6.17.70'  #build machene
hostname = '127.0.0.1'  #local
#hostname = '194.84.44.42'  #robot

#self.thr_proc = threading.Thread(target=self.process, args=(self.data.decode('CP1251'),)).start() 


#myLock = Lock()

#app='trfix'
app='trcap'
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
  

#hertbeat_interval = 0

if hostname == '194.84.44.1': # telis
  sender = 'MU0059900001'
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
#sender = 'MU0059900002' # telis
#sender = 'MU0000800002' # telis

#sender = 'MU0059900001' # for telis
#sender = 'MU0057000002' # telis


password=' '


''' Here we can redefine its
(app, host, port, sender, target, password)'''

#!!!!!!!!!!!!!!!!!!!!!!!!!!
#telis curr
#target = 'MFIXTradeIDCurr'
#sender = 'MD0154300002' # telis
#sender = 'MD0154500001' # telis
#port = 9212
#host = '194.84.44.1'

'''if app == 'trfix':
  process = process_trfix

if app == 'trcap':
  process = process_trcap
if app == 'mdfix':
  process = process_mdfix
'''

def main():
    pass


if __name__ == '__main__':
    main()
