#!/usr/bin/env python
from scapy.all import *

def parsePacket(pkt):
    if pkt.haslayer(Ether):
         print "Found Ethernet packet"
         print str(pkt[Ether].dst)

if __name__ == "__main__":
    sniff(prn=parsePacket, store=0)
