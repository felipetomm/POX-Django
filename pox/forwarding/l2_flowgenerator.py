import grp
from pox.core import core
from pox.lib.util import dpid_to_str, str_to_bool
from pox.lib.revent.revent import *
import pox.openflow.libopenflow_01 as of
import pox.openflow.of_service as of_service
import pox.lib.packet as pkt
from pox.lib.addresses import IPAddr, EthAddr
from pox.lib.addresses import *
from random import randrange
from pox.lib.recoco import Timer
from pox.openflow.flow_table import FlowTable, TableEntry
from pox.openflow.of_json import *
from pox.openflow import OpenFlowNexus

from netaddr import IPNetwork

log = core.getLogger()


def _handle_ConnectionUp(event):
    log.debug("Switch %s esta UP" % (dpid_to_str(event.dpid)))

    ##REGRA 01.01 - IDENTICAS
    msg1 = of.ofp_flow_mod()
    msg1.match.in_port= 3
    msg1.table_id = 0x1
    msg1.priority = 3000
    msg1.match.dl_type = 0x800
    msg1.match.nw_proto = 6
    msg1.match.nw_src = "10.0.0.0/8"
    msg1.match.nw_dst = "10.0.0.2"
    msg1.actions.append(of.ofp_action_output(port = of.OFPP_ALL))
    event.connection.send(msg1)

    msg1 = of.ofp_flow_mod()
    msg1.table_id = 0x1
    msg1.priority = 3000
    msg1.match.dl_type = 0x800
    msg1.match.nw_proto = 6
    msg1.match.nw_src = "10.0.0.2"
    msg1.match.nw_dst = "10.0.0.1"
    msg1.actions.append(of.ofp_action_output(port = of.OFPP_ALL))
    event.connection.send(msg1)

    ##REGRA 01.02
    msg2 = of.ofp_flow_mod()
    msg2.match.in_port = 3
    msg2.priority = 3000
    msg2.match.dl_type = 0x800
    msg2.match.nw_proto = 6
    msg2.match.nw_src = "10.0.0.100"
    msg2.match.nw_dst = "10.0.0.1"
    msg2.match.tp_src = 80
    msg2.actions.append(of.ofp_action_output(port=4))
    event.connection.send(msg2)

    msg3 = of.ofp_flow_mod()
    msg3.priority = 42
    msg3.match.dl_type = 0x800
    msg3.match.nw_proto = 6
    msg3.match.nw_src = "10.0.0.0"
    msg3.match.tp_dst = 22
    event.connection.send(msg3)

    msg4 = of.ofp_flow_mod()
    msg4.priority = 42
    msg4.match.dl_type = 0x800
    msg4.match.nw_proto = 6
    msg4.match.nw_dst = "192.168.101.150"
    msg4.match.tp_dst = 443
    msg4.match.tp_src = 80
    msg4.actions.append(of.ofp_action_output(port=4))
    event.connection.send(msg4)

    #Esta ultima regra nao pode conflitar
    msg5 = of.ofp_flow_mod()
    msg5.priority = 41
    msg5.match.dl_type = 0x800
    msg5.match.nw_proto = 6
    msg5.match.nw_src = "191.10.10.150"
    msg5.match.nw_dst = "192.168.10.150"
    msg5.match.tp_dst = 445
    msg5.match.tp_src = 81
    event.connection.send(msg5)


    """actionlist = []
    for action in msg4.actions:
        string = action.__class__.__name__ + "["
        string += action.show().strip("\n").replace("\n", ", ") + "]"
        actionlist.append(string)
        print string"""


