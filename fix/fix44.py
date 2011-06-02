#!/usr/bin/python3
''' Simple FIX client'''

from datetime import datetime, date

class FIX44(object):    
    PROTOCOL='FIX.4.4'
    SOH = '\x01'
    DATE_SHORT_FORMAT= '%Y%m%d'
    DATE_LONG_FORMAT= '%Y%m%d-%H:%M:%S'
    HEADER_NECESSERY_TAGS = [ 8, 35, 49, 56, 34, 52 ]
    #DEFAULT_HEADER_TAGS_VALUES = {'8':PROTOCOL,  }
    
    def __init__ (self):
        self.seqNum=0

    def init (self, SenderCompId,  TargetCompId):
        self.seqNum=0
        if (TargetCompId is None) or (TargetCompId is None):
            raise Exception
        else:
            self.SenderCompId = SenderCompId
            self.TargetCompId = TargetCompId
        

    def get_next_seqNum(self):
        self.seqNum+=1
        return self.seqNum

    def set_seqNum(self,  num):
        self.seqNum = num
        return self.seqNum

    def get_header(self):
        self.header={'8':FIX44.PROTOCOL, '49':self.SenderCompId,  '56': self.TargetCompId,  '34':FIX44.get_next_seqNum(self),  '52':FIX44.date_long_encode(self,  datetime.now())}
        return  self.header
    
    def generate_message(self,  body):    
        header = self.get_header()
        header.update(body)
        
        self.body=''
        for key,  val  in header.items():
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
