#!/usr/bin/env python
#
# This test passively sniffs 
# and look for Ethernet packets 
# using Scapy. 
#
# This is meant to be used on the sniffing 
# host, h11 in the PyTapDEMon prototype 
# setup. 
#

from scapy.all import *

def parsePacket(pkt):
    if pkt.haslayer(Ether):
         print "Found Ethernet packet"
         print str(pkt[Ether].dst)

if __name__ == "__main__":
    sniff(prn=parsePacket, store=0)
