import graphm
GraphPert = graphm.graphpert.GraphPert

pert = {'A': ('', 2), 'B': ('', 3), 'C': ('D', 5), 'D': ('A', 2), 'E': ('A', 1), 'F': ('D,E,G,X,Y,I,Z', 3), 'G': ('B', 2), 'H': ('F,K', 2), 'I': ('B', 1), 'J': ('C,H', 2), 'K': ('I', 3), 'L': ('', 10), 'X':('A', 3), 'Y':('A', 3), 'Z':('', 3), '<': ('J,L', 0)}
pert = {'A': ('', 2), 'B': ('', 3), 'C': ('D', 5), 'D': ('A', 2), 'E': ('A,B', 1), 'F': ('D,E,G,X,Y,I,Z,Z2', 3), 'G': ('A,B', 2), 'H': ('F,K', 2), 'I': ('B', 1), 'J': ('C,H', 2), 'K': ('I', 3), 'L': ('', 10), 'X':('A', 3), 'Y':('A', 3), 'Z':('', 3), 'Z2':('L', 3), '<': ('J,L', 0)}
pert = {'A': ('', 2), 'B': ('', 3), 'C': ('D', 5), 'D': ('A', 2), 'E': ('A', 1), 'F': ('D,E,G,X,Y,I,Z', 3), 'G': ('A,B', 2), 'H': ('F,K', 2), 'I': ('A,B', 1), 'J': ('C,H', 2), 'K': ('I', 3), 'L': ('', 10), 'X':('A', 3), 'Y':('A,B', 3), 'Z':('', 3), '<': ('J,L', 0)}
pert = {'A': ('', 2), 'B': ('', 3), 'P': ('', 5), 'C': ('D', 5), 'D': ('A', 2), 'E': ('A,B', 1), 'F': ('D,E,G,X,Y,I,O,O2', 3), 'G': ('A,B', 2), 'H': ('F,K', 2), 'I': ('A,B', 8), 'J': ('C,H', 2), 'K': ('I', 4), 'L': ('', 10), 'X':('P', 12), 'Y':('P', 3), 'O':('', 3), 'Q':('A', 7), 'O2':('L', 3)}
pert = {'A': ('', 2), 'B': ('', 3), 'P': ('', 5), 'C': ('D', 5), 'D': ('A', 2), 'E': ('A,B', 1), 'F': ('D,E,G,X,Y,I,O,O2', 3), 'G': ('A,B', 2), 'H': ('F,K', 2), 'I': ('A,B', 8), 'J': ('C,H', 2), 'K': ('I', 4), 'L': ('', 10), 'X':('P', 12), 'Y':('P', 3), 'O':('', 3), 'Q':('A', 7), 'O2':('L', 3), '<': ('J,L', 0)}
pert = {'A': ('', 2), 'B': ('', 3), 'C': ('D', 5), 'D': ('A', 2), 'E': ('A', 1), 'F': ('D,E,G', 3), 'G': ('B', 2), 'H': ('F,K', 2), 'I': ('B', 1), 'J': ('C,H', 2), 'K': ('I', 3), 'L': ('', 10), '<': ('J,L', 0)}
pert = {'A': ('', 2), 'B': ('', 3), 'P': ('', 5), 'C': ('D', 5), 'D': ('A', 2), 'E': ('A,B', 1), 'F': ('D,E,G,X,Y,I,O,N,R', 3), 'G': ('A,B', 2), 'H': ('F,K', 2), 'I': ('A,B', 8), 'J': ('C,H', 2), 'K': ('I', 4), 'L': ('', 10), 'X':('P', 12), 'Y':('P', 3), 'O':('', 3), 'R':('A', 5), 'Q':('A', 7), 'N':('L', 3), '<': ('J,L', 0)}
#g = GraphPert(pert=pert, graph_attr={'label':'"My first Pert"', 'ranksep':'1.0 equally'})
g = GraphPert(pert=pert, graph_attr={'label':'"My first Pert"', 'ransep': 1})
print(g)

"""
g = GraphPert(ancestors={
	'A': ('', 2),
	'B': ('', 3),
	'C': ('D', 5),
	'D': ('A', 2),
	'E': ('A', 1),
	'F': ('D,E,G', 3),
	'G': ('B', 2),
	'H': ('F,K', 2),
	'I': ('B', 1),
	'J': ('C,H', 2),
	'K': ('I', 3),
	'L': ('', 10),
	'A': ('', 2),
	'<': ('J,L', 0),
	})
"""

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
