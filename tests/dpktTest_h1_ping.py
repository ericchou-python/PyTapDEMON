#!/usr/bin/env python
#
# Example from: 
# http://jon.oberheide.org/blog/2008/08/25/dpkt-tutorial-1-icmp-echo/
# 
# More documentation: 
# http://www.commercialventvac.com/dpkt.html#mozTocId305148
#
# This file sends ICMP packet to the destination host. 
# This is meant to be run on h1 to generate interesting traffic. 
# It has the same affect as Mininet "h1 ping h2"
# 

import dpkt
import socket, random

echo = dpkt.icmp.ICMP.Echo()
echo.id = random.randint(0, 0xffff)
echo.seq = random.randint(0, 0xffff)
echo.data = 'hello world'

icmp = dpkt.icmp.ICMP()
icmp.type = dpkt.icmp.ICMP_ECHO
icmp.data = echo

destination = '10.0.0.2'
s = socket.socket(socket.AF_INET, socket.SOCK_RAW, dpkt.ip.IP_PROTO_ICMP)
s.connect((destination, 1))
sent = s.send(str(icmp))

print 'sent %d bytes to %s' % (sent, destination)

