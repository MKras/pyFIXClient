#!/usr/bin/python3
''' Simple FIX client'''
    
class FIX44(object):    
    PROTOCOL='FIX.4.4'
    SOH = '\x01'
    
    def __init__ (self):
        self.seqNum=0

    def get_next_seqNum(self):
        self.seqNum+=1
        return self.seqNum
    
    def get_header(selfself):
        pass
    
    def generate_message(self,  body):    
        self.body=''
        for key,  val  in body.items():
            self.body+= str(key+'='+str(val))+FIX44.SOH
        return self.body
    
