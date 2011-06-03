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

def generate_groupe(grp_tag,  grp_tag_val,  grp_container):
    file = open('msg.in', encoding='utf-8',  mode='a')
    grp = fix.get_groupe(grp_tag,  grp_tag_val,  grp_container)
    print (grp)
    for it in grp:
        print(it+'='+grp[it])
        s=it+'='+grp[it]
    file.write( str( s) ) 
    file.write('\n')
    file.close()


grp_tag='270'
grp_tag_val = 2
grp_container = [('290',  0),  ('290', 1)]

generate_groupe(grp_tag,  grp_tag_val,  grp_container)

g = fix.get_groupe(grp_tag,  grp_tag_val,  grp_container)

msg =OrderedDict([('35',  'D'), (grp_tag, g[grp_tag]) ])
#msg =OrderedDict([('35',  'D'), ('57','XXXXXX') ])
generate_message(msg)


now = datetime.now()

now = fix.date_long_encode(now)
print(now)
now = fix.date_long_decode(now)
print(now)
