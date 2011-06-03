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

def generate_grope(grp_tag,  grp_tag_val,  grp_container):
    file = open('msg.in', encoding='utf-8',  mode='a')
    grp = fix.get_groupe(grp_tag,  grp_tag_val,  grp_container)
    print (grp)
    for it in grp:
        print(it+'='+grp[it])
        s=it+'='+grp[it]
    file.write( str( s) ) 
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

#msg =OrderedDict([('35',  'D') ])
#generate_message(msg)

grp_tag='270'
grp_tag_val = 2
grp_container = [('290',  0),  ('290', 1)]

generate_grope(grp_tag,  grp_tag_val,  grp_container)


now = datetime.now()

now = fix.date_long_encode(now)
print(now)
now = fix.date_long_decode(now)
print(now)
