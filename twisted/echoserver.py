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

