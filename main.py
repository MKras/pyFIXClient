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
port = 9212
hertbeat_interval = 0

sender = 'MU0057000002'
#sender = 'MU0059000001'
#target = 'MFIXTradeCaptureID'
target = 'MFIXTradeID'
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

'''if (msg["35=0"])
		#@network.say Fix::generate_message({ 35 => "0" })
	elsif ( msg["35=1"] )
		reqId = Fix::get_tag_from_message( msg, 112 )
		@network.say Fix::generate_message({ 35 => "0", 112 => reqId })
	elsif ( msg["35=5"] )
		# nothing on disconnect
	elsif ( msg["35=2"] )
		@network.say Fix::generate_message({ 35 => "4", 36 => (Fix::current34tag + 2), 123 => 'N', 43 => 'Y' })
	elsif ( msg["35=4"] )
		new34Tag = Fix::get_tag_from_message( msg, 36 )
#		Fix::tag34=new34Tag
	elsif ( msg["35=A"] )	
		if (@first)'''
		
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
	elif (fix.get_tag(msg,  35) == 'A'):
		#network.say Micex::generate_35_D( cl_ord_id, "S01-00000F00", "EQBR", "SBER03", 1, 1, 0, (rand*100).round )
		#8=FIX.4.49=16735=D49=MU005900000156=MFIXTradeCaptureID34=352=20110627-10:56:2911=82750020211=S01-00000F00386=1336=EQBR55=SBER0354=160=20110627-10:56:29.00038=4340=144=010=060
		#trfix
		#msg = fix.generate_message( OrderedDict([ ('35',  'D'), ('49', sender), ('56' , target), ('11', str(random.randint(100, 1000000)) ), ('1', 'S01-00000F00'), ('386',  '1'), ('336', 'EQBR'), ('54', '1'), ('38', '43'), ('40', '1'),('44', '0') ]) )
		#trcap
		#@network.say Fix::generate_message({ 35 => "AD", 568=> "555", 569=> "0",  263=> "1" })
		msg = fix.generate_message( OrderedDict([ ('35',  'AD'), ('49', sender), ('56' , target), ('568', '555' ), ('569', '0'), ('263',  '1') ]) )
		self.send(msg)
		msg = fix.generate_message( OrderedDict([ ('35',  'AD'), ('49', sender), ('56' , target), ('568', '444' ), ('569', '0'), ('263',  '1') ]) )
		self.send(msg)
		msg=None
	else:
		msg = None
	return msg

#@network.say Micex::generate_35_D( cl_ord_id_1, "S01-00000F00", "EQBR", "SBER03", 2, 2 , 125, 800, {111=>150} )

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
		#msg = fix.generate_message( OrderedDict([ ('35',  'D'), ('49', sender), ('56' , target), ('11', str(random.randint(100, 1000000))), ('1', 'S01-00000F00'), ('386',  '1'), ('336', 'EQBR'), ('55', 'SBER03'), ('54', 1), ('38', 200), ('40', 2), ('44', 100) , ('111', 50)]) )
		msg = fix.generate_message( OrderedDict([ ('35',  'D'), ('49', sender), ('56' , target), ('11', str(random.randint(100, 1000000))), ('1', 'S01-00000F00'), ('386',  '1'), ('336', 'EQBR'), ('55', 'SBER03'), ('54', 2), ('38', 1000), ('40', 2), ('44', 100) , ('111', 100)]) )
		#msg = fix.generate_message( OrderedDict([ ('35',  'D'), ('49', sender), ('56' , target), ('11', str(random.randint(100, 1000000))), ('1', 'S01-00000F00'), ('386',  '1'), ('336', 'EQBR'), ('55', 'SBER03'), ('54', 1), ('38', 200), ('40', 2), ('44', 100) , ('111', 50)]) )
		self.send(msg)
		
		msg=None
	else:
		msg = None
	return msg

process = process_trfix
#process = process_trcap

def main():
    cl = Client(host, port,  process)
    cl.send(logon_msg)    
    

if __name__ == '__main__':
    main()
