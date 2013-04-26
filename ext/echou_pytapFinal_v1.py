#!/usr/bin/env python

"""
Custom Topology: PyTapDEMON_topo.py

"""

# These next two imports are common POX convention
from pox.core import core
import pox.openflow.libopenflow_01 as of

from twisted.internet import protocol, reactor
import json

# Even a simple usage of the logger is much nicer than print!
log = core.getLogger()

# global flow timeout
timeout = 120

# flow simulation on ports
s1PortPairs = [(1,2), (3,4)]
s2PortPairs = [(1,2)]

# mirror source and destination
f = open('ext/mirrorPorts.txt', 'r')
for num, item in enumerate(f.readlines()):
    if num == 0:
        s1MirrorSrc = item.strip().split(',')[1:]
        s1MirrorSrc = map(lambda x: int(x), s1MirrorSrc) #convert to int
    if num == 1:
        s1MirrorDst = item.strip().split(',')[1:]
        s1MirrorDst = map(lambda x: int(x), s1MirrorDst)
    if num == 2:
        s2MirrorSrc = item.strip().split(',')[1:]
        s2MirrorSrc = map(lambda x: int(x), s2MirrorSrc)
    if num == 3: 
        s2MirrorDst = item.strip().split(',')[1:]
        s2MirrorDst = map(lambda x: int(x), s2MirrorDst)

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

def _PortFlowMod(srcPort, dstPort, timeout, mirrorSrc, mirrorDst):
    print "Push Flow from Source Port %s to Destion Port %s with %s seconds timeout" % \
    (srcPort, dstPort, timeout)
    forwardFlow = of.ofp_flow_mod()
    forwardFlow.idle_timeout = timeout
    forwardFlow.hard_timeout = timeout
    forwardFlow.match.in_port = srcPort
    forwardFlow.actions.append(of.ofp_action_output(port=dstPort))
    # add mirror src and destination
    if srcPort in mirrorSrc:
        for dstMirror in s1MirrorDst:
            forwardFlow.actions.append(of.ofp_action_output(port=dstMirror))
    return forwardFlow


def _simulateTraffic(portPairs, switch):
    print "***Simulating Traffic flow for switch %s" % str(switch)
    for pair in portPairs:
        srcPort, dstPort = pair[0], pair[1]
        print "Pushing flow from %s to %s" % (srcPort, dstPort)
        core.openflow.getConnection(switch).send(_PortFlowMod(srcPort, dstPort, timeout, \
            mirrorSrc=s1MirrorSrc, mirrorDst=s1MirrorDst))
        core.openflow.getConnection(switch).send(_PortFlowMod(dstPort, srcPort, timeout, \
            mirrorSrc=s2MirrorSrc, mirrorDst=s2MirrorDst))


def _handle_pytap (event):
    # packet is an instance of class 'pox.lib.packet.ethernet.ethernet'
    packet = event.parsed
    #print packet.dst, packet.src

    #each switch is a separate conneciton object
    for conn in core.openflow.connections: 
        print "Switch %s with DPID %s is connected" % (conn, conn.dpid)

    # push static flows from agg switche ports to packet inspection host
    print "***Pushing static flow on switch " + str(core.openflow.getConnection(3).dpid)
    for port in range(1,11):
        core.openflow.getConnection(3).send(_PortFlowMod(port,11,timeout, [], []))

    # simulation s1 traffic flows
    _simulateTraffic(s1PortPairs, 1)

    # simulation s2 traffic flows 
    _simulateTraffic(s2PortPairs, 2)


# function that is invoked upon load to ensure that listeners are
# registered appropriately.  
def launch ():
    core.openflow.addListenerByName("PacketIn", _handle_pytap)
    log.info("PyTapDEMON is running.")
    
    reactor.listenTCP(8000, EchoFactory())
    reactor.run()

