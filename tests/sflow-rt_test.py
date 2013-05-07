#!/usr/bin/env python
#
# This file queries the sflow-rt tool at 192.168.56.1 (host)
# which already has TCP filter setup to capture all TCP traffic
# from switch sflow exports. 
# 
# If TCP traffic is detected, ovs-ofctl will push down port-based
# flows to allow port 3 <> port 4 bi-dir flows on s2 (h8 and h9)
# as well as mirror port 4 traffic toward port 7 (toward s3). 
#

import json
import urllib2
import subprocess

data = json.load(urllib2.urlopen('http://192.168.56.1:8008/metric/ALL/tcp/json'))

# if TCP traffic is detected
if 'topKeys' in data[0]:
    info =  data[0]['topKeys'][0]['key']
    dst, src, dstPort, srcPort = info.split(',')
    # install flows to s2 for h8 and h9
    # port 4 will also duplicate traffic to port 7 mirror port
    subprocess.call(['sudo','ovs-ofctl','add-flow','s2','hard_timeout=120,in_port=4,actions=output:3,output:7'])
    subprocess.call(['sudo','ovs-ofctl','add-flow','s2','hard_timeout=120,in_port=3,actions=output:4'])

