#!/usr/bin/env python3

from collections import OrderedDict
import sys
from datetime import datetime, date
from fix.fix44  import  FIX44
from fix.log  import  FIX_Log
from fix.network  import  Client, threading_deco
from cfg import app, host, port, client_sender, client_target, password
import random
import time
import threading,  _thread
from threading import Thread, Lock
import string
import logging
from queue import Queue


class BaseProcessor(object):
    
    def cut_numbers_after_point_str(self, val, numbers_after_point):
      '''# will round last number
      format_str = "{0:."+str(numbers_after_point)+"f}"
      return str( format_str.format(float(val)))  '''
      
      #no round, just cut
      val = str(val)  
      if ( (val.find('.')) is -1):
        return val
      idx = val.index('.')  
      return val[:idx+1+numbers_after_point]
      
    def __init__(self):
        pass
    
    def process(self, msg, self_fix):
        pass



