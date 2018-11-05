PyTapDEMON
==========

Python-based OpenFlow Distributed Ethernet Monitoring System

**[11/05/2018 Update] This was an old project that I developed a number of years ago using OpenFlow, POX, and Mininet. If there is enough interest, I would be open to take the next step forward with perhpas Ryu controller, physical switches, and OpenFlow 1.3 and above.**

PyTapDEMON is a project from my Python class at University of Washington Extension in 2013. It is a Distributed Ethernet MOnitoring (DEMon) prototype system using OpenFlow-enabed switch with POX as the controller. It is not a new concept, my friend Rich Groves presented this project at Sharkfest. There is a number of reports and commercial offerings based on this idea. 

* [Microsoft uses OpenFlow SDN for network monitoring and analysis](https://searchsdn.techtarget.com/news/2240181908/Microsoft-uses-OpenFlow-SDN-for-network-monitoring-and-analysis)
* [SDN Packet Broker](https://blog.sflow.com/2013/04/sdn-packet-broker.html)
* [Rich's Sharkfest 2012 Presentation](https://sharkfestus.wireshark.org/sharkfest.12/presentations/A-4_Leveraging_Openflow_to_create_a_Large_Scale_and_Cost_Effective_Packet_Capture_Network.pdf)
* For more related links, please see the [blog post](http://blog.pythonicneteng.com/2013/04/introducing-pytapdemon.html)

## Overview

The concept is simple, having an on-demand OpenFlow-enabled access and aggregation layer that is directed by the controller to send relevant traffic to a deep packet analyzer. The differentiator is the fact that OpenFlow can match the packet at a much deeper level compare to traditional switches, therefore allowing more surgical match action. 

![PyTapDEMON Overview](https://github.com/ericchou-python/PyTapDEMON/blob/master/Graphs/Overview.png "PyTapDEMON Overview")

The prototype mainly uses Mininet to simulate the network and POX controller and OpenFlow 1.0 messages. For more information on the background, you can check out this [post](http://blog.pythonicneteng.com/2013/04/introducing-pytapdemon.html). 

## Usage

Unfortunately, as prototype goes, there are some rough edges around this project, e.g. you can't just 'pip install' the code. It requires some knowledge with OpenFlow 1.0 specifications, Mininet, and POX controller. All the necessary links are included in the posts linked below. 

However, it is a working prototype as you can find the screencast in the [this post](http://blog.pythonicneteng.com/2013/04/pytapdemon-part-2-prototype.html). 

## Prototype

The prototype consist of a custom Mininet config (included in this repo) with 2 filter switches (s1 and s2) with 5 hosts each (h1-h5 on s1, h6-h10 on s2), 5x uplinks aggregation switch (s3), and a capture host (h11) attached to Eth11 on s3: 

![Mininet Normal State](https://github.com/ericchou-python/PyTapDEMON/blob/master/Graphs/PyTapDEMON_Original.gv.png)

The Red link indicates the 'always forward' state. For example, eth6 will always forward to eth1 on s3 and s3 will always forward all traffic from eth1-10 to eth11 to the capture host.

Here is the simulation state:

![Mininet Simulated State](https://github.com/ericchou-python/PyTapDEMON/blob/master/Graphs/PyTapDEMON_Simulate.gv.png)

On s1, (port 1 / port 2) and (port 3 / port 4) will always forward traffic to each other. On s2, (port 1 / port 2) will forward traffic to each other. Switch s1 traffic on eth1 will be mirrored to eth6 and switch s2 eth2 traffic will be mirrored to eth7. To keep things simple, only 1 link on the mirrored is picked so I dont see the same traffic multiple times and eth3/eth4 traffic on s1 is not mirrored to show isolation.

For a more detailed explaination and screencast of the demonstration, please check out this [post](http://blog.pythonicneteng.com/2013/04/pytapdemon-part-2-prototype.html).

## sFlow-RT Integration

If you have read to this far, you must be wondering if instead of static monitoring, we can integrate dynamic monitoring based on traffic pattern. I used the sFlow-RT for this purpose, at the time, the virtual switch only supports sFlow for flow-based monitoring (I believe this is still the case). 

For more information, you can check out this [post](http://blog.pythonicneteng.com/2013/05/pytapdemon-part-3-pro-active-monitoring.html).

## Unittest Integration

For part 4, I will attempt to write some testing for the project. Of course, as part of the TDD approach, this really should have been either part 2 of the project, or be integrated into all the steps during the development. But how many of us really write the tests first? So here I am, trying to write some tests. :)

To be honest, in my opinion, this is part of the larger problem that it is hard to write tests against code that either make changes to the network or monitors the network. The network is inherently distributed and traditionally been stateless from one another. Such as the case here, for the test, I can write test to test my code; or I can write test to query the network and see if it is in an expected state. If I have time, I should do both, but comparing the two, I have decided to write test for the network state because ultimately that is what I care about the most. 

The objectives are simple: 

1. Query the switches for the current flow information. 
2. Compare them to the expected port-based flow data. 

For more information, you can check out this [post](http://blog.pythonicneteng.com/2013/05/pytapdemon-part-4-unittest-for-your.html).

## Misc Tools

I developed various scripts and tools for the project with the intention of making them into more baked features such as Scapy and DPKT Ping Test. However, they remained to be half-baked at this time. I am putting them in this[post](http://blog.pythonicneteng.com/2013/05/pytapdemon-part-5-misc-tools.html) for now, if they ever grow into a post of their own I will remove them from here.

If you are interested in this project, let me know via [Twitter](https://twitter.com/ericchou?lang=en) or [LinkedIn](https://www.linkedin.com/in/choueric/)!


