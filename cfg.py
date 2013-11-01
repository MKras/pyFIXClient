#!/usr/bin/env python3

from collections import OrderedDict
import sys
from datetime import datetime, date

''' Tne next values should be setted:
app, host, port, sender, target, password'''


hostname = '127.0.0.1'  #local


#password='XxX'
password=' '

#!!!!!!!!!!!!!!!!!!!!!!!!!!
#telis trfix
app='trfix'
client_target = 'Server'
client_sender = 'Client' 

server_target = 'Client'
server_sender = 'Server' # telis

port = 9120

host = hostname


'''if app == 'trfix':
  process = process_trfix

if app == 'trcap':
  process = process_trcap
if app == 'mdfix':
  process = process_mdfix
'''

def main():
    pass


if __name__ == '__main__':
    main()
