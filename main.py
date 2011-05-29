#!/usr/bin/python3
''' Simple FIX client'''
    
SOH = '\x01'

seqNum=0

def get_next_seq_nam():
    global seqNum
    seqNum=seqNum+1
    return seqNum

def generate_message(msg):
    mm=''
    for key,  val  in msg.items():
        mm += str(key+'='+str(val))+SOH
    msg=mm
    
    file = open('msg.in', encoding='utf-8',  mode='a')
    file.write(msg)
    file.write('\n')
    file.close()

msgs=[]

msgs.append(dict( { '35': 'A',   '34' : get_next_seq_nam() }) )
msgs.append(dict( { '35': 'B',   '34' : get_next_seq_nam() }) )
msgs.append(dict( { '35': 'C',   '34' : get_next_seq_nam() }) )
msgs.append({ '35': 'D',   '34' : get_next_seq_nam() } )

for msg in msgs:
    generate_message(msg)
    
    
