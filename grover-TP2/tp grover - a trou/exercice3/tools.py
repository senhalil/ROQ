def n_cnot(circuit, controls, ancillas, target):
    n = len(controls)
    if n == 1:
        circuit.cx(controls[0], target)
    elif n == 2:
        circuit.ccx(controls[0], controls[1], target)
    else:
        circuit.ccx(controls[0], controls[1], ancillas[0])
        for i in range(2,n):
            circuit.ccx(controls[i], ancillas[i-2], ancillas[i-1])
        circuit.cx(ancillas[n-2], target)
        for i in range(n-1,1,-1):
            circuit.ccx(controls[i], ancillas[i-2], ancillas[i-1])
        circuit.ccx(controls[0], controls[1], ancillas[0])
        
def n_cz(qc, controls, ancillas, target ) :
    qc.h(target)
    n_cnot(qc, controls, ancillas, target )
    qc.h(target)

def getMostFrequent(dic):
    tmp = 0
    k = ''
    for key in dic: 
        if tmp < dic.get(key):
            tmp = dic.get(key)
            k = key       
    print("Etat le plus probable : " + k[::-1])
    return k[::-1]

#int -> bitfield 
def bitfield(n):
    return [1 if digit=='1' else 0 for digit in bin(n)[2:]]

#ajouter des 0 pour que la liste soit de taille n  
def complement(b, n):
    m = len(b)
    for i in range(abs(n-m)):
        b.append(0)

# encode v sur q
def encode(qc, v, q):
    v_b =  bitfield(v)
    v_b.reverse()
    n = len(q)
    complement(v_b, n)
    for b in range(n):
        if v_b[b] == 1:
            qc.x(q[b])

def encodeInv(qc, v, q):
    v_b =  bitfield(v)
    v_b.reverse()
    n = len(q)
    complement(v_b, n)
    for b in range(n):
        if v_b[b] == 0:
            qc.x(q[b])

# encode value sur y intriqué avec x 
def entangle(qc, value, x, y, anc):
    v_b =  bitfield(value)
    n = len(x)
    v_b.reverse()
    complement(v_b, n)
    for i in range(n):
        if v_b[i] == 1:
            n_cnot(qc, x, anc, y[i])
