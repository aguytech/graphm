"""
	MATRIXBOOLEAN
"""
import graphm
MatrixBoolean = graphm.matrixboolean.MatrixBoolean

m = MatrixBoolean(matrix=['010100','000000','010010','000001','001100','000000'])
i = MatrixBoolean(unity=6)
mi = m + i
mp = {
	1: m,
	2: m * m,
	3: (m * m) * (m * m),
	4: ((m * m) * (m * m)) * ((m * m) * (m * m)),
	5: ((m * m) * (m * m)) * ((m * m) * (m * m)) * ((m * m) * (m * m)) * ((m * m) * (m * m)),
	}
mt = m.copy()
mc = {1: m.copy()}
for i in range(2, 6):
	mc[i] = mc[i-1] * mc[i-1]

for k, v in mp.items():
	print(mp[k] == mc[k])

print('break')

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
"""

"""
n = 10
m = MatrixBoolean(random=(n, n))
print('m', m)

# manual closure
mi = m + MatrixBoolean(unity=n) 
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
