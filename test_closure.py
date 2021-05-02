"""
	MATRIXBOOLEAN
"""
import graphm
Graph = graphm.graph.Graph
MatrixBoolean = graphm.matrixboolean.MatrixBoolean

m = MatrixBoolean(matrix=['010100','000000','010010','000001','001100','000000'])
if isinstance(m, MatrixBoolean):
	print('yes')

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
g = Graph(boolean=mc[1].matrix, node_style='int')
g.draw("files/closure-1")
for i in range(2, 6):
	mc[i] = mc[i-1] * mc[i-1]
	g = Graph(boolean=mc[i].matrix, node_style='int')
	g.draw(f"files/closure-{i}")

for k, v in mp.items():
	print(mp[k] == mc[k])

print('break')
