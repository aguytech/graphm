

"""
from graphm import MatrixBinary
from graphm import MatrixBinarySlides
from graphm import GraphM

m = MatrixBinary(boolean=['01001', '00100', '01010', '00001', '01010'])
mc = (m.get_closure_slides())
mbs = MatrixBinarySlides(mc)
c = mbs.get_paths_from(4)
print('m', m)
print()
print('c', c)
print()
print('repr mbs', repr(mbs))
print()
print('mbs', mbs)


m = MatrixBinary(boolean=['00001', '00100', '00010', '00000', '01001'])
mbs = MatrixBinarySlides(m.get_closure_slides())
closure = mbs.get_closure()
print('closure', closure)
print(mbs.get_slide_MS2NS(closure))

edges = 'XA,XB,DC,AD,AE,DF,EF,GF,BG,FH,KH,BI,CJ,HJ,IK,XL,JY,LY'
g = GraphM()
print(g)
print(repr(g))
print(g.str())
g = GraphM(
	edges=edges,
	graph_attr={'rankdir':'LR', 'label':'mytest'},
	node_attr={'shape':'ellipse'}
	)
edges = {'X': 'L', 'D': 'F', 'A': 'E', 'E': 'F', 'G': 'F', 'B': 'I', 'F': 'H', 'K': 'H', 'C': 'J', 'H': 'J', 'I': 'K', 'J': 'Y', 'L': 'Y'}
g = GraphM(
	edges=edges,
	graph_attr={'rankdir':'LR', 'label':'mytest'},
	node_attr={'shape':'ellipse'}
	)
edges = [('X', 'L'), ('D', 'F'), ('A', 'E'), ('E', 'F'), ('G', 'F'), ('B', 'I'), ('F', 'H'), ('K', 'H'), ('C', 'J'), ('H', 'J'), ('I', 'K'), ('J', 'Y'), ('L', 'Y')]
g = GraphM(
	edges=edges,
	graph_attr={'rankdir':'LR', 'label':'mytest'},
	node_attr={'shape':'ellipse'}
	)
print(g.str())
print(g.viz.string())
g.draw(path='files/mdm.png')
g.draw(f"files/mdm2.png", graph_attr={'nodes_style':'int'})

g = GraphM(boolean=['00010', '01100', '10000', '10100', '00000'], nodes='a,b,c,d,e,f,g,h,i', node_style='int')
g = GraphM(boolean=['0001', '0010', '0001', '1011'], nodes=['v','w','x','y','z'])
g = GraphM(boolean=['00010', '01100', '10000', '10100', '00000'], nodes='aa,bbb,c,d,e,f,g,h,i,j', node_style='int')
print(g)
g.set_viz_edges('a,b,c,d,e,f,g,h,j')
g.set_viz_nodes(nodes='UU,V,X,Y,Z,T')
g = GraphM(boolean=['00010', '01100', '10000', '10100', '00000'], nodes=['α','β','γ','δ','ε','ζ'])
g.draw(f"files/test.png")

g = GraphM(nodes=['A','B','C','D','E'], edges=('AD','DA','DC','CA','BC','BB'))
g.draw(f"files/test2.png")
"""

"""
g.draw(f"docs/src/files/graph1.png", label='', nodes_style='int')
g.draw(f"docs/build/html/files/graph1.png", label='', nodes_style='int')
"""