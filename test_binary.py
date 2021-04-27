"""
	MATRIXBINARY
"""
from graphm import MatrixBinary

"""
m1 = MatrixBinary(matrix=([1, 1, 0, 4, 10, 8], 6))
print(m1.str())
m1 = MatrixBinary(boolean=['010101','101010','101011','111000'])
print(m1.str())
m1 = MatrixBinary(empty=(2, 6))
print('empty', m1)
m1 = MatrixBinary(random=(6, 4))
print('random', m1)
m2 = MatrixBinary(random=(6, 4))
print('random', m2)
m = m1 + m2
print('m1 + m2', m)

m1 = MatrixBinary(unity=4)
print('unity - str', m1.str())

me = MatrixBinary(empty=(6,4))
me2 = MatrixBinary(empty=(6,4))
print('me', id(me))
print('me2', id(me2))
print('m == me', m == me)
print('me == me2', me == me2)
print('me is me2', me is me2)

n = 10
"""

m = MatrixBinary(random=(n, n))
print('m', m)

m1 = MatrixBinary(matrix=([1, 1, 0, 4, 10, 8], 6))
print(m1.str())

"""
"""
# manual closure
mi = m + MatrixBinary(unity=n) 
print('mi', mi)

mt = mi.copy()
dim,_ = m.get_dim()
for i in range(2, dim):
	mt = mt * mi
	print(f"m{i} ", mt)
mt = m.copy()
d = {1:m.copy()}
dim,_ = m.get_dim()
for i in range(2, dim):
	mt = mt * m
	d[i] = mt
print('d', d)

"""
mi = m + MatrixBinary(unity=n)
mt = mi.copy()
mtmp = mi.copy()
ic = 2
for i in range(2, n):
	mt = mt * mi
	if mt != mtmp:
		l = i20
	else:
		break
	mtmp = mt.copy()
#print('mt', mt)
"""

print('--------')
mc = m.get_closure()
print('--------')
print('mc', mc)
#print(mt == mc)
#print('count mt', l)

"""
"""
mc = m.get_connect()
print('mt == mc', mt == mc['matrix'])
print('c', mc['connect'])
print('d', mc['deep'])
print('get_connect', mc['matrix'])

mc = m.get_connect_nodes(2, n-1)
print('get_connect_node', mc['matrix'])
print('c', mc['connect'])
print('d', mc['deep'])

