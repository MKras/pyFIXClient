#!/usr/bin/python3

from collections import OrderedDict

from datetime import datetime, date
from fix.fix44  import  *


fix=FIX44()
fix.init('Sender',  'Target')

def generate_header():
    pass

def generate_message(msg):
    file = open('msg.in', encoding='utf-8',  mode='a')
    file.write( fix.generate_message(msg) )
    file.write('\n')
    file.close()


'''msgs=[]
msgs.append({ '35': 'A',   '34' : fix.get_next_seqNum()  } )
msgs.append({ '35': 'B',   '34' : fix.get_next_seqNum() } )
msgs.append({ '35': 'C',   '34' : fix.get_next_seqNum() } )
msgs.append({ '35': 'D',   '34' : fix.get_next_seqNum() } )

for msg in msgs:
    generate_message(msg)
'''

msg =OrderedDict([('35',  'D') ])
generate_message(msg)


now = datetime.now()

now = fix.date_long_encode(now)
print(now)
now = fix.date_long_decode(now)
print(now)
