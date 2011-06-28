#!/usr/bin/python3

from collections import OrderedDict

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

sender = 'MU0057000002'
#sender = 'MU0059000001'
target = 'MFIXTradeCaptureID'
password=' '

fix=FIX44()
fix.init(sender , target )
logon_msg =fix.generate_message ( OrderedDict([('35',  'A'), ('49', sender), ('56' , target), ('98', 0), ('108',  hertbeat_interval), ('141', 'N'), ('554', password)]) )

'''example how to generate message with grope'''
'''grp_tag='270'
    grp_tag_val = 2
    grp_container = [('290',  0),  ('290', 1)]
    g = fix.get_groupe(grp_tag,  grp_tag_val,  grp_container)'''
'''if (fix.get_tag(m,  35) == 'D'):
        print ('35 = '+fix.get_tag(m,  35))'''

def process(msg):
	#time.sleep(1)
	if (fix.get_tag(msg,  35) == 'A'):
		#network.say Micex::generate_35_D( cl_ord_id, "S01-00000F00", "EQBR", "SBER03", 1, 1, 0, (rand*100).round )
		#8=FIX.4.49=16735=D49=MU005900000156=MFIXTradeCaptureID34=352=20110627-10:56:2911=82750020211=S01-00000F00386=1336=EQBR55=SBER0354=160=20110627-10:56:29.00038=4340=144=010=060
		#trfix
		#msg = fix.generate_message( OrderedDict([ ('35',  'D'), ('49', sender), ('56' , target), ('11', str(random.randint(100, 1000000)) ), ('1', 'S01-00000F00'), ('386',  '1'), ('336', 'EQBR'), ('54', '1'), ('38', '43'), ('40', '1'),('44', '0') ]) )
		#trcap
		#@network.say Fix::generate_message({ 35 => "AD", 568=> "555", 569=> "0",  263=> "1" })				
		msg = fix.generate_message( OrderedDict([ ('35',  'AD'), ('49', sender), ('56' , target), ('568', '555' ), ('569', '0'), ('263',  '1') ]) )
	elif (fix.get_tag(msg,  35) == '0'):
		msg = fix.generate_message( OrderedDict([ ('35',  '0'), ('49', sender), ('56' , target)]) )
	else:
		msg = None
	return msg

def main():
    cl = Client(host, port,  process)
    cl.send(logon_msg)    
    

if __name__ == '__main__':
    main()
