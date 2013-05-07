#!/usr/bin/env python
#
# Example from:
# http://www.secdev.org/projects/scapy/build_your_own_tools.html
#
# This is meant to be executed on h1 to ping toward h2
# 

from scapy.all import sr1, IP, ICMP

dstIP = '10.0.0.2'

packet = sr1(IP(dst=dstIP)/ICMP())
if packet:
    packet.show()


