#!/usr/bin/env python

"""
Mininet: sudo mn --topo single,3 --mac --switch ovsk --controller remote
"""

# These next two imports are common POX convention
from pox.core import core
import pox.openflow.libopenflow_01 as of

# Even a simple usage of the logger is much nicer than print!
log = core.getLogger()

# Method for just sending a packet to any port (broadcast by default)
def send_packet (event, dst_port = of.OFPP_ALL):
  msg = of.ofp_packet_out(in_port=event.ofp.in_port)
  if event.ofp.buffer_id != -1 and event.ofp.buffer_id is not None:
    # We got a buffer ID from the switch; use that
    msg.buffer_id = event.ofp.buffer_id
  else:
    # No buffer ID from switch -- we got the raw data
    if event.ofp.data:
      # No raw_data specified -- nothing to send!
      return
    msg.data = event.ofp.data
  msg.actions.append(of.ofp_action_output(port = dst_port))
  event.connection.send(msg)

# Establish flows with static port 1 to port 2
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
      forwardFlow.idle_timeout = 120
      forwardFlow.hard_timeout = 120
      forwardFlow.match.in_port = 1
      forwardFlow.actions.append(of.ofp_action_output(port=2))
      event.connection.send(forwardFlow)

      # build the flow from port 2 to port 1
      returnFlow = of.ofp_flow_mod()
      returnFlow.idle_timeout = 120
      returnFlow.hard_timeout = 120
      returnFlow.match.in_port = 2
      returnFlow.actions.append(of.ofp_action_output(port=1))
      event.connection.send(returnFlow)

      log.debug("Installing flow from Port 1 to Port 2")

  send_packet(event, dst_port=3)
  log.debug("Sending event packet to mirror port")

# function that is invoked upon load to ensure that listeners are
# registered appropriately.  
def launch ():
  core.openflow.addListenerByName("PacketIn", _handle_pytap)

  log.debug("pytap is running.")

