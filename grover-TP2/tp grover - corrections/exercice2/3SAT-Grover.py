# 3-SAT avec Grover en Qiskit d'IBM
# inspired from Nannincini paper "An introduction of Quantum Computing, without Physics" 2017

from qiskit import *

from qiskit import IBMQ

import sys
from qiskit import QuantumRegister, ClassicalRegister , QuantumCircuit
from qiskit import Aer
from qiskit.tools import visualization

def black_box_uf (circuit , f_in , f_out , aux , n , sat_formula) :
  num_clauses = len ( sat_formula)

  # spécification des contraintes
  for (k , clause ) in enumerate( sat_formula ) :
      for literal in clause :
        if literal > 0 :
           circuit.x( f_in [literal - 1])
      circuit.ccx ( f_in [ 0 ] , f_in [ 1 ] , aux [ num_clauses ] )
      circuit.ccx ( f_in [ 2 ] , aux [ num_clauses ] , aux [ k ] )
      circuit.ccx ( f_in [ 0 ] , f_in [ 1 ] , aux [ num_clauses] )
      for literal in clause :
         if literal > 0 :
           circuit.x( f_in [literal -1])
  for i in range(num_clauses):
      circuit.x(aux[i])

  if ( num_clauses == 1 ) :
        circuit.cx ( aux [ 0 ] , f_out [0] )
  elif ( num_clauses == 2 ) :
         circuit.ccx ( aux [ 0 ] , aux [ 1 ] , f_out [ 0 ] )
  elif ( num_clauses == 3 ) :
         circuit.ccx ( aux [ 0 ] , aux [ 1 ] , aux [ num_clauses ] )
         circuit.ccx ( aux [ 2 ] , aux [ num_clauses ] , f_out [ 0 ] )
         circuit.ccx ( aux [ 0 ] , aux [ 1 ] , aux [ num_clauses ] )

  # Unroll
  for i in range(num_clauses):
         circuit.x(aux[i])

  for (k , clause ) in enumerate( sat_formula ) :
      for literal in clause :
         if literal > 0 :
           circuit.x( f_in [literal -1])
      circuit.ccx ( f_in [ 0 ] , f_in [ 1 ] , aux [ num_clauses] )
      circuit.ccx ( f_in [ 2 ] , aux [ num_clauses ] , aux [ k ] )
      circuit.ccx ( f_in [ 0 ] , f_in [ 1 ] , aux [ num_clauses ] )
      for literal in clause :
          if literal > 0 :
            circuit.x( f_in [literal - 1])

def inversion_about_average (circuit , f_in , n ) :
       for j in range (n ) :
            circuit.h( f_in [ j ] )
       for j in range (n ) :
            circuit.x ( f_in [ j ] )
       n_controlled_Z( circuit , [ f_in [ j ] for j in range (n -1)] , f_in[ n-1])
       for j in range (n ) :
            circuit.x( f_in [ j ] )
       for j in range (n ) :
            circuit.h( f_in [ j ] )

def n_controlled_Z ( circuit , controls , target ) :
       if ( len ( controls ) > 2 ) :
           raise ValueError ('erreur')
       elif ( len ( controls ) == 1 ) :
           circuit.h( target )
           circuit.cx ( controls [ 0 ] , target )
           circuit.h( target )
       elif (len ( controls ) == 2 ) :
          circuit.h( target )
          circuit.ccx ( controls [ 0 ] , controls [ 1 ] , target )
          circuit.h( target )

def input_state( circuit , f_in , f_out , n ) :
    for j in range (n ) :
       circuit.h( f_in [ j ] )
    circuit.x ( f_out )
    circuit.h ( f_out )


# ----------------------------------
# definition de l'instance
# f = (x0 ⋁ x1 ⋁ ¬ x2) ⋀(¬ x0 ⋁ ¬ x1 ⋁ ¬ x2) ⋀(¬ x0 ⋁ x1 ⋁ x2)

n=3
sat_formula=[[1,2,-3], [-1 ,-2,-3], [-1,2,3]]

f_in = QuantumRegister (n)
f_out = QuantumRegister (1)
aux = QuantumRegister ( len (sat_formula) + 1)

ans = ClassicalRegister (n)
qc = QuantumCircuit ( f_in , f_out , aux , ans)

input_state ( qc , f_in , f_out , n)
## 1 iteration
black_box_uf(qc, f_in, f_out , aux , n, sat_formula)
inversion_about_average ( qc , f_in , n)

# 2 iterations
#black_box_uf(qc, f_in, f_out , aux , n, sat_formula)
#inversion_about_average ( qc , f_in , n)

# 3 iterations
#black_box_uf(qc, f_in, f_out , aux , n, sat_formula)
#inversion_about_average ( qc , f_in , n)

# 4 iterations
#black_box_uf(qc, f_in, f_out , aux , n, sat_formula)
#inversion_about_average ( qc , f_in , n)

# Measure the output r e g i s t e r in the computational b a s i s
for j in range (n ) :
  qc.measure ( f_in [ j ] , ans[j] )

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import Aer, execute
from qiskit.tools.visualization import plot_histogram
from qiskit.providers.aer import QasmSimulator

# Create an instance of the local quantum simulator
quantum_simulator = Aer.get_backend("qasm_simulator")
    
qc.draw(output='mpl',filename='circuit.png')
# Execute and store the results.
job = execute(qc,quantum_simulator, shots =1024)
result = job.result()
# Get counts and p l o t histogram
counts = result.get_counts()
print(str(counts))
fig = plot_histogram(counts)
fig.savefig('distribution_simulation.png')
# print(qc)


