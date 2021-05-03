"""
	MATRIXBOOLEAN
"""
import graphm
Graph = graphm.graph.Graph
MatrixBoolean = graphm.matrixboolean.MatrixBoolean

"""
closure
"""

m = MatrixBoolean(matrix=['010100','000000','010010','000001','001100','000000'])

i = MatrixBoolean(unity=6)
mi = m + i
mp = {
	1: m,
	2: m * m,
	3: m * m * m,
	4: m * m * m * m,
	5: m * m * m * m * m,
	}

i = MatrixBoolean(unity=6)
mi = m + i
mp = {
	1: m,
	2: m * m,
	3: (m * m) * m,
	4: ((m * m) * m) * m,
	5: (((m * m) * m) * m) * m,
	}

i = MatrixBoolean(unity=6)
mi = m + i
mpc = {
	1: m,
	2: m * m,
	3: (m * m) * (m * m),
	4: ((m * m) * (m * m)) * ((m * m) * (m * m)),
	5: ((m * m) * (m * m)) * ((m * m) * (m * m)) * ((m * m) * (m * m)) * ((m * m) * (m * m)),
	}

mt = m.copy()
mc = {1: m.copy()}
g = Graph(boolean=mc[1], node_style='int', graph_attr={'label': f'rang 1'})
g.draw("files/closure-1.svg", ext='svg')
for i in range(2, 6):
	mc[i] = mc[i-1] * mc[i-1]
	g = Graph(boolean=mc[i], node_style='int', graph_attr={'label': f'rang {i}'})
	g.draw(f"files/closure-{i}.svg", ext='svg')

for k, v in mp.items():
	print()
	#print(mp[k])
	print(mc[k])
	print(mp[k] == mc[k])

print('break')
