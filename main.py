#!/usr/bin/python3

from collections import OrderedDict

from datetime import datetime, date
from fix.fix44  import  FIX44
from fix.log  import  FIX_Log
from fix.network  import  Client

LOGGER = FIX_Log()

fix=FIX44()
fix.init('Sender',  'Target')

def generate_header():
    pass

def generate_message(msg):    
    LOGGER.log_in_msg(fix.generate_message(msg) )


def main():
    '''example how to generate message with grope'''
    grp_tag='270'
    grp_tag_val = 2
    grp_container = [('290',  0),  ('290', 1)]
    g = fix.get_groupe(grp_tag,  grp_tag_val,  grp_container)
    msg =OrderedDict([('35',  'D'), (grp_tag, g[grp_tag]) ])
    #generate_message(msg)

    #generate_groupe(grp_tag,  grp_tag_val,  grp_container)

    #msg =OrderedDict([('35',  'D'), (grp_tag, g[grp_tag]) , ('95',  'SSSSS')])


    m = fix.generate_message(msg) 

    if (fix.get_tag(m,  35) == 'D'):
        print ('35 = '+fix.get_tag(m,  35))
        #LOGGER.log_in_msg(m)
        

    now = datetime.now()

    '''now = fix.date_long_encode(now)
    print(now)
    now = fix.date_long_decode(now)
    print(now)'''
    
    cl = Client('127.0.0.1', 9120)
    cl.send(m)

if __name__ == '__main__':
    main()
