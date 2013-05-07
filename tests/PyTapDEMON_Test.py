#!/usr/bin/env python
#
# This test uses out of band ovs-ofctl to query the 
# switches and compare to an existing state to see
# if the flows are installed correctly in the PyTapDEMon
# topology. 
#

import unittest
import subprocess

def parseFlows(flows):
    """
    Parse out the string representation of flows passed in. 
    Example: 
    NXST_FLOW reply (xid=0x4):
     cookie=0x0, duration=4.329s, table=0, n_packets=0, n_bytes=0, idle_timeout=120,hard_timeout=120,in_port=3 actions=output:4
    """
    switchFlows = {}
    for flow in flows.split('\n'):
        line = flow.split()
        if len(line) > 3: #get rid of first line in flow output
            inputPort = line[5].split(',')[2].split('=')[1]
            outputPorts = line[6].split('actions=')[1]
            switchFlows[inputPort] = outputPorts
    return switchFlows
     

globalFlows = {}
for i in range(1, 4):
    """Query switches s1, s2, s3 and dump flows, add to global flow dictionary"""
    switch = 's'+str(i)
    flows = subprocess.check_output(['sudo', 'ovs-ofctl', 'dump-flows', switch])
    switchFlows = parseFlows(flows)
    globalFlows[switch] = switchFlows


class PyTapDEMON_Test(unittest.TestCase):
    def test_s1_port1(self):
        self.assertEqual('output:2,output:6,output:8', globalFlows['s1']['1'])
    
    def test_s2_port1(self):
        self.assertEqual('output:2,output:6,output:8', globalFlows['s2']['1'])

    def test_s3_port10(self):
        self.assertEqual('output:11', globalFlows['s3']['10'])


if __name__ == '__main__':
    unittest.main()
