#!/usr/bin/env python3
''' Simple FIX client'''

import unittest
import random
import string
import json
import os.path
from collections import OrderedDict
from datetime import datetime, date
import logging

class FIXException(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)


class FIX44(object):    
    PROTOCOL='FIX.4.4'
    SOH = '\x01'
    DATE_SHORT_FORMAT= '%Y%m%d'
    DATE_LONG_FORMAT= '%Y%m%d-%H:%M:%S'
    HEADER_NECESSERY_TAGS = [ 8, 35, 49, 56, 34, 52 ]
    LOGGER=None	
    
    def __init__ (self):
        self.seqNum=0
        self.session_file='session.json'
        self.customer_processor = None

    def init (self, SenderCompId,  TargetCompId, customer_processor):
        self.seqNum=0
        self.customer_processor = customer_processor
        cfg = self.restore_config()
        if cfg and cfg['SeqNum']:
            self.seqNum = cfg['SeqNum']            
        if (TargetCompId is None) or (TargetCompId is None):
            raise Exception
        else:
            self.SenderCompId = SenderCompId
            self.TargetCompId = TargetCompId
            self.LastSendingTime_52=''
            self.LastOrderID_37 = ''

    def get_seqNum(self):
        return self.seqNum

    def get_next_seqNum(self):
        self.seqNum+=1
        return self.seqNum

    def set_seqNum(self,  num):
        self.seqNum = num
        return self.seqNum
    
    def store_config(self):
        cfg_json = {
            'Sender': self.SenderCompId,
            'Target' : self.TargetCompId,
            'SeqNum': self.seqNum
        }
        cfg_file = open(self.session_file, 'w')
        json.dump(cfg_json, cfg_file, indent=4)
        cfg_file.close()
    
    def restore_config(self):
        if (os.path.exists(self.session_file)):
            cfg_file = open(self.session_file, 'r')
            cfg_json = json.load(cfg_file)
            cfg_file.close()
            return cfg_json
            
    def init_from_file (self):
        cfg = self.restore_config()
        if cfg:
            self.seqNum = cfg['SeqNum']
            self.SenderCompId = cfg['Sender']
            self.TargetCompId = cfg['Target']
        else:
            raise FIXException('Can not find '+self.session_file+' file!')
            
    def restore_SeqNum_from_file (self):
        cfg = self.restore_config()
        if cfg:
            if self.SenderCompId == cfg['Sender'] and self.TargetCompId == cfg['Target']:
              self.seqNum = cfg['SeqNum']
            else:
              raise FIXException('wrong Sender and Target in '+self.session_file+' file!') 
        else:
            raise FIXException('Can not find '+self.session_file+' file!')
            
    def get_header(self):        
        self.LastSendingTime_52 = FIX44.date_long_encode(self,  datetime.now())
        self.header = OrderedDict([('8',  FIX44.PROTOCOL), ('35', None), ('49',  self.SenderCompId),  ('56',  self.TargetCompId),  
                                   ('34',  FIX44.get_next_seqNum(self)),  ('52',  self.LastSendingTime_52) ])        
        return  self.header
    
    def getLastSendingTime(self):
      return self.LastSendingTime_52
      

    def get_trailer(self,  msg ):
        '''assume msg is str'''    
        tag35_pos = msg.index('35=')
        tag9 = str(len(msg[tag35_pos:]))
        msg = msg[:tag35_pos]+'9='+tag9+FIX44.SOH+msg[tag35_pos:]
        tag10 = str( sum(ord(c) for c in msg) & 255 )
        if len(tag10) > 3:
          tag10 = tag10[:2]
        else:
          while len(tag10)<3:
            tag10 = '0'+tag10
        msg+='10='+tag10+FIX44.SOH
        return msg
    
    def get_groupe(self, grp_tag_val,  grp_container):
        '''assume grp_container is set of dicts [(key, val),]
        returns group's tag val and proup tags like string/ example to use:
        ....OrderedDict([ ('<grout_tag>', get_groupe(<grp_tag_val>, ([(tag, val),(tag, val),(tag, val),(tag, val).....])))])
        '''
        container=''
        for it in grp_container:            
            key,  val  = it
            container+=str(str(key)+'='+str(val))+FIX44.SOH
        container = container[:-1]
        self.res  = str(str(grp_tag_val)+FIX44.SOH+container)
        return self.res

    def generate_message(self,  body, exclude_tags = None):  
        try:
           self.header = self.get_header()
           self.header.update(body)           
           self.body=''
           for key,  val  in self.header.items():
               if exclude_tags is not None and key in exclude_tags:
                 continue
               self.body+= str(str(key)+'='+str(val))+FIX44.SOH
           self.body = self.get_trailer(self.body)
        except (TypeError,  ValueError) as err:
            logging.critical('generate_message Exception: '+ str(err))
            return ''
        return self.body
    
    def get_tag(self,  msg,  tag_num):
        tags = msg.split(FIX44.SOH)
        tags_dict = OrderedDict([])
        for tag_val in tags:            
            item = tag_val.split('=')
            #print(item)
            if (len(item) >1):
                tags_dict.update(OrderedDict([(item[0],  item[1])]))
        return str(tags_dict.get(str(tag_num)))
    
    def generate_Login_35_A (self, hertbeat_interval = 0, password = ' ', rest=None ):
      if (rest):
        if ((str(rest.get(str('141')))) == str('N')):
          print ('Try to load SeqNum  from session.cfg')
          self.restore_SeqNum_from_file()
    
      msg = OrderedDict([('35',  'A'), ('49', self.SenderCompId), ('56' , self.TargetCompId), ('98', 0), ('108',  hertbeat_interval),  ('554', password)]) #('141', 'N'),
      if rest :
        msg.update(OrderedDict(rest))
      login = self.generate_message ( msg )  
      self.session_is_active = True
      return login

    def generate_Logout_35_5 (self, rest=None ):
      msg = OrderedDict([('35',  '5'), ('49', self.SenderCompId), ('56' , self.TargetCompId)])
      if rest :
        msg.update(OrderedDict(rest))
      logout = self.generate_message ( msg )  
      self.store_config()
      self.session_is_active = False
      return logout

    def generate_Heartbeat_35_0 (self, rest=None ):
      msg = OrderedDict([('35',  '0'), ('49', self.SenderCompId), ('56' , self.TargetCompId)])      
      if rest :
        msg.update(OrderedDict(rest))
      Heartbeat = self.generate_message ( msg )  
      return Heartbeat

      #logout_msg =fix.generate_message ( OrderedDict([('35',  '5'), ('49', sender), ('56' , target)]) )

    def adapt_fix_message(self,  msg,  tag_num):
        tags = msg.split(FIX44.SOH)
        tags_dict = OrderedDict([])
        for tag_val in tags:            
            item = tag_val.split('=')
            #print(item)
            if (len(item) >1):
                tags_dict.update(OrderedDict([(item[0],  item[1])]))
        return str(tags_dict.get(str(tag_num)))

    def generate_message_from_list(self,  msg):  
        try:
           body=''
           for tag  in msg:
             if tag is not '':
               body+= str(tag)+FIX44.SOH  
           #body = body[:-1]    
           body = self.get_trailer(body)
        except (TypeError,  ValueError) as err:
            logging.critical('generate_message_from_list Exception: '+ str(err))
            return ''
        return body

    def parce(self, msg, split_symbol = '^', rest=None):
      tags = msg.split(split_symbol)
      for i in range(0, len(tags)):
        splitted_tag = tags[i].split('=')
        if splitted_tag[0] == '9':
          tags[i]=''
        if splitted_tag[0] == '10':
          tags[i]=''
        if splitted_tag[0] == '49':
          tags[i]='49='+self.SenderCompId
        if splitted_tag[0] == '56':
          tags[i]='56='+self.TargetCompId
        if splitted_tag[0] == '34':
          tags[i]='34='+str(FIX44.get_next_seqNum(self))
        if splitted_tag[0] == '52':
          tags[i]='52='+FIX44.date_long_encode(self,  datetime.now())
        if splitted_tag[0] == '11':
          tags[i]='11='+''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
        if rest is not None:
          for key,  val  in rest.items():
               if splitted_tag[0] == key:
                 tags[i]=key+'='+str(val)
      return self.generate_message_from_list(tags)

    def get_parsed_fix_messages_from_file(self, filename, split_symbol = '^', encod = 'utf-8' ):
      res=[]
      self.file = open(filename, encoding=encod,  mode='r')
      for line in self.file.readlines():
        try:
          res.append(self.parce(line.strip()[line.strip().index('8=FI'):], split_symbol))
        except (TypeError,  ValueError) as err:
            logging.critical('\nget_parsed_fix_messages_fron_file in string:\n'+line+'\nException:\n'+ str(err)+'\n')
      return res
    
    def get_fix_messages_from_file(self, filename, split_symbol = '^', encod = 'utf-8' ):
      res=[]
      self.file = open(filename, encoding=encod,  mode='r')
      for line in self.file.readlines():
        try:
          res.append(line.strip()[line.strip().index('8=FI'):])
        except (TypeError,  ValueError) as err:
            logging.critical('\nget_parsed_fix_messages_fron_file in string:\n'+line+'\nException:\n'+ str(err)+'\n')
      return res
      
    def set_LastOrderID_37(self, tagOrderID_37 = ''):
      if tagOrderID_37 is not None:
        self.LastOrderID_37 = tagOrderID_37
      else:
        raise FIXException('You try to set tagOrderID_37, but it is None!')
  
    def get_LastOrderID_37(self):
      return self.LastOrderID_37
    
    def compare_msgs(self, msg, template):
      for key,  val  in template.items():
        if not str(val) == str(self.get_tag(msg, key)):
          #print('Fail key: ', key, 'val: ', val, 'self.get_tag(msg, ',key,'): ',self.get_tag(msg, key) )
          return False
        else:
          #print('key: ', key, 'val: ', val, 'self.get_tag(msg, ',key,'): ',self.get_tag(msg, key) )    
          pass
      return True
      
    def get_randomID(self, length=10):
      return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(length))

    def date_short_encode(self, date_short):
        return d.strftime(FIX44.DATE_SHORT_FORMAT)

    def date_short_decode(self, date_short):
        return datetime.strptime(self, date_short, FIX44.DATE_SHORT_FORMAT).date()

    def date_long_encode(self, date_long):
        return date_long.strftime(FIX44.DATE_LONG_FORMAT)

    def date_long_decode(self,  date_long):
        return datetime.strptime(date_long, FIX44.DATE_LONG_FORMAT)

