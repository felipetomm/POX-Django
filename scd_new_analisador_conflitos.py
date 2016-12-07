#!/bin/python2.7

#CLASS PARA VERIFICAR OS GRUPOS DE CONFLITO
class ScdGrupoConflito(object):
    def __init__(self):
        self.in_port = False
        self.ip_src = False
        self.ip_dst = False
        self.dl_src = False
        self.dl_dst = False
        self.tp_src = False
        self.tp_dst = False
        self.dl_type = False
        self.solucao = str("")

#CLASS PARA VERIFICAR SE OS CAMPOS SAO WILDCARDS
class ScdWildcards(object):
    def __init__(self):
        self.in_port = False
        self.ip_src = False
        self.ip_dst = False
        self.dl_src = False
        self.dl_dst = False
        self.tp_src = False
        self.tp_dst = False
        self.dl_type = False

#CLASS PARA CONTAR O TOTAL DE WILDCARDS
class ScdWildcardsTotal(object):
    def __init__(self):
        self.in_port = 0
        self.ip = 0
        self.dl = 0
        self.tp = 0

class ScdRegraGenerica(object):
    def __init__(self):
        self.in_port = False
        self.ip = False
        self.dl = False
        self.tp = False
class ScdSugestao(object):
    def __init__(self):
        self.sugestao_resolucao = None
        self.nivel_conflito = 0
        #QUANTO AO NIVEL, DEFINIDO COMO
        # 0 - Nenhum
        # 1 - Medio
        # 2 - Alto

