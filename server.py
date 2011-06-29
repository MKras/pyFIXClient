#!/usr/bin/python3

from collections import OrderedDict

from fix.network  import  Server

from datetime import datetime, date
from fix.fix44  import  FIX44
from fix.log  import  FIX_Log
from fix.network  import  Client,  Thread
import random
import time

LOGGER = FIX_Log()

host = '127.0.0.1'
port = 9121
hertbeat_interval = 0

sender = 'MFIXTradeCaptureID'
target = 'MU0057000002'
password=' '

fix=FIX44()
fix.init(sender , target )

def process(msg,  self = None):
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
		msg =fix.generate_message ( OrderedDict([('35',  'A'), ('49', sender), ('56' , target), ('98', 0), ('108',  hertbeat_interval), ('141', 'N'), ('554', password)]) )
		#msg=None
	elif (fix.get_tag(msg,  35) == 'AD'):
		msg =fix.generate_message ( OrderedDict([('35',  'AE'), ('49', sender), ('56' , target), ('98', 0), ('108',  hertbeat_interval), ('141', 'N'), ('554', password)]) )
		msg =fix.generate_message ( OrderedDict([('35', 'AQ'), ('49', sender), ('56' , target), ('568', '555'), ('569', '0') ]) )
		self.send(msg)
		msg =fix.generate_message ( OrderedDict([('35', 'AQ'), ('49', sender), ('56' , target), ('568', '555'), ('569', '1') ]) )
		self.send(msg)
		msg=None
	else:
		msg = None
	return msg

def main():
    srv = Server ('127.0.0.1',  9121, process)
    #srv.listen()
    #srv.begin_listening()
    #srv.start()
    
if __name__ == '__main__':
    main()

