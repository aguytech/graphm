import graphm
from graphm import GraphPert

g = GraphPert(nodes=['A','B','C','D','E'])
print(g)
g = GraphPert(edges='A-D,D-A,D-C,C-A,B-C,B-B')
print(g)

g = GraphPert(boolean=['00010', '01100', '10000', '10100', '00000'])
g.set_nodes(nodes='UU,V,X,Y,Z,T')
g.viz.nodes()
print(g)

g = GraphPert(boolean=[[0,0,0,1], [0,0,1,0], [0,0,0,1], [1,0,1,1]])
print(g)
		
		
"""
	GRAPH
file = "files/grah_bin_01"
m = graphm.MatrixBoolean(random=(6,6))
mb = graphm.MatrixBinary(random=(6,6))
nodes = 'a,b,c'
nodes = 'a,b,c,d,e,f,g,h,i,j,k,l'

options = {
	'strict': True,
	'directed': False,
	}

g = GraphPert(binary=mb.matrixM)
g = GraphPert(binary=mb.matrixM, node_style='int')
g = GraphPert(binary=mb.matrixM, nodes=nodes)
g = GraphPert(boolean=m.matrix)
g = GraphPert(boolean=m.matrix, node_style='int')
g = GraphPert(boolean=m.matrix, nodes=nodes)
g = GraphPert(nodes=['a','b','c','d','e','f','g'])
g = GraphPert(nodes=['A','B','C','D','E','F','G'], edges=('a-f','b-g','d-a','f-e','d-b','b-f'))
g = GraphPert(nodes=['A','B','C','D','E','F','G'], edges=('A-F','B-G','D-A','F-E','D-B','B-F'))
g = GraphPert(edges='A-D,D-A,D-C,C-A,B-C,B-B,E-F,E-G,B-I')

g.draw(f"{file}.png", label='test', node_style='int')
g.draw(f"{file}-2.png", label='test2')
g.draw(f"{file}-3.png", label='test3', fontsize="14")

print("m", m)
print(g.viz.string())

#g = GraphPert(mt, nodes)
#g.matrix2viz(label="G'")
#g.draw(f"{file}-final.png")
"""
