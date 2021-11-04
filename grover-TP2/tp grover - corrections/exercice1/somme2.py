from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit import Aer, execute
from qiskit.tools.visualization import plot_histogram
from qiskit.providers.aer import QasmSimulator
from numpy import pi

qreg_q = QuantumRegister(7, 'q')
creg_c = ClassicalRegister(7, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)

circuit.h(qreg_q[0])
circuit.h(qreg_q[4])
circuit.h(qreg_q[5])
circuit.h(qreg_q[1])
circuit.ccx(qreg_q[0], qreg_q[1], qreg_q[3])
circuit.ccx(qreg_q[4], qreg_q[5], qreg_q[6])
circuit.cx(qreg_q[0], qreg_q[1])
circuit.cx(qreg_q[4], qreg_q[5])
circuit.ccx(qreg_q[1], qreg_q[2], qreg_q[3])
circuit.cx(qreg_q[1], qreg_q[2])
circuit.ccx(qreg_q[3], qreg_q[5], qreg_q[6])
circuit.cx(qreg_q[0], qreg_q[1])
circuit.cx(qreg_q[5], qreg_q[3])
circuit.cx(qreg_q[4], qreg_q[5])
circuit.measure(qreg_q[2], creg_c[2])
circuit.measure(qreg_q[3], creg_c[3])
circuit.measure(qreg_q[6], creg_c[6])

quantum_simulator = Aer.get_backend("qasm_simulator")
job = execute(circuit,quantum_simulator, shots =1024)
result = job.result()
counts = result.get_counts()
print(str(counts))
fig = plot_histogram(counts)
fig.savefig('distribution_simulation2.png')
