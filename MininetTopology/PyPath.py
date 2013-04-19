#!/usr/bin/env python

"""
author: Eric Chou (@ericchou)

Programmable Patch Panel 2x 64-port switch with
the last 32 ports connected back-to-back

"""

from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel

def PyPath():

    net = Mininet( switch=OVSSwitch, build=False)

    print "** Creating controllers"
    c1 = net.addController('c1', port=6633)

    print "*** Creating switches"
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')

    print "*** Creating hosts"
    host1 = [ net.addHost('h%d' % n) for n in range(1,33)] #hosts for switch1
    host2 = [ net.addHost('h%d' % n) for n in range(33,65)] #hosts for switch2

    print "*** Creating links"
    for h in host1:
        net.addLink (s1, h)
    for h in host2:
        net.addLink (s2, h)
    for i in range(1,33): #links for back-to-back connection
        net.addLink(s1, s2)

    print "*** Starting network"
    net.build()
    s1.start ( [ c1 ])
    s2.start ( [ c1 ])

    print "*** Running CLI"
    CLI( net )
 
if __name__ == '__main__':
    setLogLevel('info')
    PyPath()

