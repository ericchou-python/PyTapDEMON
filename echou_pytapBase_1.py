#!/usr/bin/env python
""" Mininet: sudo mn --topo single,3 --mac --switch ovsk --controller remote
"""

# These next two imports are common POX convention
from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.addresses import IPAddr, EthAddr


# Even a simple usage of the logger is much nicer than print!
log = core.getLogger()

def _handle_pytap (event):
  # packet is an instance of class 'pox.lib.packet.ethernet.ethernet'
  packet = event.parsed
  print packet.dst, packet.src

  #
  # Learn the source 
  srcPort = event.port

  if srcPort == 1 or srcPort == 2:
      # build the flow from port 1 to port 2
      forwardFlow = of.ofp_flow_mod()
      forwardFlow.idle_timeout = 10
      forwardFlow.hard_timeout = 10
      forwardFlow.match.nw_dst = IPAddr("192.168.100.2")
      log.debug("Packet toward 192.168.100.2")
      forwardFlow.match.in_port = 1
      forwardFlow.actions.append(of.ofp_action_nw_addr.set_dst(IPAddr("192.168.100.2")))
      forwardFlow.actions.append(of.ofp_action_dl_addr.set_dst(EthAddr("<masked>")))
      forwardFlow.actions.append(of.ofp_action_output(port=2))
      forwardFlow.actions.append(of.ofp_action_output(port=3))
      event.connection.send(forwardFlow)
      
      log.debug("Installing flow from port 1 to port 2")
      
      # build the flow from port 2 to port 1
      returnFlow = of.ofp_flow_mod()
      returnFlow.idle_timeout = 10
      returnFlow.hard_timeout = 10
      returnFlow.match.nw_dst = IPAddr("192.168.100.1")
      returnFlow.match.in_port = 2
      returnFlow.actions.append(of.ofp_action_nw_addr.set_dst(IPAddr("192.168.100.1")))
      returnFlow.actions.append(of.ofp_action_dl_addr.set_dst(EthAddr("<masked>")))
      returnFlow.actions.append(of.ofp_action_output(port=1))
      event.connection.send(returnFlow)

      log.debug("Installing flow from port 2 to port 1")


# function that is invoked upon load to ensure that listeners are
# registered appropriately.  
def launch ():
  core.openflow.addListenerByName("PacketIn", _handle_pytap)

  log.debug("pytap is running.")

