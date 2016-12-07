#!/usr/bin/python2.7
import time
from threading import Thread
import threading, Queue


class cabeca(object):
    def __init__(self):
        self.nome = None


def check_infos(user_id, queue):
    result = user_id+5*2+4*20
    queue.put(result)

def soma(i):
    return i+5*2+4*20

queued_request = Queue.Queue()

lista_teste = []
lista_teste_2 = []
for i in range(6000):
    lista_teste.append(i+3)
    lista_teste_2.append(i+10)

tempo = time.clock()
for i in range(6000):
    check_infos_thread = threading.Thread(target=check_infos, args=(lista_teste[i], queued_request))
    check_infos_thread.start()
    final_result = queued_request.get()
    lista_teste[i] = final_result

print "Tempo Thread %s"%(time.clock()-tempo)


tempo = time.clock()
for i in range(6000):
    teste = soma(lista_teste_2[i])
    lista_teste_2[i] = teste


print "Tempo Normal %s"%(time.clock()-tempo)
#print lista_teste

cabeca = cabeca()
cabeca.nome = "Felipe"
for i in range(2):
    lista_teste[i] = cabeca

print lista_teste[0].nome

