import graphm
from graphm import Graph

g = Graph(boolean=['00010', '01100', '10000', '10100', '00000'], nodes='a,b,c,d,e,f,g,h,i,j', node_style='int')
print(g)
pert = [('>', 'A'), ('>', 'B'), ('D', 'C'), ('A', 'D'), ('A', 'E'), ('D', 'F'), ('E', 'F'), ('G', 'F'), ('B', 'G'), ('F', 'H'), ('K', 'H'), ('B', 'I'), ('C', 'J'), ('H', 'J'), ('I', 'K'), ('>', 'L'), ('J', '<'), ('L', '<')]
g = Graph(edges=pert)
g.draw('files/pert.svg', ext='svg', graph_attr={'rankdir':'LR'})
pert = [('A', 'D'), ('A', 'E'), ('A', 'X'), ('A', 'Y'), ('>', 'Z'), ('B', 'G'), ('B', 'I'), ('C', 'J'), ('D', 'C'), ('D', 'F'), ('E', 'F'), ('F', 'H'), ('G', 'F'), ('H', 'J'), ('I', 'K'), ('I', 'F'), ('J', '<'), ('K', 'H'), ('L', '<'), ('X', 'F'), ('Y', 'F'), ('Z', 'F'), ('>', 'A'), ('>', 'B'), ('>', 'L')]
g = Graph(edges=pert)
g.draw('files/pert2.svg', ext='svg', graph_attr={'rankdir':'LR'})
pert = [('A', 'D'), ('A', 'E'), ('A', 'X'), ('A', 'Y'), ('>', 'Z'), ('B', 'G'), ('B', 'I'), ('B', 'Y'), ('C', 'J'), ('D', 'C'), ('D', 'F'), ('E', 'F'), ('F', 'H'), ('G', 'F'), ('H', 'J'), ('I', 'K'), ('I', 'F'), ('J', '<'), ('K', 'H'), ('L', '<'), ('X', 'F'), ('Y', 'F'), ('Z', 'F'), ('>', 'A'), ('>', 'B'), ('>', 'L')]
g = Graph(edges=pert)
g.draw('files/pert3.svg', ext='svg', graph_attr={'rankdir':'LR'})
pert = [('A', 'D'), ('A', 'G'), ('A', 'E'), ('A', 'X'), ('A', 'Y'), ('>', 'Z'), ('B', 'G'), ('B', 'I'), ('B', 'Y'), ('C', 'J'), ('D', 'C'), ('D', 'F'), ('E', 'F'), ('F', 'H'), ('G', 'F'), ('H', 'J'), ('I', 'K'), ('I', 'F'), ('J', '<'), ('K', 'H'), ('L', '<'), ('X', 'F'), ('Y', 'F'), ('Z', 'F'), ('>', 'A'), ('>', 'B'), ('>', 'L')]
g = Graph(edges=pert)
g.draw('files/pert4.svg', ext='svg', graph_attr={'rankdir':'LR'})
pert = [('A', 'D'), ('A', 'G'), ('A', 'E'), ('A', 'X'), ('A', 'Y'), ('>', 'Z'), ('L', 'Z2'), ('B', 'G'), ('B', 'I'), ('B', 'Y'), ('C', 'J'), ('D', 'C'), ('D', 'F'), ('E', 'F'), ('F', 'H'), ('G', 'F'), ('H', 'J'), ('I', 'K'), ('I', 'F'), ('J', '<'), ('K', 'H'), ('L', '<'), ('X', 'F'), ('Y', 'F'), ('Z', 'F'), ('Z2', 'F'), ('>', 'A'), ('>', 'B'), ('>', 'L')]
g = Graph(edges=pert)
g.draw('files/pert5.svg', ext='svg', graph_attr={'rankdir':'LR'})


