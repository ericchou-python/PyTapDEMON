#
# Example taken from:
# Twisted Network Programming Essentials, 2nd Edition
# By: Jessica McKellar, Abe Fettig
# OReilly Media, Ebook ISBN:978-1-4493-3330-0
#

from twisted.internet import reactor, protocol
import json

msg = json.dumps({"s1": {'s1MirrorSrc': [1], 's1MirrorDst': [6,7]}, "s2": {'s2MirrorSrc': [2], 's2MrrorDst': [7]}})

class EchoClient(protocol.Protocol):
    def connectionMade(self):
        print "Sending: ", msg
        self.transport.write(msg)

    def dataReceived(self, data):
        print "Server returned:", data
        self.transport.loseConnection()

class EchoFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        print "Build on addr: ", addr
        return EchoClient()

    def clientConnectionFailed(self, connector, reason):
        print "Connection failed."
        reactor.stop()

    def clientConnctionLost(self, connector, reason):
        print "Connection lost."
        reactor.stop()

reactor.connectTCP("localhost", 8000, EchoFactory())
reactor.run()

