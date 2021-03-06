import graphm
MatrixBinary = graphm.MatrixBinary
MatrixBinarySlides = graphm.MatrixBinarySlides

"""
	MATRIX BINARY SLIDES
"""

n = 20

#matrix = ['0000000100', '1000000010', '0000101000', '1000010001', '0000010000', '0010001000', '0000100000', '0001000000', '0010000100', '0100000010']
#m = MatrixBinary(boolean=matrix)
m = MatrixBinary(random=(n, n))
print('m', m)
print('m matrixM', m.matrixM)
#g = GraphM(binary=m.matrixM)
#g.draw("files/mbs.png", nodes_style='int')

m = MatrixBinary(boolean=['00001', '00100', '00010', '00000', '01001'])
mc = m.closure_slides()
mbs = MatrixBinarySlides(mc)
print(mbs)

mc = m.closure_matrix()
mbs = MatrixBinarySlides(mc)
print(mbs)

mcs = m.closure_slides()
#print('mc = ', len(mc), '\n', mc)
mbs = MatrixBinarySlides(mcs)
print('mbs', '\n', mbs)
"""
print('------------------------')
print('report'), print(mbs.str_report())
"""

#print('m', len(m), '\n', m)
#print('successors', mbs.successors)

"""
"""
n = 10
c = 0
l = 0
while l < 3 and c < 200:
	m = MatrixBinary(random=(n, n), level=100)
	mbs = MatrixBinarySlides(m.closure_slides())
	dc = mbs.connectivity()
	l = len(dc['nodes_connected'])
	print(l, end=' ')
	c += 1
print('')
print('c', c)
print('------------------------')
for i, v in dc.items():
	if i in ('reached', 'count', 'graph_connected_fully'): print(i, '\t\t', v)
	else: print(i, '\t\t', len(v), '\n', v)

#all = set(range(mbs.dim))
print('start')
loners = [i for i in range(mbs.dim) if mbs.closureM[i] == 0 and mbs.closureN[i] == 0]
conexities = [mbs.closureM[i] & mbs.closureN[i] for i in range(mbs.dim) if i not in loners]
conexities_not = [i for i in range(len(conexities)) if conexities[i] == 0]
conexitiesS = [bin(line)[2:].zfill(mbs.dim) for line in conexities if line != 0]
lines = set(conexitiesS)
nodes = [[i for i in range(mbs.dim) if line[i] == '1'] for line in lines]
for line in conexitiesS: print(line)
print('loners', len(loners), ':', loners)
print('conexities_not', len(conexities_not), ':', conexities_not)
print('conexities', len(conexities), ':', conexities)
print('lines', len(lines), ':', lines)
print('nodes', len(nodes), ':', nodes)
for i in range(len(nodes)): print(len(nodes[i]), ':', nodes[i])

print("end")
