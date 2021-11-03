from tools import *
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

##################################################################################
# Swap : (a, b) -> (b, a)

def swap(qc, control, a, b):
    qc.ccx(control, a, b)
    qc.ccx(control, b, a)
    qc.ccx(control, a, b)

def integerSwap(qc, control, a, b):
    for i in range(len(a)):
        swap(qc, control, a[i], b[i])

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
# Différence controlée : (a, b) -> (a, b - a) si (a < b) et (a - b) sinon

def csubs(qc, c, a, b, control, anc, n_bit):
    leq(qc, c, b, a, control, n_bit)
    integerSwap(qc, control, a, b)
    un_uma(qc, c, a, b, n_bit)
    qc.cx(a[n_bit-1], b[n_bit])
    un_maj(qc, c, a, b, n_bit)

def un_csubs(qc, c, a , b, control, anc, n_bit):
    maj(qc, c, a, b, n_bit)
    qc.cx(a[n_bit-1], b[n_bit])
    uma(qc, c, a, b, n_bit)
    integerSwap(qc, control, a, b)
    leq(qc, c, b, a, control, n_bit)

##################################################################################
# Comparateur : (a, b, res) -> (a, b, (a <= b))

def leq(qc, c, a, b, res, n_bit):
    un_uma(qc, c, a , b, n_bit)
    qc.cx(a[n_bit-1], res)
    qc.x(res)
    uma(qc, c, a , b, n_bit)

##################################################################################
# Equal : (a, b, res) -> (a, b, (a == b))
def equal(qc, a, b, anc, res):
#a completer

def un_equal(qc, a, b, anc, res):
    equal(qc, a, b, anc, res)

# Not equal : (a, b, res) -> (a, b, (a != b))
def neq(qc, a, b, anc, res):
# a completer