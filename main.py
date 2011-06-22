#!/usr/bin/python3

from collections import OrderedDict

from datetime import datetime, date
from fix.fix44  import  FIX44
from fix.log  import  FIX_Log
from fix.network  import  Client,  Thread

LOGGER = FIX_Log()

host = '127.0.0.1'
port = 9121
hertbeat_interval = 55

sender = 'MU0057000002'
target = 'MFIXTradeCaptureID'

fix=FIX44()
fix.init(sender , target )
#fix.init('Sender',  'Target')

def generate_header():
    pass

def generate_message(msg):    
    LOGGER.log_in_msg(fix.generate_message(msg) )


class ind_client(Client):
    def __init__(self, host = '127.0.0.1',  port=9120 ):
      super().__init__(host,  int(port))
      print('done')
    
    def process(self,  msg):
        super().process(msg)

def main():
    '''example how to generate message with grope'''
    grp_tag='270'
    grp_tag_val = 2
    grp_container = [('290',  0),  ('290', 1)]
    g = fix.get_groupe(grp_tag,  grp_tag_val,  grp_container)
    #msg =OrderedDict([('35',  'A'), (grp_tag, g[grp_tag]) ])
    msg =OrderedDict([('35',  'A'), ('49', sender), ('56' , target),  ('98', 0) , ('108',  hertbeat_interval) ])

    m = fix.generate_message(msg) 

    if (fix.get_tag(m,  35) == 'D'):
        print ('35 = '+fix.get_tag(m,  35))

    now = datetime.now()

    '''now = fix.date_long_encode(now)
    print(now)
    now = fix.date_long_decode(now)
    print(now)'''
    
    cl = Client(host, port)
    #cl.start()
    cl.send(m)
    #cl.begin_listening()
    cl.start()
    #cl.listen()

if __name__ == '__main__':
    main()
