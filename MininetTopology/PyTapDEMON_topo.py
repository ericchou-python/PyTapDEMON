#!/usr/bin/env python

"""
author: Eric Chou (@ericchou)

1. 2x port Filter Switches with 5 hosts and 5 trunk ports.
2. 1x port Aggregation Switch with 10 trunk ports and Deep inspection host

"""

from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel

def PyTapDEMON():

    net = Mininet( switch=OVSSwitch, build=False)

    print "** Creating controllers"
    c1 = net.addController('c1', port=6633)

    print "*** Creating switches"
    s1 = net.addSwitch('s1', listenPort=6634)
    s2 = net.addSwitch('s2', listenPort=6635)
    s3 = net.addSwitch('s3', listenPort=6636)

    print "*** Creating hosts"
    host1 = [ net.addHost('h%d' % n) for n in range(1,6)]
    host2 = [ net.addHost('h%d' % n) for n in range(6,11)]
    host3 = net.addHost('h11')

    print "*** Creating links"
    for h in host1:
        net.addLink (s1, h)
    for h in host2:
        net.addLink (s2, h)
    for i in range(1,6):
        net.addLink(s1, s3)
    for i in range(1,6):
        net.addLink(s2, s3)
    net.addLink(host3, s3)

    print "*** Starting network"
    net.build()
    s1.start ( [ c1 ])
    s2.start ( [ c1 ])
    s3.start ( [ c1 ])

    print "*** Running CLI"
    CLI( net )
 
if __name__ == '__main__':
    setLogLevel('info')
    PyTapDEMON()


