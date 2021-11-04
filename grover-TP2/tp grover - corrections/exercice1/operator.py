
##################################################################################
# Somme : (a, b) -> (a, a + b)

def add(qc, c, a , b, n_bit):
    maj(qc, c, a, b, n_bit)
    qc.cx(a[n_bit-1], b[n_bit])
    uma(qc, c, a , b, n_bit)

def un_add(qc, c, a, b, n_bit):
    un_uma(qc, c, a , b, n_bit)
    qc.cx(a[n_bit-1], b[n_bit])
    un_maj(qc, c, a, b, n_bit)

##################################################################################
# Différence : (a, b) -> (a, b - a)

def subs(qc, c, a, b, control, n_bit):
    un_uma(qc, c, a , b, n_bit)
    qc.cx(a[n_bit-1], b[n_bit])
    un_maj(qc, c, a, b, n_bit)
    
def un_subs(qc, c, a , b, control, n_bit):
    maj(qc, c, a, b, n_bit)
    qc.cx(a[n_bit-1], b[n_bit])
    uma(qc, c, a , b, n_bit)

##################################################################################
# Comparateur : (a, b, res) -> (a, b, (a <= b)) 
    
def leq(qc, c, a, b, res, n_bit):
    un_uma(qc, c, a , b, n_bit)
    qc.cx(a[n_bit-1], res)
    qc.x(res)
    uma(qc, c, a , b, n_bit)

##################################################################################
# Equal : (a, b, res) -> (a, b, (a == b))
def eq(qc, a, b, anc, res):
    for i in range(len(a)):
        qc.cx(a[i], b[i])
        qc.x(b[i])
    n_cnot(qc, b, anc, res)
    for i in range(len(a)):
        qc.x(b[i])
        qc.cx(a[i], b[i])

def un_eq(qc, a, b, anc, res):
    for i in range(len(a)):
        qc.cx(a[i], b[i])
        qc.x(b[i])
    n_cnot(qc, b, anc, res)
    for i in range(len(a)):
        qc.x(b[i])
        qc.cx(a[i], b[i])

###############################################################################
# Not equal : (a, b, res) -> (a, b, (a != b))
def neq(qc, a, b, anc, res):
    eq(qc, a, b, anc, res)
    qc.x(res)

######
# sub function for sum
def maj(qc, c, a , b, n_bit):
    qc.cx(a[0], b[0])
    qc.cx(a[0], c[0])
    qc.ccx(c[0], b[0], a[0])
    qc.barrier()
    for i in range(1, n_bit, 1):
        qc.cx(a[i], b[i])
        qc.cx(a[i], a[i-1])
        qc.ccx(a[i-1], b[i], a[i])
        qc.barrier()
    
def uma(qc, c, a, b, n_bit):
    for i in range(n_bit-1, 0, -1):
        qc.ccx(a[i-1], b[i], a[i])
        qc.cx(a[i], a[i-1])
        qc.cx(a[i-1], b[i])
    qc.ccx(c[0], b[0], a[0])
    qc.cx(a[0], c[0])
    qc.cx(c[0], b[0])    
    
def un_maj(qc, c, a , b, n_bit):    
    for i in range(n_bit-1, 0, -1):
        qc.ccx(a[i-1], b[i], a[i])
        qc.cx(a[i], a[i-1])
        qc.cx(a[i], b[i])  
    qc.ccx(c[0], b[0], a[0])
    qc.cx(a[0], c[0])
    qc.cx(a[0], b[0])

def un_uma(qc, c, a, b, n_bit):
    qc.cx(c[0], b[0])
    qc.cx(a[0], c[0])
    qc.ccx(c[0], b[0], a[0])
    for i in range(1, n_bit):
        qc.cx(a[i-1], b[i])
        qc.cx(a[i], a[i-1])
        qc.ccx(a[i-1], b[i], a[i])