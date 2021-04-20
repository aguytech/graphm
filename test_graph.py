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

	
matrix	= [[0, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 3, 0, 0], [0, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 0, 3, 0, 3, 0, 0], [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 3, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, -1], [0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
nodes = ['>', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'X', 'Y', 'Z', 'Z2', '<']
g = Graph(boolean=matrix, nodes=nodes)
g.draw('files/pert-inter.svg', ext='svg', graph_attr={'rankdir':'LR'})

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
