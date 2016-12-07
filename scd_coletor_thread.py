#!/bin/python2.7
from __builtin__ import id

import os
import commands
from netaddr import IPNetwork
from scd_new_analisador_conflitos import analise_Conflito
import time
from threading import Thread
import threading, Queue

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scd.settings")
from django.core.management import execute_from_command_line
from django.db.models import Count
import django.db.models.query
import django
import datetime
from django.shortcuts import render
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.template import RequestContext
from array import *
from django.db.models import *
from django.db.models import F
from datetime import timedelta
from django.utils import timezone
from django.db.models import Count
from django.db.models import Sum, Avg
from datetime import datetime

from scd import settings
from scd.scd_app.models import *
"""TERMINA INPORTACAO DJANGO"""


django.setup()


#DEFINE OS CAMPOS UTILIZADOS NA COLETA
class scd_flows(object):
    def __init__(self):

        self.flow_id = None
        self.switch = None
        self.nw_src = None
        self.nw_dst = None
        self.nw_src_full = None
        self.nw_dst_full = None
        self.nw_src_mask = None
        self.nw_dst_mask = None
        self.nw_proto = None
        self.nw_tos = None

        self.dl_src = None
        self.dl_dst = None
        self.dl_type = None
        self.dl_vlan = None

        self.actions = None
        self.table = None
        self.in_port = None
        self.priority = None
        self.idle_timeout = None
        self.hard_timeout = None

        self.tp_src = None
        self.tp_dst = None

        self.conflito = []
        self.conflito_sugestao = []
        self.conflito_nivel = []


#REALIZA A COLETA DOS FLUXOS DO SWITCH ESPECIFICADO
def scd_get_flows(switch):
    dump_flow = commands.getoutput("ovs-ofctl dump-flows %s | grep -v NXST_FLOW | sed '/^$/d'"%switch)
    list_flows = dump_flow.splitlines()

    lista_flows = []
    lista_flow = []
    lista_aux = []
    for flow in list_flows:
        lista_f = flow.replace(' ',',').split(',')
        for x in lista_f:
            lista_aux = x.split('=')
            if lista_aux.__len__() ==2:
                dicio_flow = {lista_aux[0]:lista_aux[1]}
            else:
                dicio_flow = {lista_aux[0]:lista_aux[0]}
            lista_flow.append(dicio_flow)
        lista_flows.append(lista_flow)
        lista_flow = []
    return lista_flows

#REALIZA A COLETA DOS SWITCHES
def scd_get_switches():
    dump_switches = commands.getoutput("ovs-vsctl show | grep Bridge | cut -f2 -d'\"'")
    lista_dump_switches = dump_switches.splitlines()
    lista_switches = []

    for switch in lista_dump_switches:
        lista_switches.append(switch)
    return lista_switches

def scd_func_thread(scd_flow_main_list,flow1, queue):
    for flow2 in scd_flow_main_list:
        #Verifica se nao eh a mesma regra (mesma posicao da lista)
        #Se as regras forem diferentes, faz a analise
        #if flow_1 != flow_2:
        if flow1 != flow2:
            scd_verifica_conflito = analise_Conflito(flow1,flow2)
            if scd_verifica_conflito.sugestao_resolucao != None:
                flow1.conflito_nivel.append(scd_verifica_conflito.nivel_conflito)
                flow1.conflito_sugestao.append(scd_verifica_conflito.sugestao_resolucao)
                flow1.conflito.append(flow2.flow_id)
            scd_verifica_conflito = None
        queue.put(flow1)

