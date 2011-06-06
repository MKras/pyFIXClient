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
    #file = open('msg.in', encoding='utf-8',  mode='a')
    grp = fix.get_groupe(grp_tag,  grp_tag_val,  grp_container)
    #print (grp)
    for it in grp:
        #print(it+'='+grp[it])
        s=it+'='+grp[it]
    #file.write( str( s) ) 
    #file.write('\n')
    #file.close()


'''example how to generate message with grope'''
grp_tag='270'
grp_tag_val = 2
grp_container = [('290',  0),  ('290', 1)]
g = fix.get_groupe(grp_tag,  grp_tag_val,  grp_container)
msg =OrderedDict([('35',  'D'), (grp_tag, g[grp_tag]) ])
generate_message(msg)

#generate_groupe(grp_tag,  grp_tag_val,  grp_container)

msg =OrderedDict([('35',  'D'), (grp_tag, g[grp_tag]) , ('95',  'SSSSS')])

#generate_message(msg)

m = fix.generate_message(msg)  

print ('35 = '+str(fix.get_tag(m,  35)))

now = datetime.now()

now = fix.date_long_encode(now)
print(now)
now = fix.date_long_decode(now)
print(now)