""" for
pert = {'A': ('', 2), 'B': ('', 3), 'C': ('D', 5), 'D': ('A', 2), 'E': ('A', 1), 'F': ('D,E,G,X,Y,I,Z', 3), 'G': ('A,B', 2), 'H': ('F,K', 2), 'I': ('B', 1), 'J': ('C,H', 2), 'K': ('I', 3), 'L': ('', 10), 'X':('A', 3), 'Y':('A,B', 3), 'Z':('', 3), '<': ('J,L', 0)}

nodes = ['>', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'X', 'Y', 'Z', '<']

matrix	= [[None, 2, 3, None, None, None, None, None, None, None, None, None, 10, None, None, 3, None], [None, None, None, None, 2, 1, None, 2, None, None, None, None, None, 3, 3, None, None], [None, None, None, None, None, None, None, 2, None, 1, None, None, None, None, 3, None, None], [None, None, None, None, None, None, None, None, None, None, 2, None, None, None, None, None, None], [None, None, None, 5, None, None, 3, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, 3, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, 2, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, 3, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, 2, None, None, None, None, None, None], [None, None, None, None, None, None, 3, None, None, None, None, 3, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 0], [None, None, None, None, None, None, None, None, 2, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 0], [None, None, None, None, None, None, 3, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, 3, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, 3, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]]
g = Graph(matrix=matrix, nodes=nodes)
g.draw('files/pert-inter1-1.svg', ext='svg', graph_attr={'rankdir':'LR'})

matrix	= [[None, 2, 3, None, None, None, None, None, None, None, None, None, 10, None, None, 3, None], [None, None, None, None, 2, 1, None, 2, None, None, None, None, None, None, 3, 3, None], [None, None, None, None, None, None, None, 2, None, None, None, None, None, None, 3, 1, None], [None, None, None, None, None, None, None, None, None, None, 2, None, None, None, None, None, None], [None, None, None, 5, None, None, 3, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, 3, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, 2, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, 3, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, 2, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 0], [None, None, None, None, None, None, None, None, 2, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 0], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, 3, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, 3, None, None, None, None, 3, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]]
g = Graph(matrix=matrix, nodes=nodes)
g.draw('files/pert-inter1-2.svg', ext='svg', graph_attr={'rankdir':'LR'})

matrix	= [[None, 2, 3, None, None, None, None, None, None, None, None, None, 10, None, None, 3, None], [None, None, None, None, 2, 1, None, 2, None, None, None, None, None, None, 3, 3, None], [None, None, None, None, None, None, None, 2, None, None, None, None, None, None, 3, 1, None], [None, None, None, None, None, None, None, None, None, None, 2, None, None, None, None, None, None], [None, None, None, 5, None, None, 3, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, 3, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, 2, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, 3, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, 2, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 0], [None, None, None, None, None, None, None, None, 2, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 0], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, 3, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, 3, None, None, None, None, 3, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]]
nodes = ['>', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'X', 'Y', 'Z', '<']
g = Graph(matrix=matrix, nodes=nodes)
g.draw('files/pert-inter1-3.svg', ext='svg', graph_attr={'rankdir':'LR'})

matrix	= [[None, 2, 3, None, None, None, None, None, None, None, None, None, 10, None, None, 3, None], [None, None, None, None, 2, 1, None, 2, None, None, None, None, None, None, 3, 3, None], [None, None, None, None, None, None, None, 2, None, None, None, None, None, None, 3, 1, None], [None, None, None, None, None, None, None, None, None, None, 2, None, None, None, None, None, None], [None, None, None, 5, None, None, 3, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, 3, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, 2, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, 3, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, 2, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 0], [None, None, None, None, None, None, None, None, 2, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 0], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, 3, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, 3, None, None, None, None, 3, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]]
g = Graph(matrix=matrix, nodes=nodes)
g.draw('files/pert-inter1-4.svg', ext='svg', graph_attr={'rankdir':'LR'})

matrix	= [[None, 2, 3, None, None, None, None, None, None, None, None, None, 10, None, None, 3, None], [None, None, None, None, 2, 1, None, 2, None, None, None, None, None, None, 3, 3, None], [None, None, None, None, None, None, None, 2, None, None, None, None, None, None, 3, 1, None], [None, None, None, None, None, None, None, None, None, None, 2, None, None, None, None, None, None], [None, None, None, 5, None, None, 3, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, 3, None, None, None, None, None, None, None, None, None, None], [None, None, None, 2, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, 3, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 0], [None, None, None, 2, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 0], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, 3, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, 3, None, None, None, None, 3, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]]
g = Graph(matrix=matrix, nodes=nodes)
g.draw('files/pert-inter1-5.svg', ext='svg', graph_attr={'rankdir':'LR'})

matrix	= [[None, 2, 3, None, None, None, None, None, None, None, None, None, 10, None, None, 3, None], [None, None, None, None, 2, 1, None, 2, None, None, None, None, None, None, 3, 3, None], [None, None, None, None, None, None, None, 2, None, None, None, None, None, None, 3, 1, None], [None, None, None, None, None, None, None, None, None, None, 2, None, None, None, None, None, None], [None, None, None, 5, None, None, 3, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, 3, None, None, None, None, None, None, None, None, None, None], [None, None, None, 2, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, 3, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 0], [None, None, None, 2, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 0], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, 3, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, 3, None, None, None, None, 3, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]]
g = Graph(matrix=matrix, nodes=nodes)
g.draw('files/pert-inter1-6.svg', ext='svg', graph_attr={'rankdir':'LR'})

matrix	= [[None, 2, 3, None, None, None, None, None, None, None, 10, None, None, None, None, 3, None], [None, None, None, None, 2, 1, None, 2, None, None, None, None, None, None, 3, 3, None], [None, None, None, None, None, None, None, 2, None, None, None, None, None, None, 3, 1, None], [None, None, None, None, None, None, None, None, None, None, 2, None, None, None, None, None, None], [None, None, None, 5, None, None, 3, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, 3, None, None, None, None, None, None, None, None, None, None], [None, None, None, 2, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, 3, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 0], [None, None, None, 2, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, 3, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, 3, None, None, None, None, 3, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]]
g = Graph(matrix=matrix, nodes=nodes)
g.draw('files/pert-inter1-7.svg', ext='svg', graph_attr={'rankdir':'LR'})
""" 

