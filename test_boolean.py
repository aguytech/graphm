"""
	MATRIXBOOLEAN
"""
from graphm import MatrixBoolean

"""
"""
m1 = MatrixBoolean(matrix=['010101','101010','101011','111000'])
print(m1)
m1 = MatrixBoolean(empty=(2, 6))
print('empty', m1)
m1 = MatrixBoolean(random=(6, 4))
print('random', m1)
m2 = MatrixBoolean(random=(6, 4))
print('random', m2)
m = m1 + m2
print('m1 + m2', m)

m1 = MatrixBoolean(unity=4)
print('unity - str', m1)

me = MatrixBoolean(empty=(6,4))
me2 = MatrixBoolean(empty=(6,4))
print('me', id(me))
print('me2', id(me2))
print('m == me', m == me)
print('me == me2', me == me2)
print('me is me2', me is me2)

n = 10

m = MatrixBoolean(random=(n, n))
print('m', m)

"""
"""
# manual closure
mi = m + MatrixBoolean(unity=n) 
print('mi', mi)

mt = mi.get_copy()
dim,_ = m.get_dim()
for i in range(2, dim):
	mt = mt * mi
	print(f"m{i} ", mt)
mt = m.get_copy()
d = {1:m.get_copy()}
dim,_ = m.get_dim()
for i in range(2, dim):
	mt = mt * m
	d[i] = mt
print('d', d)
