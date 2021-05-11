import graphm
Graph = graphm.Graph
MatrixBinary = graphm.MatrixBinary
MatrixBoolean = graphm.MatrixBoolean
MatrixBinaryClosure = graphm.MatrixBinaryClosure

m = MatrixBinary(boolean=['010010', '001000', '010100', '010010', '000000', '000000'])
mbc = MatrixBinaryClosure(m.closure_slides())
connected = mbc.is_connected()
connected = mbc.is_connected_fully()
cycle = mbc.nodes_connected()
tree = mbc.is_matrix_tree()

m =  MatrixBinary(boolean=['010010', '001000', '010101', '010010', '000000', '000000'])
mbc = MatrixBinaryClosure(m.closure_slides())
connected = mbc.is_connected()

m =  MatrixBinary(boolean=['010011', '001000', '010100', '010010', '000100', '100000'])
mbc = MatrixBinaryClosure(m.closure_reflexive())
mbc.is_connected_fully()
		
m = MatrixBinary(boolean=['01001', '00100', '01010', '00001', '01010'])
g = Graph(binary=m, node_style='int')
g.draw("files/test_binaryclosure-1.svg", ext='svg')

m = MatrixBinary(boolean=['010010', '001000', '010100', '010010', '000000', '000000'])
g = Graph(binary=m, node_style='int', graph_attr={'label': 'graphe'})
g.draw("files/test_binaryclosure-m.svg", ext='svg')

m = MatrixBinary(boolean=['1000001001', '1111111101', '0000010000', '0011110000', '0011110000', '0000000000', '1000001001', '1111111101', '1011111001', '1000001001'])
g = Graph(binary=m, node_style='int', graph_attr={'label': 'connecté'})
g.draw("files/test_binaryclosure-connected.svg", ext='svg')

mc = m.closure_reflexive()
mbc = MatrixBinaryClosure(mc)
mc = m.closure_slides()
mbc = MatrixBinaryClosure(mc)

g = Graph(binary=mbc.closure, node_style='int', graph_attr={'label': 'fermeture transitive'})
g.draw("files/test_binaryclosure-mbc.svg", ext='svg')

formated = MatrixBinary.get_matrix_formated(mbc.closure)

nodes_start = mbc.nodes_start()
print('nodes_start', nodes_start)
connectivity = mbc.connectivity()
print('connectivity', connectivity)
paths = mbc.matrix.paths_from(1)
print('paths', paths)
nodes_start = mbc.nodes_start()
nodes_end = mbc.nodes_end()
lonely = mbc.nodes_lonely()
print('lonely', lonely)

print('---------------------------------------------------------------')
report = mbc.report()
print(mbc.str_report())
print('---------------------------------------------------------------')
connectivity = mbc.connectivity()
print(connectivity)
print('---------------------------------------------------------------')

"""
	test all get_closure
"""
n = 20
m = MatrixBinary(random=(n, n), level=100)
print('m', m)
print('m matrixM', m.matrixM)

mcr = m.closure_reflexive()
mbc = MatrixBinaryClosure(mcr)
print('mbc', '\n', mbc)

mcr = m.closure_reflexive_optimized()
mbc = MatrixBinaryClosure(mcr)
print('mbc', '\n', mbc)

mcr = m.closure_matrix()
mbc = MatrixBinaryClosure(mcr)
print('mbc', '\n', mbc)

mcr = m.closure_slides()
mbc = MatrixBinaryClosure(mcr)
print('mbc', '\n', mbc)

print("end")
