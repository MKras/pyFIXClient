#!/usr/bin/python3

    
from fix.fix44  import  *

fix=FIX44()


def generate_header():
    pass

def generate_message(msg):
    m=''
    for key,  val  in msg.items():
        m += str(key+'='+str(val))+FIX44.SOH
    msg=m
    
    file = open('msg.in', encoding='utf-8',  mode='a')
    file.write(msg)
    file.write('\n')
    file.close()

msgs=[]

msgs.append({ '35': 'A',   '34' : fix.get_next_seqNum()  } )
msgs.append({ '35': 'B',   '34' : fix.get_next_seqNum() } )
msgs.append({ '35': 'C',   '34' : fix.get_next_seqNum() } )
msgs.append({ '35': 'D',   '34' : fix.get_next_seqNum() } )

for msg in msgs:
    generate_message(msg)
    
    
