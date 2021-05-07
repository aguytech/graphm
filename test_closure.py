import graphm
Graph = graphm.Graph
MatrixBinary = graphm.MatrixBinary
MatrixBoolean = graphm.MatrixBoolean

"""
	test different closures
"""
n = 30
for _ in range(10):
	m = MatrixBinary(random=(n,n), level=50)
	mb = m.export2list()
	closure = m.get_closure_reflective(add=True)
	closure_full = m.get_closure_reflective(add=True, full=True)
	print('closure == closure_full', closure == closure_full, sep='\t')
	closure_ro, count = m.get_closure_reflective_optimized()
	closure_ros, count = m.get_closure_reflective_optimized(optimize='soft')
	closure_roh, count = m.get_closure_reflective_optimized(optimize='hard')
	print('closure == closure_ro', closure == closure_ro, sep='\t')
	print('closure == closure_ros', closure == closure_ros, sep='\t')
	print('closure == closure_roh', closure == closure_roh, sep='\t')
	closure_matrix = m.get_closure_matrix()
	closure_matrix_full = m.get_closure_matrix(full=True)
	closure_matrix = MatrixBinary.add_unit(closure_matrix[0])
	closure_matrix_full = MatrixBinary.add_unit(closure_matrix_full[0])
	print('closure == closure_matrix', closure == closure_matrix, sep='\t')
	print('closure == closure_matrix_full', closure == closure_matrix_full, sep='\t')
	closure_slides = m.get_closure_slides()
	closure_slides_full = m.get_closure_slides(full=True)
	closure_slides = MatrixBinary.get_unit_added(closure_slides[0], n)
	closure_slides_full = MatrixBinary.get_unit_added(closure_slides_full[0], n)
	print('closure == closure_slides', closure.matrixM == closure_slides, sep='\t')
	print('closure == closure_slides_full', closure.matrixM == closure_slides_full, sep='\t')
	print()

#m = MatrixBinary(matrix=([128, 0, 1024, 0, 268435460, 4, 33554432, 16777216, 269500992, 64, 128, 17, 512, 524288, 8684548, 524292, 8192, 16777216, 0, 1572864, 4097, 64, 0, 24, 131072, 0, 8192, 33554432, 4194304, 0],30))
		
"""
	natural join

m1 = MatrixBoolean(matrix=['001001', '000001', '000000', '001000', '000100', '100010'])
m2 = MatrixBoolean(matrix=['000110', '001000', '000001', '000001', '100000', '000010'])
j = MatrixBoolean(matrix=['0001100000', '0010000000', '0000010000', '0000010000', '1000000000', '0000100001', '0001000001', '0000000010', '0000010000', '0000001000'])
print(m1)
print(m2)
g1 = Graph(boolean=m1, graph_attr={'label': f'M1'}, nodes=('A,B,C,D,E,F'))
g1.draw(f"files/M1.svg", ext='svg')
g2 = Graph(boolean=m2, graph_attr={'label': f'M2'}, nodes=('M,N,O,D,P,F'))
g2.draw(f"files/M2.svg", ext='svg')
j = Graph(boolean=j, graph_attr={'label': f'J'}, nodes=('A,B,C,D,E,F,M,N,O,P'))
j.draw(f"files/J.svg", ext='svg')
"""


"""
closure

for _ in range(1):
	dim = 6
	m = MatrixBoolean(matrix=['010100','000000','010010','000001','001100','000000'])
	#m = MatrixBoolean(random=(dim, dim), level=300)
	
	i = MatrixBoolean(unity=dim)
	mi = m + i
	
	mp = {0: m.copy()}
	mpc = m.copy()
	mc = {0: mi.copy()}
	g = Graph(boolean=mp[0], node_style='int', graph_attr={'label': f'rank 1'})
	g.draw("files/closure-1.svg", ext='svg')
	for i in range(1, dim):
		mp[i] = mp[i-1] * m
		mpc = mpc + mp[i]
		mc[i] = mc[i-1] * mi
		g = Graph(boolean=mp[i], node_style='int', graph_attr={'label': f'rank {i}'})
		g.draw(f"files/rank-{i}.svg", ext='svg')
		gc = Graph(boolean=mc[i], node_style='int', graph_attr={'label': f'closure - rank {i}'})
		gc.draw(f"files/closure-{i}.svg", ext='svg')
		print()
		print(i)
		print('mp')
		print(mp[i])
		print('mc')
		print(mc[i])

	mpc += mi
	print(mpc == mc[dim-1])
"""
	
"""
	for k, v in mp.items():
		print()
		print('k', k)
		#print(mp[k])
		#print(mc[k])
		print('mc[k] == mp[k]', mc[k] == mp[k])
		print('mc[k] == mpc[k]', mc[k] == mpc[k])
	
	print('mc_c', mc_c)
	print('mp[dim-1]', mp[dim-1])
	print('mc_c == mp[dim-1]', mc_c == mp[dim-1])
"""

print('end')