class FIX44_Tests(unittest.TestCase):  

  def setUp(self):    
    self.fix=FIX44()
    pass
    
  def test_compare_msgs_true(self):
    '''test_compare_msgs_true Failed'''
    self.fix.init('Sender' , 'Target' )      
    self.tagClOrdID_11 = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
    self.tagClOrdID_526 = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(5))
    self.msg = self.fix.generate_message( OrderedDict([ ('35',  'D'),('11', self.tagClOrdID_11), ('1','S01-00000F00'), ('38', 150),('40', 2), ('44', 42), ('54', 1), ('55', 'AFLT'), ('526',self.tagClOrdID_526 ),  ('386', '1'), ('336', 'EQBR'), ('59', 0) ] ) )
    self.template = ( OrderedDict([ ('35',  'D'), ('1','S01-00000F00'), ('38', 150),('40', 2), ('44', 42), ('54', 1), ('55', 'AFLT'), ('386', '1'), ('336', 'EQBR'), ('59', 0) ] ) )
    #print('self.msg = ',self.msg)
    #print('self.template = ', self.template)
    self.assertEqual(True, self.fix.compare_msgs(self.msg, self.template))
    pass
    
  '''def test_group_tag(self):
    ' ' 'test_group_tag Failed' ' '
    self.fix.init('Sender' , 'Target' )
    self.grp = self.fix.get_groupe('3',([('1', 1),('2', 1),('3', 1),('1', 2),('2', 2),('3', 2)]))
    
    #self.template = self.fix.generate_message(OrderedDict([ ('35', 'D'),('77', str('3'+FIX44.SOH+'1=1'+FIX44.SOH+'2=1'+FIX44.SOH+'3=1'+FIX44.SOH+'1=2'+FIX44.SOH+'2=2'+FIX44.SOH+'3=2'))]))
    self.template = (OrderedDict([ ('35', 'D'),('77', str('3'+FIX44.SOH+'1=1'+FIX44.SOH+'2=1'+FIX44.SOH+'3=1'+FIX44.SOH+'1=2'+FIX44.SOH+'2=2'+FIX44.SOH+'3=2'))]))
    self.msg = self.fix.generate_message(OrderedDict([ ('35', 'D'), ('77',  self.grp)]))
    #print('self.msg = ',self.msg)
    #print('self.template = ', self.template)
    self.assertEqual(True, self.fix.compare_msgs(self.msg, self.template))
    pass'''
    
  def test_exclude_tags_true(self):
    '''test_exclude_tags_true Failed'''
    self.fix.init('Sender' , 'Target' )      
    self.tagClOrdID_11 = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
    self.tagClOrdID_526 = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(5))
    self.msg = self.fix.generate_message( OrderedDict([ ('35',  'D'),('11', self.tagClOrdID_11), ('1','S01-00000F00'), ('38', 150),('40', 2), ('44', 42), ('54', 1), ('55', 'AFLT'), ('526',self.tagClOrdID_526 ),  ('386', '1'), ('336', 'EQBR'), ('59', 0) ] ), OrderedDict([('55', 'AFLT')])  )
    self.template = ( OrderedDict([ ('35',  'D'), ('1','S01-00000F00'), ('38', 150),('40', 2), ('44', 42), ('54', 1), ('386', '1'), ('336', 'EQBR'), ('59', 0) ] ) )
    #print('self.msg = ',self.msg)
    #print('self.template = ', self.template)
    self.assertEqual(True, self.fix.compare_msgs(self.msg, self.template))
    pass
    
  def test_cfg_test(self):
    '''restore session parameters Failed'''
    self.fix.init('Test_Sender' , 'Test_Target' )
    self.fix.store_config()
    
    self.test_fix=FIX44()
    self.test_fix.init_from_file()
    self.assertEqual(self.test_fix.seqNum, self.fix.seqNum)
    self.assertEqual(self.test_fix.TargetCompId, self.fix.TargetCompId)
    self.assertEqual(self.test_fix.SenderCompId, self.fix.SenderCompId)

  def test_cfg_test(self):
    '''restore session parameters for 35=A 141=N Failed'''
    self.fix.init('Test_Sender' , 'Test_Target' )
    self.fix.set_seqNum(48)
    self.fix.store_config()
    
    self.test_fix_N=FIX44()
    self.test_fix_N.init('Test_Sender' , 'Test_Target' )
    #self.test_fix.init_from_file()
    self.test_fix_N.generate_Login_35_A(0, ' ', OrderedDict([ ('98', 0), ('141', 'N'), ('554', ' '), ('43', 'N'), ('97', 'N')]) )
    self.assertEqual(self.test_fix_N.seqNum-1, self.fix.seqNum)
    self.assertEqual(self.test_fix_N.TargetCompId, self.fix.TargetCompId)
    self.assertEqual(self.test_fix_N.SenderCompId, self.fix.SenderCompId)    
    
    self.test_fix_Y=FIX44()
    self.test_fix_Y.init('Test_Sender' , 'Test_Target' )
    self.test_fix_Y.set_seqNum(0)
    #self.test_fix.init_from_file()
    self.test_fix_Y.generate_Login_35_A(0, ' ', OrderedDict([ ('98', 0), ('141', 'Y'), ('554', ' '), ('43', 'N'), ('97', 'N')]) )
    self.assertEqual(self.test_fix_Y.seqNum , 1)
    self.assertEqual(self.test_fix_Y.TargetCompId, self.fix.TargetCompId)
    self.assertEqual(self.test_fix_Y.SenderCompId, self.fix.SenderCompId)   
    
    
    self.test_fix_NO=FIX44()
    self.test_fix_NO.init('Test_Sender' , 'Test_Target' )
    self.test_fix_NO.set_seqNum(0)
    self.test_fix_NO.generate_Login_35_A(0, ' ', OrderedDict([ ('98', 0), ('554', ' '), ('43', 'N'), ('97', 'N')]) )
    self.assertEqual(self.test_fix_NO.seqNum , 1)
    self.assertEqual(self.test_fix_NO.TargetCompId, self.fix.TargetCompId)
    self.assertEqual(self.test_fix_NO.SenderCompId, self.fix.SenderCompId)  
    
   
  def test_speed_test(self):
    ''' speed_test Failed'''
    import cProfile, pstats, io
    
    def time_func(self):
      OrderQty_38 = 0
      Price_44 = 20000; 
      self.fix.init('Test_Sender' , 'Test_Target' )      
      for x in range(0,100000):
        self.fix.generate_message( OrderedDict([ ('35',  'D'),('11', self.fix.get_randomID()), ('1','accaunt'), ('38', 'float(OrderQty_38+=1)' ),('40', 'OrdType_40'), ('44','Int(Price_44-=1)' ), ('54', 'Side_54'), ('55', 'Symbol_55'),   ('386', '1'), ('336', '2'), ('59', 'TimeInForce_59'), ('625', 'D'), ('526', 'SecondaryClOrdID_526') ] ))    
    print ('run time_func()')  
    #pr = profile.Profile(time_func(self)) #time_func(self)
    #profile.run("time_func(self)")
    profile = cProfile.Profile()
    profile.enable()
    profile.runcall(time_func, self)    
    profile.create_stats()
    profile.dump_stats('time_func.prof')
    
    ststs = pstats.Stats('time_func.prof')
    ststs.print_stats()
    

if __name__ == '__main__':
    unittest.main()