#INICIO DA COLETA
if __name__=="__main__":

    #INICIA COLETANDO OS SWITCHES
    switches = scd_get_switches()
    #VARIAVEL PARA COLETAR OS FLOWS
    scd_flow_main_list = []
    print ("Iniciando Modulo de Coleta")
    tempo_ini = time.clock()
    for switch in switches:
        flow_match = scd_get_flows(switch)

        count = flow_match.__len__()
        for i in range(0,count):
            #RECEBE OS CAMPOS DO MATCH
            scd_flow_flows = scd_flows()
            scd_flow_flows.switch = switch
            for flows in flow_match[i]:
                scd_flow_flows.flow_id = ("%s-%s"%(switch,i))
                if 'in_port' in flows:      scd_flow_flows.in_port =      flows['in_port']
                if 'priority' in flows:     scd_flow_flows.priority =     flows['priority']
                if 'table' in flows:        scd_flow_flows.table =        flows['table']
                if 'actions' in flows:      scd_flow_flows.actions =      flows['actions']
                if 'idle_timeout' in flows: scd_flow_flows.idle_timeout = flows['idle_timeout']
                if 'hard_timeout' in flows: scd_flow_flows.hard_timeout = flows['hard_timeout']

                if 'dl_vlan' in flows:  scd_flow_flows.dl_vlan = flows['dl_vlan']
                if 'dl_src' in flows:   scd_flow_flows.dl_src =  flows['dl_src']
                if 'dl_dst' in flows:   scd_flow_flows.dl_dst =  flows['dl_dst']

                #CONSULTAR MANUAL OVS-OFCTL - SAO OS PROTOCOLOS QUE PODEM SER ESPECIFICADOS
                if 'dl_type' in flows:  scd_flow_flows.dl_type = flows['dl_type']
                #####ARP/RARP/ICMP - NAO ANALISA PORTA TCP
                #dl_type=0x0806.
                elif 'arp' in flows:    scd_flow_flows.dl_type = flows['arp']
                #dl_type=0x8035.
                elif 'rarp' in flows:   scd_flow_flows.dl_type = flows['rarp']
                #dl_type=0x0800,nw_proto=1.
                elif 'icmp' in flows:   scd_flow_flows.dl_type = flows['icmp']
                #####
                #####IP/TCP/UDP/SCTP - PROTOCOLOS QUE SAO INFORMADAS AS PORTAS TCP/UDP
                #dl_type=0x0800.
                elif 'ip' in flows:     scd_flow_flows.dl_type = flows['ip']
                #dl_type=0x0800,nw_proto=6.
                elif 'tcp' in flows:    scd_flow_flows.dl_type = flows['tcp']
                #dl_type=0x0800,nw_proto=17.
                elif 'udp' in flows:    scd_flow_flows.dl_type = flows['udp']
                #dl_type=0x0800,nw_proto=132.
                elif 'sctp' in flows:   scd_flow_flows.dl_type = flows['sctp']

                if 'nw_src' in flows:
                    if flows['nw_src'].find("/"):
                        aux_nw = []
                        aux_nw_mask_lista = []
                        aux_nw_mask_str = None

                        ip_src = IPNetwork(flows['nw_src'])
                        scd_flow_flows.nw_src_full = ip_src

                        #COLETA ENDERECO IP (QUEBRA OS 4 CAMPOS)
                        for ip in ip_src.ip.words:
                            aux_nw.append(ip)

                        #COLETA NETMASK
                        aux_nw_mask_str = str(ip_src.netmask).split('.')
                        for mask in aux_nw_mask_str:
                            aux_nw_mask_lista.append(mask)

                        #ATRIBUI O VALOR PARA AS VARIAVEIS
                        scd_flow_flows.nw_src = aux_nw
                        scd_flow_flows.nw_src_mask = aux_nw_mask_lista

                if 'nw_dst' in flows:
                    if flows['nw_dst'].find("/"):
                        aux_nw = []
                        aux_nw_mask_lista = []
                        aux_nw_mask_str = None

                        ip_dst = IPNetwork(flows['nw_dst'])
                        scd_flow_flows.nw_dst_full = ip_dst
                        #COLETA ENDERECO IP (QUEBRA OS 4 CAMPOS)
                        for ip in ip_dst.ip.words:
                            aux_nw.append(ip)

                        #COLETA NETMASK
                        aux_nw_mask_str = str(ip_dst.netmask).split('.')
                        for mask in aux_nw_mask_str:
                            aux_nw_mask_lista.append(mask)

                        #ATRIBUI O VALOR PARA AS VARIAVEIS
                        scd_flow_flows.nw_dst = aux_nw
                        scd_flow_flows.nw_dst_mask = aux_nw_mask_lista

                if 'nw_proto' in flows: scd_flow_flows.nw_proto = flows['nw_proto']
                if 'nw_tos' in flows:   scd_flow_flows.nw_tos = flows['nw_tos']
                if 'tp_src' in flows:   scd_flow_flows.tp_src = flows['tp_src']
                if 'tp_dst' in flows:   scd_flow_flows.tp_dst = flows['tp_dst']

            scd_flow_main_list.append(scd_flow_flows)
            scd_flow_flows = None
    print ("Modulo de Coleta demorou: %s" %(time.clock()-tempo_ini))
    #VARIAVEL UTILIZADA PARA RECEBER O RETORNO DA ANALISE DE CONFLITO
    scd_verifica_conflito = None
    i = 0
    count = scd_flow_main_list.__len__()

    print ("Iniciando Modulo de Verificacao")
    tempo_ini = time.clock()

    #var para thread
    queued_request = Queue.Queue()

    #INICIO DA VERIFICACAO DOS FLOWS PARA A DETECCAO DE CONFLITO
    #for flow_1 in scd_flow_main_list:
    for flow in scd_flow_main_list:
        #TENTATIVA DE PARALELIZACAO
        scd_thread = threading.Thread(target=scd_func_thread, args=(scd_flow_main_list,flow,queued_request))
        print scd_thread.name
        print queued_request.get()
        flow = queued_request.get()

    print ("Modulo de Verificacao demorou: %s" %(time.clock()-tempo_ini))

    print ("Iniciando Gravacao das Informacoes na Base de Dados")
    tempo_ini = time.clock()

    #INICIA A GRAVACAO NO BANCO DE DADOS
    #LIMPA AS TABELAS DA BASE DE DADOS
    dj_comutador    = ScdComutador.objects.all().delete()
    dj_flow         = ScdFlow.objects.all().delete()
    df_conflito     = ScdConflito.objects.all().delete()

    #VARIAVEL QUE DETERMINA O IDENTIFICADOR DO SWITCH
    i=1
    django.setup()
    """
    #REALIZA O INSERT DOS SWITCHES NA TABELA SCD_COMUTADOR
    for switch in switches:
        dj_comutador = ScdComutador.objects.create(comut_id=i,comut_nome=switch)
        dj_comutador.save()
        i += 1

    #REALIZA O INSERT DAS REGRAS NA TABELA SCD_FLOWS
    for flow in scd_flow_main_list:
        switch = ScdComutador.objects.get(comut_nome=flow.switch)
        dj_flow = ScdFlow.objects.create(fl_id=flow.flow_id,fl_flowtable=flow.table,\
                                                id_comutador_id=switch.comut_id,fl_dl_dst=flow.dl_dst,\
                                                fl_dl_src=flow.dl_src,fl_dl_vlan=flow.dl_vlan,\
                                                fl_dl_type=flow.dl_type,fl_nw_src=flow.nw_src_full,\
                                                fl_nw_dst=flow.nw_dst_full,fl_nw_tos=flow.nw_tos,\
                                                fl_nw_proto=flow.nw_proto,fl_in_port=flow.in_port,\
                                                fl_tp_src=flow.tp_src,fl_tp_dst=flow.tp_dst,fl_priority=flow.priority,\
                                                fl_idle_timeout=flow.idle_timeout,fl_hard_timeout=flow.hard_timeout,\
                                                fl_actions=flow.actions)
        dj_flow.save()

    #REALIZA O INSERT DOS CONFLITOS NA TABELA SCD_CONFLITOS
    for flow in scd_flow_main_list:
        count = flow.conflito.__len__()
        for j in range(0,count):
            dj_conflito = ScdConflito.objects.create(con_sugestao=flow.conflito_sugestao[j],\
                                                     con_nivel=flow.conflito_nivel[j],\
                                                     con_flow_principal_id=flow.flow_id,\
                                                     con_flow_analisada_id=flow.conflito[j])
            dj_conflito.save()"""
    print scd_flow_main_list.__len__()
    print scd_flow_main_list[0].flow_id
    print scd_flow_main_list[1].flow_id
    print scd_flow_main_list[2].flow_id
    print scd_flow_main_list[3].flow_id
    print scd_flow_main_list[4].flow_id
    print scd_flow_main_list[5].flow_id
    print scd_flow_main_list[6].flow_id
    print ("Processo de gravar na Base demorou: %s" %(time.clock()-tempo_ini))