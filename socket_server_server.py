#!/usr/bin/python3
# a simple tcp server

import socketserver

class EchoRequestHandler(socketserver.BaseRequestHandler ):
    def setup(self):
        print (self.client_address, 'connected!')
        msg = 'hi ' + str(self.client_address) + '\n'
        self.request.send(msg.encode())

    def handle(self):
        data = 'dummy'
        while data:
            data = self.request.recv(1024)
            self.request.send(data.encode())
            if data.strip() == 'bye':
                return

    def finish(self):
        print (self.client_address, 'disconnected!')
        msg = 'bye ' + str(self.client_address) + '\n'
        self.request.send(msg.decode())

    #server host is a tuple ('host', port)
server = socketserver.ThreadingTCPServer(('', 9120), EchoRequestHandler)
server.serve_forever()
