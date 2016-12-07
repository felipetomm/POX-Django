#!/bin/python2.7
import os
import commands


#REALIZA A COLETA DOS SWITCHES
def scd_get_switches():
    dump_switches = commands.getoutput("ovs-vsctl show | grep Bridge | cut -f2 -d'\"'")
    lista_dump_switches = dump_switches.splitlines()
    lista_switches = []

    for switch in lista_dump_switches:
        lista_switches.append(switch)
    return lista_switches


#INICIO DA COLETA
if __name__=="__main__":
    #INICIA COLETANDO OS SWITCHES
    switches = scd_get_switches()
    for switch in switches:
        for i in range(0,2048):
            commands.getoutput("ovs-ofctl add-flow %s nw_src=172.16.32.1,dl_src=00:00:00:00:00:04,dl_dst=00:00:00:00:00:05,in_port=%s,priority=1,actions=normal"%(switch,i))