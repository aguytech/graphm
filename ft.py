"""
	MATRIXBOOLEAN
"""
from graphm import MatrixBoolean
from graphm import GraphM

"""
"""
#m1 = MatrixBoolean([[1,1,0,0],[0,1,1,0],[0,1,1,1],[1,0,0,1]])
m = MatrixBoolean(matrix=['00000','10000','01010','10001','00100'])
print('m', m)

i = MatrixBoolean(unity=(5))
mi = m + i
print('mi', mi)
mi2 = mi * mi
print('mi2', mi2)
mi4 = mi2 * mi2
print('mi4', mi4)

"""
"""
mt = MatrixBoolean(matrix=['00000','10000','01010','10001','00100'])
r = MatrixBoolean(matrix=['00000','10000','01010','10001','00100'])
nodes = 'A,B,C,D,E'
g = GraphM(boolean=mt.matrix, nodes=nodes)
g.draw(f"files/graphm.png")

dim,_ = mt.get_dim()
for i in range(dim):
	mt = mt * m
	r = r + mt
	print(f'm{i}', mt)
	g.draw(f"files/graphm{i}.png")

g = GraphM(boolean=r.matrix, nodes=nodes)
g.draw(f"files/graphr.png")

"""
"""
file = "files/exo41"
m = MatrixBoolean(matrix=['1011','1011','0111','0011'])
i = MatrixBoolean(unity=(4))
print('m', m)
mt = MatrixBoolean(matrix=['1011','1011','0111','0011'])
r = MatrixBoolean(matrix=['1011','1011','0111','0011'])
nodes = 'A,B,C,D'
g = GraphM(boolean=mt.matrix, nodes=nodes)
g.draw(f"{file}.png")

"""
"""
file = "files/exo42"
m = MatrixBoolean(matrix=['01110000','00001000','10000110','01000000','00000001','00000010','00011000','00000010'])
dim, _ = m.get_dim()
i = MatrixBoolean(unity=(dim))
print('m', m)
nodes = 'A,B,C,D,E,F,G,H'
g = GraphM(boolean=m.matrix, nodes=nodes)
g.draw(f"{file}.png")

mi = m + i
print('mi', mi)
mit = mi * mi * mi * mi * mi * mi
print('mit', mit)

g = GraphM(boolean=mit.matrix, nodes=nodes)
g.draw(f"{file}-final.png")

file = "files/exo43"
m = MatrixBoolean(matrix=['01010','00100','00001','00101','00000'])
mt = MatrixBoolean(matrix=['01010','00100','00001','00101','00000'])
s = MatrixBoolean(matrix=['01010','00100','00001','00101','00000'])
dim, _ = m.get_dim()
i = MatrixBoolean(unity=(dim))
print('m', m)
nodes = 'A,B,C,D,E'
g = GraphM(boolean=m.matrix, nodes=nodes)
g.draw(f"{file}.png")

dim,_ = m.get_dim()
for i in range(2, dim):
	mt = mt * m
	s = s + mt
	print(f"m{i} ", mt)

print ('s', s)
g = GraphM(boolean=mt.matrix, nodes=nodes)
g.draw(f"{file}-final.png")

"""
"""
r = MatrixBoolean(matrix=['01010','00100','00001','00101','00000'])
dim,_ = mt.get_dim()
for i in range(dim):
	mt = mt * m
	r = r + mt
	print(f'm{i}', mt)
	g.draw(f"{file}{i}.png")

g = GraphM(boolean=r.matrix, nodes=nodes)
g.draw(f"{file}.png")

