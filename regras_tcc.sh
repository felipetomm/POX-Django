#!bin/bash

sudo ovs-ofctl add-flow s1 tcp,in_port=3,nw_src=10.0.0.0/8,nw_dst=10.0.0.2,priority=3000,actions=normal
sudo ovs-ofctl add-flow s1 tcp,nw_src=10.0.0.2,nw_dst=10.0.0.1,priority=3000,actions=normal
sudo ovs-ofctl add-flow s1 tcp,in_port=3,nw_src=10.0.0.100,nw_dst=10.0.0.1,tp_src=80,priority=3000,actions=normal
sudo ovs-ofctl add-flow s1 tcp,nw_src=10.0.0.0,priority=42,tp_dst=22,actions=normal
sudo ovs-ofctl add-flow s1 tcp,nw_dst=192.168.101.150,tp_dst=443,tp_src=80,priority=42,actions=normal
sudo ovs-ofctl add-flow s1 tcp,nw_src=191.10.10.150,nw_dst=192.168.10.150,tp_dst=445,tp_src=81,priority=41,actions=normal
sudo ovs-ofctl add-flow s1 arp,dl_src=00:00:00:00:00:01,dl_dst=00:00:00:00:00:02,in_port=3,priority=45,actions=normal

