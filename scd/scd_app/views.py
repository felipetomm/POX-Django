from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.db.models import Count
from array import *
from .models import *
from django.db.models import F
from datetime import timedelta
from django.utils import timezone
from django.core import serializers
from scd_coletor import scd_flows



def index(request):
    return render_to_response('index.html', context_instance=RequestContext(request))

def sobre(request):
    return render_to_response('index.html', context_instance=RequestContext(request))

def switches(request):
    switches = ScdComutador.objects.all().order_by('comut_id')

    #PERFUMARIA - LISTAR O TOTAL DE REGRAS E O TOTAL DE REGRAS COM CONFLITO
    """lista_regras=[]
    for switch in switches:
        flows_count = ScdFlow.objects.all().Count('fl_id').filter(id_comutador=switch.comut_id)
        flows = ScdFlow.objects.all().order_by('fl_id').filter(id_comutador=switch.comut_id)
        for flow in flows:
            regras = scd_flows()
            conflitos = ScdConflito.objects.all().order_by('con_flow_principal').filter(con_flow_principal=flow.fl_id)
            for conflito in conflitos:
                regras.conflito.append(conflito.con_flow_analisada.fl_id)"""



    return render_to_response('switches.html', RequestContext(request,{'switches':switches}))

def regras(request):
    switches = ScdComutador.objects.all().order_by('comut_nome')

    if (request.GET.get('opt_politica')): slc_politica = int(request.GET.get('opt_politica'))
    else: slc_politica = 0
    if (request.GET.get('opt_switch')): slc_switch = int(request.GET.get('opt_switch'))
    else: slc_switch = 0
    lista_regras=[]

    #FILTRA PELO SWITCH
    if ((slc_switch != 0) and (slc_switch != None)):
        flows = ScdFlow.objects.all().order_by('fl_id').filter(id_comutador=slc_switch)
    else:
        flows = ScdFlow.objects.all().order_by('fl_id')
    for flow in flows:
        regras = scd_flows()
        regras.flow_id = flow.fl_id
        regras.table = flow.fl_flowtable
        regras.switch = flow.id_comutador.comut_nome
        regras.priority = flow.fl_priority
        regras.idle_timeout = flow.fl_idle_timeout
        regras.hard_timeout = flow.fl_hard_timeout
        regras.in_port = flow.fl_in_port
        regras.actions = flow.fl_actions

        regras.dl_dst = flow.fl_dl_dst
        regras.dl_src = flow.fl_dl_src
        regras.dl_type = flow.fl_dl_type
        regras.dl_vlan = flow.fl_dl_vlan

        regras.nw_src = flow.fl_nw_src
        regras.nw_dst = flow.fl_nw_dst
        regras.nw_tos = flow.fl_nw_tos
        regras.nw_proto = flow.fl_nw_proto

        regras.tp_dst = flow.fl_tp_dst
        regras.tp_src = flow.fl_tp_src
        conflitos = ScdConflito.objects.all().order_by('con_flow_principal').filter(con_flow_principal=flow.fl_id)
        for conflito in conflitos:
            regras.conflito.append(conflito.con_flow_analisada.fl_id)
            regras.conflito_sugestao.append(conflito.con_sugestao)
            regras.conflito_nivel.append(conflito.con_nivel)
        if ((slc_politica == 0) or (slc_politica == None)): lista_regras.append(regras)
        elif ((slc_politica == 1) and (regras.conflito.__len__() > 0)): lista_regras.append(regras)
        elif ((slc_politica == 2) and (regras.conflito.__len__() < 1)): lista_regras.append(regras)
        regras = None

    return render_to_response('regras.html', RequestContext(request,{'regras':lista_regras, 'switches':switches}))
