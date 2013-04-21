#!/usr/bin/env python

from pox.core import core
from pox.lib.addresses import IPAddr, EthAddr

class MyComponent (object):
    def __init__ (self, an_arg):
        self.arg = an_arg
        print "MyComponent instance registered with arg: ", self.arg

    def foo (self):
        print "MyComponent with arg:", self.arg
    
    def ip (self):
        ip = IPAddr("192.168.1.1")
        print str(ip)
        print ip.toUnsignedN() # converts to network-order unsigned integer 16885952
        print ip.toRaw() # returns a length-four bytes object 
        print "*****"
        ip = IPAddr(16885952, networkOrder=True)
        print str(ip)

def launch ():
    core.registerNew(MyComponent, "spam")
    core.MyComponent.foo()
    core.MyComponent.ip()

