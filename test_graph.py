import graphm
#from graphm import Graph

"""
	GRAPH
"""
file = "files/grah_bin_01"
m = graphm.MatrixBoolean(random=(6,6))
mb = graphm.MatrixBinary(random=(6,6))
nodes = 'a,b,c,d,e,f'

options = {
	'strict': True,
	'directed': False,
	}

g = graphm.GraphM(nodes=['A','B','C','D','E','F','G'], edges=('AF','BG','DA','FE','DB','BF'))
g2 = graphm.GraphM(binary=mb.matrixM, dimN=mb.dimN)
g3 = graphm.GraphM(boolean=m.matrix, nodes=nodes, nodes_style='int')

g.draw(f"{file}.png", label='test', nodes_style='int')
g2.draw(f"{file}-2.png", label='test2')
g3.draw(f"{file}-3.png", label='test3', fontsize="14")

g = graphm.GraphM(boolean=['00010', '01100', '10000', '10100', '00000'], nodes='a,b,c,d,e,f,g,h,i,j', node_style='int', graph_attr = {'label' : 'graph', 'directed' : True})
g.draw(f"graph2.png", label='graph2.png')

print("m", m)
print(g.viz.string())
print(g2.viz.string())
print(g3.viz.string())


#g = GraphM(mt, nodes)
#g.matrix2viz(label="G'")
#g.draw(f"{file}-final.png")
