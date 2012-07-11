#!/usr/bin/env python3

from collections import OrderedDict
import sys
from datetime import datetime, date

''' Tne next values should be setted:
app, host, port, sender, target, password'''


hostname = '127.0.0.1'  #local
#hostname = 'evbyminsd1118' #evbyminsd1118
#hostname = '194.84.44.1'  #robot

#self.thr_proc = threading.Thread(target=self.process, args=(self.data.decode('CP1251'),)).start() 


#myLock = Lock()

#password='XxX'
password=' '

#!!!!!!!!!!!!!!!!!!!!!!!!!!
#telis trfix
app='trfix'
target = 'MFIXTradeID'
sender = 'MU0057000001' # telis
#sender = 'MU0057000003' # telis
#sender = 'MU0000800004' # telis
#sender = 'MU0059900002' # telis
port = 9120
#port = 9132
host = hostname


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
