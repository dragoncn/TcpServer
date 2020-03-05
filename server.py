import sys
import threading
from socketserver import BaseRequestHandler, TCPServer, ThreadingMixIn
from protocol import processMsg

class ThreadingTCPServer(ThreadingMixIn, TCPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        TCPServer.__init__(self, server_address, RequestHandlerClass)
    pass

class EchoHandler(BaseRequestHandler):
    def handle(self):
        print('Got connection from', self.client_address)
        while True:
            msg = self.request.recv(8192)
            if not msg:
                break
            ret=processMsg(msg)
            self.request.send(ret)

if __name__ == '__main__':
    serv = ThreadingTCPServer(('', 88), EchoHandler)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)