""" for
pert = {'A': ('', 2), 'B': ('', 3), 'C': ('D', 5), 'D': ('A', 2), 'E': ('A,B', 1), 'F': ('D,E,G,X,Y,I,Z,Z2', 3), 'G': ('A,B', 2), 'H': ('F,K', 2), 'I': ('B', 1), 'J': ('C,H', 2), 'K': ('I', 3), 'L': ('', 10), 'X':('A', 3), 'Y':('A', 3), 'Z':('', 3), 'Z2':('L', 3), '<': ('J,L', 0)}
""" 

nodes = ['>', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'X', 'Y', 'Z', 'Z2', '<']

matrix	= [[None, 2, 3, None, None, None, None, None, None, None, None, None, 10, None, None, 3, None, None], [None, None, None, None, 2, 1, None, 2, None, None, None, None, None, 3, 3, None, None, None], [None, None, None, None, None, 1, None, 2, None, 1, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, 2, None, None, None, None, None, None, None], [None, None, None, 5, None, None, 3, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, 3, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, 2, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, 3, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, 2, None, None, None, None, None, None, None], [None, None, None, None, None, None, 3, None, None, None, None, 3, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 0], [None, None, None, None, None, None, None, None, 2, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 3, 0], [None, None, None, None, None, None, 3, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, 3, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, 3, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, 3, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]]
g = Graph(matrix=matrix, nodes=nodes)
g.draw('files/pert-inter2-1.svg', ext='svg', graph_attr={'rankdir':'LR'})



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

g = Graph(binary=mb.matrixM)
g = Graph(binary=mb.matrixM, node_style='int')
g = Graph(binary=mb.matrixM, nodes=nodes)
g = Graph(boolean=m.matrix)
g = Graph(boolean=m.matrix, node_style='int')
g = Graph(boolean=m.matrix, nodes=nodes)
g = Graph(nodes=['a','b','c','d','e','f','g'])
g = Graph(nodes=['A','B','C','D','E','F','G'], edges=('a-f','b-g','d-a','f-e','d-b','b-f'))
g = Graph(nodes=['A','B','C','D','E','F','G'], edges=('A-F','B-G','D-A','F-E','D-B','B-F'))
g = Graph(edges='A-D,D-A,D-C,C-A,B-C,B-B,E-F,E-G,B-I')

g.draw(f"{file}.png", label='test', node_style='int')
g.draw(f"{file}-2.png", label='test2')
g.draw(f"{file}-3.png", label='test3', fontsize="14")

print("m", m)
print(g.viz.string())

#g = Graph(mt, nodes)
#g.matrix2viz(label="G'")
#g.draw(f"{file}-final.png")
"""