def analise_Conflito(pscd_rule_1, pscd_rule_2):
    # Inicia a verificacao das rules

    ##DECLARACAO DAS VARIAVEIS UTILIZADAS NA FUNCTION
    grp_conflito = ScdGrupoConflito()

    wildcards_rule_1 = ScdWildcards()
    wildcards_rule_2 = ScdWildcards()

    wildcards_total_1 = ScdWildcardsTotal()
    wildcards_total_2 = ScdWildcardsTotal()

    regra_generica = ScdRegraGenerica()

    sugestao = ScdSugestao()

    #print "Iniciando verificacao de Conflitos"
    #print "################################################"

    #PRIMEIRO VERIFICA SE SAO DO MESMA SWITCH
    if pscd_rule_1.switch == pscd_rule_2.switch:
        #VERIFICA SE SAO DA MESMA PORTA DE ENTRADA E DO MESMO TIPO (DL_TYPE)
        if pscd_rule_1.dl_type != pscd_rule_2.dl_type:
            #print "REGRAS NAO SAO DO MESMO DL_TYPE"
            return sugestao

        else:

            #print "REGRAS SAO DO MESMO DL_TYPE"
            grp_conflito.dl_type = True

            #print "------------------------------------"
            #print "----> VERIFICA IN_PORT - GRUPO 1"
            #print "------------------------------------"
            #SE UMA DAS IN_PORT FOR WILDCARD OU AS DUAS FOREM IGUAIS, PROSSEGUE
            if (((pscd_rule_1.in_port == None) and (pscd_rule_2.in_port == None)) or (pscd_rule_1.in_port == pscd_rule_2.in_port)):
                if (pscd_rule_1.in_port == None):
                    #print "IN_PORT 1 EH WILDCARD"
                    grp_conflito.in_port = True
                if (pscd_rule_2.in_port == None):
                    #print "IN_PORT 2 EH WILDCARD"
                    grp_conflito.in_port = True
                if (pscd_rule_1.in_port == pscd_rule_2.in_port):
                    #print "IN_PORT IGUAIS"
                    grp_conflito.in_port = True

                #print ("Conflito Grupo 1: %s" %grp_conflito.in_port)
                ####FIM GRUPO 1

                ## Verifica IP_SRC e IP_DST - GRUPO 2
                ###################################
                #print "------------------------------------"
                #print "----> GRUPO 2 - VERIFICA IP SRC/DST"
                #print "------------------------------------"
                ##IP_SRC
                if pscd_rule_1.nw_src == pscd_rule_2.nw_src:
                    #print "GRUPO 2 - IP_SRC iguais"
                    grp_conflito.ip_src = True
                    if pscd_rule_1.nw_src == None and pscd_rule_2.nw_src == None:
                        #print "GRUPO 2 - IP_SRC 1 e 2 Wildcards"
                        wildcards_rule_1.ip_src = True
                        wildcards_rule_2.ip_src = True
                else:
                    if pscd_rule_1.nw_src == None:
                        #print "GRUPO 2 - IP_SRC 1 Wildcard"
                        grp_conflito.ip_src = True
                        wildcards_rule_1.ip_src = True
                    if pscd_rule_2.nw_src == None:
                        #print "GRUPO 2 - IP_SRC 2 Wildcard"
                        grp_conflito.ip_src = True
                        wildcards_rule_2.ip_src = True
                    elif pscd_rule_1.nw_src is not None and pscd_rule_2.nw_src is not None:
                        mask = 0
                        if pscd_rule_1.nw_src[0] == pscd_rule_2.nw_src[0]:
                            if pscd_rule_1.nw_src[1] == pscd_rule_2.nw_src[1]:
                                if pscd_rule_1.nw_src[2] == pscd_rule_2.nw_src[2]:
                                    if pscd_rule_1.nw_src[3] == pscd_rule_2.nw_src[3]:
                                        mask = 1
                                    else:
                                        if pscd_rule_1.nw_src[3] == 0: mask = 1
                                        elif pscd_rule_2.nw_src[3] == 0: mask = 1
                                else:
                                    if pscd_rule_1.nw_src[2] == 0 and pscd_rule_1.nw_src[3] == 0: mask = 1
                                    elif pscd_rule_2.nw_src[2] == 0 and pscd_rule_2.nw_src[3] == 0: mask = 1
                            else:
                                if pscd_rule_1.nw_src[1] == 0 and pscd_rule_1.nw_src[2] == 0 and pscd_rule_1.nw_src[3] == 0: mask = 1
                                elif pscd_rule_2.nw_src[1] == 0 and pscd_rule_2.nw_src[2] == 0 and pscd_rule_2.nw_src[3] == 0: mask = 1
                        else:
                            if pscd_rule_1.nw_src[0] == 0 and pscd_rule_1.nw_src[1] == 0 and pscd_rule_1.nw_src[2] == 0 and pscd_rule_1.nw_src[3] == 0: mask = 1
                            elif pscd_rule_2.nw_src[0] == 0 and pscd_rule_2.nw_src[1] == 0 and pscd_rule_2.nw_src[2] == 0 and pscd_rule_2.nw_src[3] == 0: mask = 1
                        if mask > 0: grp_conflito.ip_src = True
                        #print ("Net_Mask SRC: %s" % mask)
                ##IP_DST
                if pscd_rule_1.nw_dst == pscd_rule_2.nw_dst:
                    #print "GRUPO 2 - IP_DST iguais"
                    grp_conflito.ip_dst = True
                    if pscd_rule_1.nw_dst == None and pscd_rule_2.nw_dst == None:
                        #print "GRUPO 2 - IP_DST 1 e 2 Wildcards"
                        wildcards_rule_1.ip_dst = True
                        wildcards_rule_2.ip_dst = True
                else:
                    if pscd_rule_1.nw_dst == None:
                        #print "GRUPO 2 - IP_DST 1 Wildcard"
                        grp_conflito.ip_dst = True
                        wildcards_rule_1.ip_dst = True
                    if pscd_rule_2.nw_dst == None:
                        #print "GRUPO 2 - IP_DST 2 Wildcard"
                        grp_conflito.ip_dst = True
                        wildcards_rule_2.ip_dst = True
                    elif pscd_rule_1.nw_dst is not None and pscd_rule_2.nw_dst is not None:
                        mask = 0
                        if pscd_rule_1.nw_dst[0] == pscd_rule_2.nw_dst[0]:
                            if pscd_rule_1.nw_dst[1] == pscd_rule_2.nw_dst[1]:
                                if pscd_rule_1.nw_dst[2] == pscd_rule_2.nw_dst[2]:
                                    if pscd_rule_1.nw_dst[3] == pscd_rule_2.nw_dst[3]:
                                        mask = 1
                                    else:
                                        if pscd_rule_1.nw_dst[3] == 0: mask = 1
                                        elif pscd_rule_2.nw_dst[3] == 0: mask = 1
                                else:
                                    if pscd_rule_1.nw_dst[2] == 0 and pscd_rule_1.nw_dst[3] == 0: mask = 1
                                    elif pscd_rule_2.nw_dst[2] == 0 and pscd_rule_2.nw_dst[3] == 0: mask = 1
                            else:
                                if pscd_rule_1.nw_dst[1] == 0 and pscd_rule_1.nw_dst[2] == 0 and pscd_rule_1.nw_dst[3] == 0: mask = 1
                                elif pscd_rule_2.nw_dst[1] == 0 and pscd_rule_2.nw_dst[2] == 0 and pscd_rule_2.nw_dst[3] == 0: mask = 1
                        else:
                            if pscd_rule_1.nw_dst[0] == 0 and pscd_rule_1.nw_dst[1] == 0 and pscd_rule_1.nw_dst[2] == 0 and pscd_rule_1.nw_dst[3] == 0: mask = 1
                            elif pscd_rule_2.nw_dst[0] == 0 and pscd_rule_2.nw_dst[1] == 0 and pscd_rule_2.nw_dst[2] == 0 and pscd_rule_2.nw_dst[3] == 0: mask = 1
                        if mask > 0: grp_conflito.ip_dst = True
                        #print ("Net_Mask dst: %s" % mask)

                ######FIM GRUPO 2

                #Verifica MAC_SRC e MAC_DST - GRUPO 3
                #####################################
                #print "------------------------------------"
                #print "----> GRUPO 3 - VERIFICA MAC SRC/DST"
                #print "------------------------------------"


                #ANALISA OS DOIS MAC
                if pscd_rule_1.dl_src != None and pscd_rule_2.dl_src != None and pscd_rule_1.dl_dst != None and pscd_rule_2.dl_dst != None:
                    if pscd_rule_1.dl_src == pscd_rule_2.dl_src and pscd_rule_1.dl_dst != pscd_rule_2.dl_dst:
                        grp_conflito.dl_dst = False
                        grp_conflito.dl_src = False
                    if pscd_rule_1.dl_src != pscd_rule_2.dl_src and pscd_rule_1.dl_dst == pscd_rule_2.dl_dst:
                        grp_conflito.dl_dst = False
                        grp_conflito.dl_src = False
                else:
                    # MAC SRC
                    if pscd_rule_1.dl_src == pscd_rule_2.dl_src:
                        #print "GRUPO 3 - DL_SRC iguais"
                        grp_conflito.dl_src = True
                        if pscd_rule_1.dl_src == None: wildcards_rule_1.dl_src = True
                        if pscd_rule_2.dl_src == None: wildcards_rule_2.dl_src = True
                    else:
                        if pscd_rule_1.dl_src == None:
                            #print "GRUPO 3 - DL_SRC 1 Wildcard"
                            grp_conflito.dl_src = True
                            wildcards_rule_1.dl_src = True
                        else:
                            if pscd_rule_2.dl_src == None:
                                #print "GRUPO 3 - DL_SRC 2 Wildcard"
                                grp_conflito.dl_src = True
                                wildcards_rule_2.dl_src = True
                    # MAC DST
                    if pscd_rule_1.dl_dst == pscd_rule_2.dl_dst:
                        #print "GRUPO 3 - DL_DST iguais"
                        grp_conflito.dl_dst = True
                        if pscd_rule_1.dl_dst == None: wildcards_rule_1.dl_dst = True
                        if pscd_rule_2.dl_dst == None: wildcards_rule_2.dl_dst = True
                    else:
                        if pscd_rule_1.dl_dst == None:
                            #print "GRUPO 3 - DL_DST 1 Wildcard"
                            grp_conflito.dl_dst = True
                            wildcards_rule_1.dl_dst = True
                        else:
                            if pscd_rule_2.dl_dst == None:
                                #print "GRUPO 3 - DL_DST 2 Wildcard"
                                grp_conflito.dl_dst = True
                                wildcards_rule_2.dl_dst = True

                #print ("Conflito Grupo 3: MAC_SRC: %s  MAC_DST: %s" % (grp_conflito.dl_src, grp_conflito.dl_dst))
                ####FIM GRUPO 3

                # Verifica TP_SRC e TP_DST - GRUPO 4
                #print "------------------------------------"
                #print "----> GRUPO 4 - VERIFICA PORTA TCP/UDP SRC/DST"
                #print "------------------------------------"
                #PRIMEIRO, VERIFICAMOS SE O PROTOCOLO EH IP/TCP/UDP/SCTP, VIDE COMENTARIO NO SCRIPT COLETOR

                #ANALISA SOMENTE UMA DAS REGRAS, POIS AS DUAS JA PASSARAM PELO TESTE DE IGUALDADE
                if (pscd_rule_1.dl_type =="ip" or pscd_rule_1.dl_type =="tcp" or pscd_rule_1.dl_type =="udp" or pscd_rule_1.dl_type =="sctp"):
                    # PORTA TCP/UDP SRC
                    if pscd_rule_1.tp_src == pscd_rule_2.tp_src:
                        #print "GRUPO 4 - TP_SRC iguais"
                        grp_conflito.tp_src = True
                    else:
                        if pscd_rule_1.tp_src == None:
                            #print "GRUPO 4 - TP_SRC 1 Wildcard"
                            grp_conflito.tp_src = True
                            wildcards_rule_1.tp_src = True
                        else:
                            if pscd_rule_2.tp_src == None:
                                #print "GRUPO 4 - TP_SRC 2 Wildcard"
                                grp_conflito.tp_src = True
                                wildcards_rule_2.tp_src = True

                    # PORTA TCP/UDP DST
                    if pscd_rule_1.tp_dst == pscd_rule_2.tp_dst:
                        #print "GRUPO 4 - TP_DST iguais"
                        grp_conflito.tp_dst = True
                    else:
                        if pscd_rule_1.tp_dst == None:
                            #print "GRUPO 4 - TP_DST 1 Wildcard"
                            grp_conflito.tp_dst = True
                            wildcards_rule_2.tp_dst = True
                        else:
                            if pscd_rule_2.tp_dst == None:
                                #print "GRUPO 4 - TP_DST 2 Wildcard"
                                grp_conflito.tp_dst = True
                                wildcards_rule_2.tp_dst = True

                #print ("Conflito Grupo 4: TP_SRC: %s  TP_DST: %s" % (grp_conflito.tp_dst, grp_conflito.tp_dst))

                #print ("----------------------------")
                #print ("RESULTADO DAS ANALISES:")
                #print ("----------------------------")
                #print ("Grupo Conflitos:   %s" % grp_conflito.__dict__)
                #print ("Wildcards Regra 1: %s" % wildcards_rule_1.__dict__)
                #print ("Wildcards Regra 2: %s" % wildcards_rule_2.__dict__)
                #print ("----------------------------")
                #print ("----------------------------")

                ##Conta os WildCards
                #REGRA 1
                if wildcards_rule_1.in_port == True: wildcards_total_1.in_port += 1
                if wildcards_rule_1.dl_src == True: wildcards_total_1.dl += 1
                if wildcards_rule_1.dl_dst == True: wildcards_total_1.dl += 1
                if wildcards_rule_1.ip_dst == True: wildcards_total_1.ip += 1
                if wildcards_rule_1.ip_src == True: wildcards_total_1.ip += 1
                if wildcards_rule_1.tp_dst == True: wildcards_total_1.tp += 1
                if wildcards_rule_1.tp_src == True: wildcards_total_1.tp += 1

                #REGRA 2
                if wildcards_rule_2.in_port == True: wildcards_total_2.in_port += 1
                if wildcards_rule_2.dl_src == True: wildcards_total_2.dl += 1
                if wildcards_rule_2.dl_dst == True: wildcards_total_2.dl += 1
                if wildcards_rule_2.ip_dst == True: wildcards_total_2.ip += 1
                if wildcards_rule_2.ip_src == True: wildcards_total_2.ip += 1
                if wildcards_rule_2.tp_dst == True: wildcards_total_2.tp += 1
                if wildcards_rule_2.tp_src == True: wildcards_total_2.tp += 1

                #Compara as regras para ver se a regra 1 eh a mais generica
                if wildcards_total_1.in_port > wildcards_total_2.in_port: regra_generica.in_port = True
                if wildcards_total_1.ip > wildcards_total_2.ip: regra_generica.ip = True
                if wildcards_total_1.dl > wildcards_total_2.dl: regra_generica.dl = True
                if wildcards_total_1.tp > wildcards_total_2.tp: regra_generica.tp = True

                generica_count = 0
                if regra_generica.in_port==True: generica_count += 1
                if regra_generica.ip==True: generica_count += 1
                if regra_generica.tp==True: generica_count += 1
                if regra_generica.dl==True: generica_count += 1

                #if generica_count >= 3: print ("Regra 1 eh a mais Generica: %s" %generica_count)
                #elif generica_count == 2: print ("Regras Genericas: %s" %generica_count)
                #else: print ("Regra 2 eh a mais Generica: %s" %generica_count)

                ####### FAZ A DECISAO FINAL PARA VER SE AS REGRAS CONFLITAM
                grupo_2 = 0
                grupo_3 = 0
                grupo_4 = 0
                if grp_conflito.ip_src == True: grupo_2 += 1
                if grp_conflito.ip_dst == True: grupo_2 += 1
                if grp_conflito.dl_src == True: grupo_3 += 1
                if grp_conflito.dl_dst == True: grupo_3 += 1
                if grp_conflito.tp_src == True: grupo_4 += 1
                if grp_conflito.tp_dst == True: grupo_4 += 1

                #Conflita Totalmente
                if (grupo_2 == 2) and (grupo_3 == 2) and (grupo_4 == 2):
                    #print "Conflitam em IP, MAC e TCP"

                    #COMO CONFLITA COM TUDO, VERIFICAR A PRIORIDADE E A QUANTIDADE DE WILDCARDS
                    if (pscd_rule_1.priority > pscd_rule_2.priority) and (generica_count >= 3):
                        sugestao.sugestao_resolucao = ("Voce pode alterar a prioridade da Regra. Ela eh a mais generica e sobreescreve a Regra %s!"%pscd_rule_2.flow_id)
                    elif (pscd_rule_1.priority > pscd_rule_2.priority) and (generica_count == 2):
                        sugestao.sugestao_resolucao = "Voce pode alterar a prioridade da Regra. As duas regras sao genericas!"
                    elif generica_count < 2:
                        sugestao.sugestao_resolucao = "Possuem caracteristicas de IP, MAC E TCP muito semelhantes. Confira estes campos!"
                    sugestao.nivel_conflito = 2
                #Conflitos Parciais
                elif (grupo_2 == 1) and (grupo_3 == 2) and (grupo_4 == 2):
                    #print "Conflitam em IP/Parcialmente, MAC e TCP"

                    #Analisa IP para ver qual eh wildcard
                    if wildcards_rule_1.ip_src == True and (pscd_rule_1.priority > pscd_rule_2.priority):
                        sugestao.sugestao_resolucao = "Verifique o IP de Origem da Regra. Estah bem generico"
                        sugestao.nivel_conflito = 2

                    elif wildcards_rule_2.ip_src == True and (pscd_rule_1.priority > pscd_rule_2.priority):
                        sugestao.sugestao_resolucao = ("Verifique o IP de Origem da Regra %s. Estah bem generico"%pscd_rule_2.flow_id)
                        sugestao.nivel_conflito = 2

                    elif wildcards_rule_1.ip_dst == True and (pscd_rule_1.priority > pscd_rule_2.priority):
                        sugestao.sugestao_resolucao = "Verifique o IP de Destino da Regra. Estah bem generico"
                        sugestao.nivel_conflito = 2

                    elif wildcards_rule_2.ip_dst == True and (pscd_rule_1.priority > pscd_rule_2.priority):
                        sugestao.sugestao_resolucao = ("Verifique o IP de Destino da Regra %s. Estah bem generico"%pscd_rule_2.flow_id)
                        sugestao.nivel_conflito = 2

                    else:
                        sugestao.sugestao_resolucao = "Verifique o IP das Regras. Grande probabilidade de conflito em MAC e Portas TCP"
                        sugestao.nivel_conflito = 2
                ##COMPARA QUANDO FOR UMA REGRA TCP
                elif (pscd_rule_1.dl_type =="ip" or pscd_rule_1.dl_type =="tcp" or pscd_rule_1.dl_type =="udp" or pscd_rule_1.dl_type =="sctp") and (grupo_2==2) and (grupo_4==2):
                    sugestao.sugestao_resolucao = "Regra TCP. Os Campos IP e Portas TCP/UDP estao bem genericos."
                    sugestao.nivel_conflito = 2

                elif (pscd_rule_1.dl_type =="ip" or pscd_rule_1.dl_type =="tcp" or pscd_rule_1.dl_type =="udp" or pscd_rule_1.dl_type =="sctp") and (grupo_2==1) and (grupo_4==2):
                    sugestao.sugestao_resolucao = "Regra TCP. As Portas TCP/UDP estao bem genericos. Confira tambem os Campos IP, podem vir a conflitar."
                    sugestao.nivel_conflito = 2

                elif (pscd_rule_1.dl_type =="ip" or pscd_rule_1.dl_type =="tcp" or pscd_rule_1.dl_type =="udp" or pscd_rule_1.dl_type =="sctp") and (grupo_2==2) and (grupo_4==1):
                    sugestao.sugestao_resolucao = "Regra TCP. Os Campos IP estao bem generico. Confira tambem as Portas TCP/UDP, podem vir a conflitar."
                    sugestao.nivel_conflito = 2

                elif (grupo_2 == 1) and (grupo_3 == 1) and (pscd_rule_1.dl_type =="arp" or pscd_rule_1.dl_type =="rarp" or pscd_rule_1.dl_type =="icmp"):
                    sugestao.sugestao_resolucao = ("Em regras %s, voce pode verificar os campos IP e MAC. Algum deles estah bem generico."%pscd_rule_1.dl_type)
                    sugestao.nivel_conflito = 1

                elif (grupo_2 == 2) and (grupo_3 == 2) and (pscd_rule_1.dl_type =="arp" or pscd_rule_1.dl_type =="rarp" or pscd_rule_1.dl_type =="icmp"):
                    sugestao.sugestao_resolucao = ("Em regras %s, voce pode verificar os campos IP e MAC que estao bem genericos."%pscd_rule_1.dl_type)
                    sugestao.nivel_conflito = 2

                elif (grupo_2 == 1) and (grupo_3 == 2) and (pscd_rule_1.dl_type =="arp" or pscd_rule_1.dl_type =="rarp" or pscd_rule_1.dl_type =="icmp"):
                    sugestao.sugestao_resolucao = ("Em regras %s, voce pode verificar os campos MAC que estao bem genericos."%pscd_rule_1.dl_type)
                    sugestao.nivel_conflito = 2

                #elif (grupo_2 == 2) and (grupo_3 == 0) and (pscd_rule_1.dl_type =="arp" or pscd_rule_1.dl_type =="rarp" or pscd_rule_1.dl_type =="icmp"):
                #    sugestao.sugestao_resolucao = ("Em regras %s, voce pode verificar os campos IP que estao bem genericos."%pscd_rule_1.dl_type)
                #    sugestao.nivel_conflito = 2

                elif (grupo_2 == 2) and (grupo_3 == 1) and (grupo_4 == 2):
                    #print "Conflitam em IP, MAC/Parcialmente e TCP"
                    sugestao.sugestao_resolucao = "Verifique os campos de IP e Portas TCP/UDP das Regras. Estao bem Genericos"
                    sugestao.nivel_conflito = 2

                elif (grupo_2 == 2) and (grupo_3 == 2) and (grupo_4 == 1):
                    #print "Conflitam em IP, MAC e TCP/Parcialmente"
                    sugestao.sugestao_resolucao = "Verifique os campos de IP e MAC das Regras. Estao bem Genericos"
                    sugestao.nivel_conflito = 2

                elif (grupo_2 == 2) and (grupo_3 == 1) and (grupo_4 == 1):
                    #print "Conflitam em IP, MAC/Parcialmente e TCP/Parcialmente"
                    sugestao.sugestao_resolucao = "Verifique os campos de IP das Regras. Estao bem Genericos. Os campos de Porta TCP/UDP e MAC tambem podem vir a conflitar!"
                    sugestao.nivel_conflito = 1

                elif (grupo_2 == 1) and (grupo_3 == 2) and (grupo_4 == 1):
                    #print "Conflitam em IP/Parcialmente, MAC e TCP/Parcialmente"
                    sugestao.sugestao_resolucao = "Verifique os campos de MAC das Regras. Estao bem Genericos. Os campos de IP e Porta TCP/UDP tambem podem vir a conflitar!"
                    sugestao.nivel_conflito = 1

                elif (grupo_2 == 1) and (grupo_3 == 1) and (grupo_4 == 2):
                    #print "Conflitam em IP/Parcialmente, MAC/Parcialmente e TCP"
                    sugestao.sugestao_resolucao = "Verifique os campos de Portas TCP/UDP das Regras. Estao bem Genericos. Os campos de IP e MAC tambem podem vir a conflitar!"
                    sugestao.nivel_conflito = 1

                return sugestao

            #SE NAO, ASSUME QUE NAO EH CONFLITO
            else:
                #print "IN_PORT DIFERENTES, NAO EH CONLITO"
                return sugestao
    else:
        return sugestao