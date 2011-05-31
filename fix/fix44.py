#!/usr/bin/python3
''' Simple FIX client'''

from datetime import datetime, date

class FIX44(object):    
    PROTOCOL='FIX.4.4'
    SOH = '\x01'
    DATE_SHORT_FORMAT= '%Y%m%d'
    DATE_LONG_FORMAT= '%Y%m%d-%H:%M:%S'
    HEADER_NECESSERY_TAGS = [ 8, 35, 49, 56, 34, 52 ]
    
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

    def date_short_encode(self, date_short):
        return d.strftime(FIX44.DATE_SHORT_FORMAT)

    def date_short_decode(self, date_short):
        return datetime.strptime(self, date_short, FIX44.DATE_SHORT_FORMAT).date()

    def date_long_encode(self, date_long):
        return date_long.strftime(FIX44.DATE_LONG_FORMAT)

    def date_long_decode(self,  date_long):
        return datetime.strptime(date_long, FIX44.DATE_LONG_FORMAT)
