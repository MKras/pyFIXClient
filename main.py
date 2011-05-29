#!/usr/bin/python3

from datetime import datetime, date
from fix.fix44  import  *

fix=FIX44()


def generate_header():
    pass

def generate_message(msg):
    file = open('msg.in', encoding='utf-8',  mode='a')
    file.write( fix.generate_message(msg) )
    file.write('\n')
    file.close()


msgs=[]
msgs.append({ '35': 'A',   '34' : fix.get_next_seqNum()  } )
msgs.append({ '35': 'B',   '34' : fix.get_next_seqNum() } )
msgs.append({ '35': 'C',   '34' : fix.get_next_seqNum() } )
msgs.append({ '35': 'D',   '34' : fix.get_next_seqNum() } )

for msg in msgs:
    generate_message(msg)


DATEFMT = '%Y%m%d'

def dencode(d):
	return d.strftime(DATEFMT)

def ddecode(d):
	return datetime.strptime(d, DATEFMT).date()

DATETIMEFMT = '%Y%m%d-%H:%M:%S'

def dtencode(dt):
	return dt.strftime(DATETIMEFMT)

def dtdecode(dt):
	return datetime.strptime(dt, DATETIMEFMT)


now = datetime.now()
now = dtencode(now)


print(now)
