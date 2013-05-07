#
# Example taken from:
# Twisted Network Programming Essentials, 2nd Edition
# By: Jessica McKellar, Abe Fettig
# OReilly Media, Ebook ISBN:978-1-4493-3330-0
#

from twisted.internet import protocol, reactor
import json

class Echo(protocol.Protocol):
    def dataReceived(self, data):
        print "Received This Data: ", data
        ports = json.loads(data)
        for key in ports: 
            print key, ports[key]
        self.transport.write(data)

class EchoFactory(protocol.Factory):
    def buildProtocol(self, addr):
        print "Received from addr: ", addr
        return Echo()

reactor.listenTCP(8000, EchoFactory())
reactor.run()

