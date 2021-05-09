import graphm
Graph = graphm.Graph
MatrixBinary = graphm.MatrixBinary
MatrixBoolean = graphm.MatrixBoolean
MatrixBinaryClosure = graphm.MatrixBinaryClosure

m = MatrixBinary(boolean=['01001', '00100', '01010', '00001', '01010'])
g = Graph(binary=m, node_style='int')
g.draw("files/test_binaryclosure-1.svg", ext='svg')

mbc = MatrixBinaryClosure(m.closure_matrix())
connectivity = mbc.connectivity()
print(connectivity)

m = MatrixBinary(boolean=['010010', '001000', '010100', '010010', '000000', '000000'])
g = Graph(binary=m, node_style='int')
g.draw("files/test_binaryclosure-2.svg", ext='svg')

mbc = MatrixBinaryClosure(m.closure_matrix())
connectivity = mbc.connectivity()
print(connectivity)

paths = mbc.matrix.paths_from(1)
print(paths)

"""
	test all get_closure
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
"""


print("end")
