#!/usr/bin/env python
# coding: utf-8

from qiskit import QuantumCircuit, execute, Aer, IBMQ, QuantumRegister, ClassicalRegister, circuit
from qiskit.compiler import transpile, assemble
from qiskit.tools.visualization import plot_histogram
from qiskit.providers.aer import QasmSimulator
from qiskit.tools.jupyter import *
from qiskit.visualization import *
#from ibm_quantum_widgets import *
from math import *
import sys
import time
import random

from tools import *
from utils import *
#from operator import *

# provider = IBMQ.load_account()
# provider = IBMQ.get_provider(hub='ibm-q-france', group='univ-montpellier', project='default')
# backends = provider.backends

simulator = Aer.get_backend('aer_simulator_matrix_product_state')
simulator.set_option('fusion_enable', False)

########################################################################
# Opérateur de grover
def inversion_about_average(qc, x, ancillas, n):
        f_in = list()
        for i in range(len(x)):
            qc.h(x[i])
            qc.x(x[i])
            for xi in x[i]:
                f_in.append(xi)
        n_cz(qc, [f_in[i] for i in range (n-1)], ancillas, f_in[ n-1])
        for i in range(len(x)-1, 0, -1):
            qc.x(x[i])
            qc.h(x[i])


def input_state(x, diff, inf, qres, q, carry, k, anc, ans):
    qc = QuantumCircuit(x[0], x[1], x[2], x[3], x[4], diff, inf, qres, carry, k, anc, q, ans, name='graph colouring')
    for i in range(len(x)):
        qc.h(x[i])
    qc.x(q)
    qc.h(q)
    return qc

########################################################################
# Oracle

def oracle(G, qc, x, diff, inf, qres, q, carry, k, anc, pivot):

    V, E = G
    nv = len(V)
    ne = len(E)

    # préparation de k
    encode(qc, pivot, k)

    ##############################################
    #  \forall u,v \in E, x_u \neq x_v
    for j in range(ne):
        u, v = E[j]
        neq(qc, x[u], x[v], anc, diff[j])

    qc.barrier()

    # \forall x_i, x_i <= k
    for i in range(nv):
        leq(qc, carry, x[i], k, inf[i], max(len(x[i]), len(k)))

    qc.barrier()

    #### and sur les diff[i]
    n_cnot(qc, diff, anc, qres[0])
    qc.barrier()
    #### and sur les inf[i]
    n_cnot(qc, inf, anc, qres[1])
    qc.barrier()

    qc.ccx(qres[0], qres[1], q)
    ##############################################
    #unroll
    qc.barrier()
    #### and sur les inf[i]
    n_cnot(qc, inf, anc, qres[1])
    qc.barrier()
    #### and sur les diff[i]
    n_cnot(qc, diff, anc, qres[0])
    qc.barrier()
    # \forall x_i, x_i <= k
    for i in range(nv-1, 0, -1):
        leq(qc, carry, x[i], k, inf[i], max(len(x[i]), len(k)))

    #  \forall u,v \in E, x_u \neq x_v
    for j in range(ne-1, 0, -1):
        u, v = E[j]
        neq(qc, x[u], x[v], anc, diff[j])

    qc.barrier()

    encodeInv(qc, pivot, k)

    ##############################################

########################################################################
# return nb color if valide else n+nb violation
def isSoluce(solution, G, k):
    # verifie que la solution est viable
    V, E = G
    nv = len(V)
    t = getMostFrequent(solution)
    colors = [0 for _ in range(nv)]
    for i in range(nv):
        colors[i] = int(t[2*i])+int(t[2*i+1])*2
        print("sommet ", str(i), "de couleur", str(colors[i]))
    tmp = 0
    cost = 0
    for e in E:
        u, v = e
        if colors[u] == colors[v]:
            print("arete violee ",u,",",v)
            cost+=1

    if cost > 0:
        tmp = nv + cost
    else:
        tmp = max(colors)

    return tmp

def minimize(G, x, diff, inf, qres, q, carry, k, anc, ans):
    V, E = G
    nv = len(V)
    ne = len(E)
    random.seed()
    mini = -1
    debut = 1
    fin = 2**len(k)
    candidat = fin
    print("############################################################################################")
    #print("Fenêtre de recherche : " + str(debut) + " - " + str(fin))
    while debut < fin :
        m = 1
        print("Recherche d'une solution de poids <= " + str(candidat))
        while m <= sqrt(pow(2,2*nv)):
            qc = input_state(x, diff, inf, qres, q, carry, k, anc, ans)
            n_iter = random.randint(1, ceil(m))
            print("    Recherche : " + str(m) + "/" + str(sqrt(pow(2, 2*nv))))
            print("        Nombre d'itérations : " + str(n_iter))
            for j in range(n_iter):
                oracle(G, qc, x, diff, inf, qres, q, carry, k, anc, candidat)
                inversion_about_average(qc, x, anc, nv)
            l = 0
            qc.measure(x[0], ans[0:2])
            qc.measure(x[1], ans[2:4])
            qc.measure(x[2], ans[4:6])
            qc.measure(x[3], ans[6:8])
            qc.measure(x[4], ans[8:10])
            # for i in range(nv):
            #
            #     qc.measure(x[i], ans[l:l+2])
            #     l+=2
            print('        Circuit composé de : ' + str(qc.num_qubits) + ' qubits, ' + str(qc.num_clbits) + ' bits.')
            print('        Portes : ', qc.count_ops())
            print('\********** Execution du circuit **********/')
            start = time.time()
            job = execute(qc, simulator, shots=2048)
            result = job.result()
            end = time.time()
            print('Circuit executé en ' + str(end-start) + " s.")
            print("\********** Lecture des états **********/")
            counts = result.get_counts(qc)
            print(counts)

            #verifie si on a bien trouvé une solution
            mini = isSoluce(counts, G, candidat)
            print("nb co = ",mini)
            if mini <= candidat:
                print("    Solution valide")
                searchedIndex = getMostFrequent(counts)
                break
            else:
                print("    Solution non valide")
                m = (4/3)*m
        if mini > candidat :
            debut = candidat
        else:
            candidat = mini - 1
        print("############################################################################################")
        print("Fenêtre de recherche : " + str(debut) + " - " + str(fin))
    return searchedIndex

def main():
	############################################################################################
	######################## Paramètres à modifier pour coder l'instance########################
    nv=5 #sommets
    V = [i for i in range(nv)]  #a0b1c2d3e4
    E = [[0, 1], [0, 2], [1, 2], [1, 3], [2, 3], [3, 4], [2, 4]] #arêtes

    ############################################################################################

    ne = len(E)
    G = (V, E)

	#qubits paramètres
    x= list()
    for i in range(nv):
        node = QuantumRegister(2, "x"+str(i))
        x.append(node)
    #qubits contraintes


    diff = QuantumRegister(ne, "edge") # diff forall u, v in e
    inf = QuantumRegister(nv, "node") # < k,  forall u, v in e
    #qubits auxiliaires
    k = QuantumRegister(2, "k") # chromatic number
    carry = QuantumRegister(1, "carry")
    qres = QuantumRegister(3, "qres")
    q = QuantumRegister(1, "fout") # diff forall u, v in e


    anc = QuantumRegister (6, "ancilla")
    q = QuantumRegister (1, "q") #anc grover
    #registre classique pour la mesure
    ans = ClassicalRegister (2*nv)
    mini = minimize(G,x, diff, inf, qres, q, carry, k, anc, ans)
    print("coloration possible : " + mini)

if __name__ == "__main__":
    main()