"""
def analisys_Conflict(pscd_rule_1, pscd_rule_2):
    # Inicia a verificacao das rules

    ##DECLARACAO DAS VARIAVEIS UTILIZADAS NA FUNCTION
    grp_conflito = {'in_port': False, 'ip_src': False, 'ip_dst': False, 'dl_src': False, 'dl_dst': False,
                    'tp_src': False, 'tp_dst': False}

    wildcards_rule_1 = {'in_port': False, 'ip_src': False, 'ip_dst': False, 'dl_src': False, 'dl_dst': False,
                        'tp_src': False, 'tp_dst': False}
    wildcards_rule_2 = {'in_port': False, 'ip_src': False, 'ip_dst': False, 'dl_src': False, 'dl_dst': False,
                        'tp_src': False, 'tp_dst': False}

    wildcards_total_1 = {'in_port': 0, 'ip': 0, 'dl': 0, 'tp': 0}
    wildcards_total_2 = {'in_port': 0, 'ip': 0, 'dl': 0, 'tp': 0}

    regra_generica = {'in_port':False,'ip':False,'dl':False,'tp':False}

    print "Iniciando verificacao de Conflitos"
    print "################################################"

    # Preciso achar um modo de printar as actions
    # teste = of.ofp_flow_wildcards_rev_map.items()
    # pscd_rule_1.match.adjust_wildcards = False
    # teste = pscd_rule_1.match.wildcards
    # print teste

    # print '[%s]' %', '.join(map(str, pscd_rule_1.actions))

    # Verifica a prioridade das regras
    print "------------------------------------"
    print "----> VERIFICA PRIORIDADE"
    print "------------------------------------"
    if pscd_rule_1.priority == pscd_rule_2.priority:
        print "Regras de Mesma PRIORIDADE"
    elif pscd_rule_1.priority < pscd_rule_2.priority:
        print "Regra 1 tem PRIORIDADE MENOR que Regra 2"
    else:
        print "Regra 2 tem PRIORIDADE MENOR que Regra 1"

    # Verifica porta de entrada - GRUPO 1
    ####################################
    print "------------------------------------"
    print "----> VERIFICA IN_PORT"
    print "------------------------------------"
    if type(pscd_rule_1.match._in_port) is tuple or type(pscd_rule_2.match._in_port) is tuple:
        if type(pscd_rule_1.match._in_port) is tuple and type(pscd_rule_2.match._in_port) is int:
            if pscd_rule_2.match._in_port == 0:
                print "Regra 2 IN_PORT Wildcard"
                grp_conflito['in_port'] = True
                wildcards_rule_2['in_port'] = True
            else:
                for in_port in pscd_rule_1.match._in_port:
                    if in_port == pscd_rule_2.match._in_port:
                        print ("Regra 1: In Port iguais Porta: %s" % in_port)
                        grp_conflito['in_port'] = True

        elif type(pscd_rule_2.match._in_port) is tuple and type(pscd_rule_1.match._in_port) is int:
            if pscd_rule_1.match._in_port == 0:
                print "Regra 1 IN_PORT Wildcard"
                grp_conflito['in_port'] = True
                wildcards_rule_1['in_port'] = True
            else:
                for in_port in pscd_rule_2.match._in_port:
                    if in_port == pscd_rule_1.match._in_port:
                        print ("Regra 2: In Port iguais Porta: %s" % in_port)
                        grp_conflito['in_port'] = True
        else:
            for in_port_1 in pscd_rule_1.match._in_port:
                for in_port_2 in pscd_rule_2.match._in_port:
                    if in_port_1 == in_port_2:
                        print ("Regra 1,2: In Port iguais Porta: %s" % in_port_1)
                        grp_conflito['in_port'] = True

    else:
        if pscd_rule_1.match._in_port == 0:
            print "IN_PORT 1 Wildcard"
            wildcards_rule_1['in_port'] = True
            grp_conflito['in_port'] = True
        if pscd_rule_2.match._in_port == 0:
            print "IN_PORT 2 Wildcard"
            wildcards_rule_2['in_port'] = True
            grp_conflito['in_port'] = True
        if (pscd_rule_1.match._in_port != 0 and pscd_rule_2.match._in_port != 0) and (
            pscd_rule_1.match._in_port == pscd_rule_2.match._in_port):
            print "IN_PORT Iguais"
            grp_conflito['in_port'] = True
    print ("Conflito Grupo 1: %s" % grp_conflito['in_port'])

    # Verifica IP_SRC e IP_DST - GRUPO 2
    ###################################
    print "------------------------------------"
    print "----> VERIFICA IP SRC/DST"
    print "------------------------------------"
    ##IP_SRC
    if pscd_rule_1.match.nw_src == pscd_rule_2.match.nw_src:
        print "IP_SRC iguais"
        grp_conflito['ip_src'] = True
        if pscd_rule_1.match.nw_src == None and pscd_rule_2.match.nw_src == None:
            print "IP_SRC 1 e 2 Wildcards"
            wildcards_rule_1['ip_src'] = True
            wildcards_rule_2['ip_src'] = True
    else:
        if pscd_rule_1.match.nw_src == None:
            print "IP_SRC 1 Wildcard"
            grp_conflito['ip_src'] = True
            wildcards_rule_1['ip_src'] = True
        if pscd_rule_2.match.nw_src == None:
            print "IP_SRC 2 Wildcard"
            grp_conflito['ip_src'] = True
            wildcards_rule_2['ip_src'] = True
        elif pscd_rule_1.match.nw_src is not None and pscd_rule_2.match.nw_src is not None:
            mask = 0
            ip1_a, ip1_b, ip1_c, ip1_d = str(pscd_rule_1.match.nw_src).split('.')
            ip2_a, ip2_b, ip2_c, ip2_d = str(pscd_rule_2.match.nw_src).split('.')
            if ip1_a == ip2_a:
                print "Campo A iguais"
                mask = 8
                if ip1_b == ip2_b:
                    print "Campo B iguais"
                    mask = 16
                    if ip1_c == ip2_c:
                        print "Campo C iguais"
                        mask = 24
                        if ip1_d == ip2_d:
                            print "Campo D iguais"
                            mask = 32
            if mask > 0: grp_conflito['ip_src'] = True
            print ("Net_Mask SRC: %s" % mask)
    ##IP_DST
    if pscd_rule_1.match.nw_dst == pscd_rule_2.match.nw_dst:
        print "IP_DST iguais"
        grp_conflito['ip_dst'] = True
        if pscd_rule_1.match.nw_dst == None:
            wildcards_rule_1['ip_dst'] = True
            print "IP_DST 1 Wildcards"
        if pscd_rule_2.match.nw_dst == None:
            wildcards_rule_2['ip_dst'] = True
            print "IP_DST 2 Wildcards"

    else:
        if pscd_rule_1.match.nw_dst == None:
            print "IP_DST 1 Wildcard"
            grp_conflito['ip_dst'] = True
            wildcards_rule_1['ip_dst'] = True
        if pscd_rule_2.match.nw_dst == None:
            print "IP_DST 2 Wildcard"
            grp_conflito['ip_dst'] = True
            wildcards_rule_2['ip_dst'] = True
        elif pscd_rule_1.match.nw_dst is not None and pscd_rule_2.match.nw_dst is not None:
            mask = 0
            ip1_a, ip1_b, ip1_c, ip1_d = str(pscd_rule_1.match.nw_dst).split('.')
            ip2_a, ip2_b, ip2_c, ip2_d = str(pscd_rule_2.match.nw_dst).split('.')
            if ip1_a == ip2_a:
                print "Campo A iguais"
                mask = 8
                if ip1_b == ip2_b:
                    print "Campo B iguais"
                    mask = 16
                    if ip1_c == ip2_c:
                        print "Campo C iguais"
                        mask = 24
                        if ip1_d == ip2_d:
                            print "Campo D iguais"
                            mask = 32
            if mask > 0: grp_conflito['ip_dst'] = True
            print ("Net_Mask DST: %s" % mask)
    print ("Conflito Grupo 2: IP_SRC: %s  IP_DST: %s" % (grp_conflito['ip_src'], grp_conflito['ip_dst']))

    # Verifica MAC_SRC e MAC_DST - GRUPO 3
    #####################################
    print "------------------------------------"
    print "----> VERIFICA MAC SRC/DST"
    print "------------------------------------"
    # Define o MAC Wildcard
    mac_null = "00:00:00:00:00:00"

    # MAC SRC
    if pscd_rule_1.match._dl_src == pscd_rule_2.match._dl_src:
        print "DL_SRC iguais"
        grp_conflito['dl_src'] = True
        if pscd_rule_1.match._dl_src == None: wildcards_rule_1['dl_src'] = True
        if pscd_rule_2.match._dl_src == None: wildcards_rule_2['dl_src'] = True
    else:
        if str(pscd_rule_1.match._dl_src) == mac_null:
            print "DL_SRC 1 Wildcard"
            grp_conflito['dl_src'] = True
            wildcards_rule_1['dl_src'] = True
        else:
            if str(pscd_rule_2.match._dl_src) == mac_null:
                print "DL_SRC 2 Wildcard"
                grp_conflito['dl_src'] = True
                wildcards_rule_2['dl_src'] = True
    # MAC DST
    if pscd_rule_1.match._dl_dst == pscd_rule_2.match._dl_dst:
        print "DL_DST iguais"
        grp_conflito['dl_dst'] = True
        if pscd_rule_1.match._dl_dst == None: wildcards_rule_1['dl_dst'] = True
        if pscd_rule_2.match._dl_dst == None: wildcards_rule_2['dl_dst'] = True
    else:
        if str(pscd_rule_1.match._dl_dst) == mac_null:
            print "DL_DST 1 Wildcard"
            grp_conflito['dl_dst'] = True
            wildcards_rule_1['dl_dst'] = True
        else:
            if str(pscd_rule_2.match._dl_dst) == mac_null:
                print "DL_DST 2 Wildcard"
                grp_conflito['dl_dst'] = True
                wildcards_rule_2['dl_dst'] = True

    print ("Conflito Grupo 3: MAC_SRC: %s  MAC_DST: %s" % (grp_conflito['dl_src'], grp_conflito['dl_dst']))

    # Verifica TP_SRC e TP_DST - GRUPO 4
    print "------------------------------------"
    print "----> VERIFICA PORTA TCP/UDP SRC/DST"
    print "------------------------------------"
    # PORTA TCP/UDP SRC
    if pscd_rule_1.match.tp_src == pscd_rule_2.match.tp_src:
        print "TP_SRC iguais"
        grp_conflito['tp_src'] = True
    else:
        if pscd_rule_1.match.tp_src == None:
            print "TP_SRC 1 Wildcard"
            grp_conflito['tp_src'] = True
            wildcards_rule_1['tp_src'] = True
        else:
            if pscd_rule_2.match.tp_src == None:
                print "TP_SRC 2 Wildcard"
                grp_conflito['tp_src'] = True
                wildcards_rule_2['tp_src'] = True

    # PORTA TCP/UDP DST
    if pscd_rule_1.match.tp_dst == pscd_rule_2.match.tp_dst:
        print "TP_DST iguais"
        grp_conflito['tp_dst'] = True
    else:
        if pscd_rule_1.match.tp_dst == None:
            print "TP_DST 1 Wildcard"
            grp_conflito['tp_dst'] = True
            wildcards_rule_2['tp_dst'] = True
        else:
            if pscd_rule_2.match.tp_dst == None:
                print "TP_DST 2 Wildcard"
                grp_conflito['tp_dst'] = True
                wildcards_rule_2['tp_dst'] = True

    print ("Conflito Grupo 4: TP_SRC: %s  TP_DST: %s" % (grp_conflito['tp_dst'], grp_conflito['tp_dst']))
    print ("----------------------------")
    print ("RESULTADO DAS ANALISES:")
    print ("----------------------------")
    print ("Grupo Conflitos:   %s" % grp_conflito)
    print ("Wildcards Regra 1: %s" % wildcards_rule_1)
    print ("Wildcards Regra 2: %s" % wildcards_rule_2)
    print ("----------------------------")
    print ("----------------------------")

    ##Conta os WildCards
    #REGRA 1
    if wildcards_rule_1['in_port'] == True: wildcards_total_1['in_port'] += 1
    if wildcards_rule_1['dl_src'] == True: wildcards_total_1['dl'] += 1
    if wildcards_rule_1['dl_dst'] == True: wildcards_total_1['dl'] += 1
    if wildcards_rule_1['ip_dst'] == True: wildcards_total_1['ip'] += 1
    if wildcards_rule_1['ip_src'] == True: wildcards_total_1['ip'] += 1
    if wildcards_rule_1['tp_dst'] == True: wildcards_total_1['tp'] += 1
    if wildcards_rule_1['tp_src'] == True: wildcards_total_1['tp'] += 1

    #REGRA 2
    if wildcards_rule_2['in_port'] == True: wildcards_total_2['in_port'] += 1
    if wildcards_rule_2['dl_src'] == True: wildcards_total_2['dl'] += 1
    if wildcards_rule_2['dl_dst'] == True: wildcards_total_2['dl'] += 1
    if wildcards_rule_2['ip_dst'] == True: wildcards_total_2['ip'] += 1
    if wildcards_rule_2['ip_src'] == True: wildcards_total_2['ip'] += 1
    if wildcards_rule_2['tp_dst'] == True: wildcards_total_2['tp'] += 1
    if wildcards_rule_2['tp_src'] == True: wildcards_total_2['tp'] += 1

    #Compara as regras para ver se a regra 1 eh a mais generica
    if wildcards_total_1['in_port'] > wildcards_total_2['in_port']: regra_generica['in_port'] = True
    if wildcards_total_1['ip'] > wildcards_total_2['ip']: regra_generica['ip'] = True
    if wildcards_total_1['dl'] > wildcards_total_2['dl']: regra_generica['dl'] = True
    if wildcards_total_1['tp'] > wildcards_total_2['tp']: regra_generica['tp'] = True

    generica_count = 0
    if regra_generica['in_port']==True: generica_count += 1
    if regra_generica['ip']==True: generica_count += 1
    if regra_generica['tp']==True: generica_count += 1
    if regra_generica['dl']==True: generica_count += 1

    if generica_count >= 3: print ("Regra 1 eh a mais Generica: %s" %generica_count)
    elif generica_count == 2: print ("Regras Genericas: %s" %generica_count)
    else: print ("Regra 2 eh a mais Generica: %s" %generica_count)

    ####### FAZ A DECISAO FINAL PARA VER SE AS REGRAS CONFLITAM

    #Se existe conflito no Grupo 1 (Porta de Entrada), continua verificando
    if grp_conflito['in_port'] == True:
        grupo_2 = 0
        grupo_3 = 0
        grupo_4 = 0
        sugestao_resolucao = ""
        if grp_conflito['ip_src'] == True: grupo_2 += 1
        if grp_conflito['ip_dst'] == True: grupo_2 += 1
        if grp_conflito['dl_src'] == True: grupo_3 += 1
        if grp_conflito['dl_dst'] == True: grupo_3 += 1
        if grp_conflito['tp_src'] == True: grupo_4 += 1
        if grp_conflito['tp_dst'] == True: grupo_4 += 1

        #Conflita Totalmente
        if (grupo_2 == 2) and (grupo_3 == 2) and (grupo_4 == 2):
            print "Conflitam em IP, MAC e TCP"

            #COMO CONFLITA COM TUDO, VERIFICAR A PRIORIDADE E A QUANTIDADE DE WILDCARDS
            if (pscd_rule_1.priority < pscd_rule_2.priority) and (generica_count >= 3):
                sugestao_resolucao = "Voce pode alterar a prioridade da Regra 1. Ela eh a mais generica e sobreescreve a Regra 2!"

        #Conflitos Parciais
        elif (grupo_2 == 1) and (grupo_3 == 2) and (grupo_4 == 2):
            print "Conflitam em IP/Parcialmente, MAC e TCP"

            #Analisa IP para ver qual eh wildcard
            if wildcards_rule_1['ip_src'] == True and (pscd_rule_1.priority < pscd_rule_2.priority):
                sugestao_resolucao = "Verifique o IP de Origem da Regra 1. Estah bem generico"

            elif wildcards_rule_2['ip_src'] == True and (pscd_rule_1.priority < pscd_rule_2.priority):
                sugestao_resolucao = "Verifique o IP de Origem da Regra 2. Estah bem generico"

            elif wildcards_rule_1['ip_dst'] == True and (pscd_rule_1.priority < pscd_rule_2.priority):
                sugestao_resolucao = "Verifique o IP de Destino da Regra 1. Estah bem generico"

            elif wildcards_rule_2['ip_dst'] == True and (pscd_rule_1.priority < pscd_rule_2.priority):
                sugestao_resolucao = "Verifique o IP de Destino da Regra 2. Estah bem generico"

            else:
                sugestao_resolucao = "Verifique o IP das Regras. Grande probabilidade de conflito"

        elif (grupo_2 == 2) and (grupo_3 == 1) and (grupo_4 == 2):
            print "Conflitam em IP, MAC/Parcialmente e TCP"
            sugestao_resolucao = "Verifique os campos de IP e Portas TCP/UDP das Regras. Estao bem Genericos"

        elif (grupo_2 == 2) and (grupo_3 == 2) and (grupo_4 == 1):
            print "Conflitam em IP, MAC e TCP/Parcialmente"
            sugestao_resolucao = "Verifique os campos de IP e MAC das Regras. Estao bem Genericos"

        elif (grupo_2 == 2) and (grupo_3 == 1) and (grupo_4 == 1):
            print "Conflitam em IP, MAC/Parcialmente e TCP/Parcialmente"
            sugestao_resolucao = "Verifique os campos de IP das Regras. Estao bem Genericos. Os campos de Porta TCP/UDP e MAC tambem podem vir a conflitar!"

        elif (grupo_2 == 1) and (grupo_3 == 2) and (grupo_4 == 1):
            print "Conflitam em IP/Parcialmente, MAC e TCP/Parcialmente"
            sugestao_resolucao = "Verifique os campos de MAC das Regras. Estao bem Genericos. Os campos de IP e Porta TCP/UDP tambem podem vir a conflitar!"

        elif (grupo_2 == 1) and (grupo_3 == 1) and (grupo_4 == 2):
            print "Conflitam em IP/Parcialmente, MAC/Parcialmente e TCP"
            sugestao_resolucao = "Verifique os campos de Portas TCP/UDP das Regras. Estao bem Genericos. Os campos de IP e MAC tambem podem vir a conflitar!"

        else:
            sugestao_resolucao = "Final da verificacao: Regras Nao Conflitam"

    #SE NAO TEM CONFLITO NA PORTA DE ENTRADA, FINALIZA
    else:
        sugestao_resolucao = "Regras Nao Conflitam"


    #for d,p in wildcards_total_1.iteritems():
    #    print d,p
    print ("Total de WildCards 1: %s" % wildcards_total_1)
    print ("Total de WildCards 2: %s" % wildcards_total_2)

    print ("RESULTADO FINAL:")
    print ("----------------------------")
    print ("SUGESTAO: %s" %(sugestao_resolucao))
    print ("----------------------------")
    print ("----------------------------")



class FlowMod(EventMixin):

    def __init__(self,transparent):
        self.listenTo(core.openflow)
        self.transparent = transparent
        core.openflow.addListeners(self, "all")
        log.debug("Enabling Firewall Module")
    def _handle_FlowMod(self,event):
        print "Entro aqui caralho"
        if isinstance(event, of.ofp_flow_mod):
            print "Detectou flow mod"
    def _handle_ConnectionUp(self, event):
        log.debug("Switch %s esta UP NA MINHA FUNCAO" % (dpid_to_str(event.dpid)))

        ##REGRA 01.01 - IDENTICAS
        msg1 = of.ofp_flow_mod()
        #msg1.match._in_port = 3
        msg1.table_id = 0x1
        msg1.priority = 3000
        msg1.idle_timeout = 30
        msg1.match.dl_type = 0x800
        msg1.match.nw_proto = 6
        msg1.match.nw_src = "10.0.0.1"
        msg1.match.nw_dst = "10.0.0.2"
        #msg1.match.tp_dst = 80
        #msg1.match.tp_src = 80
        msg1.actions.append(of.ofp_action_output(port = of.OFPP_ALL))

        event.connection.send(msg1)

"""
def launch(transparent=True):
    log.debug("Iniciando Rede TCC")
    #core.registerNew(FlowMod, str_to_bool(transparent))
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)