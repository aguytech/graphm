import datetime
import graphm
MatrixBinary = graphm.matrixbinary.MatrixBinary
MatrixBoolean = graphm.matrixboolean.MatrixBoolean
Factor = graphm.factor.Factor

"""
	PERFORMANCE MATRIX_BOOLEAN
from graphm import MatrixBoolean
import datetime

n = 100
m = MatrixBoolean(random=(n, n))
print(m)

t1 = datetime.datetime.now()
s = m
for i in range(n-2):
	s = s * m
t2 = datetime.datetime.now()
print(m)
print(t2 - t1)
"""

"""
	factor operations far far away
"""
m = 1000
print('exponent, operations, operations_h, operations_s')
for i in range(1000, 40200, 200):
	#print('-------------- factor')
	f = Factor(i)
	f_h = Factor(i, optimize='hard')
	f_s = Factor(i, optimize='soft')
	ops = f.operations()
	ops_h = f_h.operations()
	ops_s = f_s.operations()
	print(i, ops, ops_h, ops_s, sep=',')
	#print()
print('end')

"""
	factor & matrixbinary
def matrix_product(matrix, expo):
	mr = matrix.copy()
	for _ in range(1, f):
		mr *= matrix
	return mr

s = 20
print('exponent, operations, operations2, product, factor')
for f in range(100, 1100, 100):
	#print('exponent:', f)
	m = MatrixBinary(random=(s,s))
	mu = MatrixBinary(unity=s)
	mi = m + mu
	
	#print('-------------- factor')
	factor = Factor(f)
	ops = factor.operations()
	t1 = datetime.datetime.now()
	result, count = factor.calculate(mi)
	t2 = datetime.datetime.now()
	#print('operations:', count)
	#print('time:', t2 - t1)
	tf = t2 - t1
	
	#print('-------------- product')
	t1 = datetime.datetime.now()
	#mr = matrix_product(mi, f)
	t2 = datetime.datetime.now()
	tp = t2 -t1
	#print('time:', t2 - t1)
	print(f, count, ops, tp, tf, sep=',')
	#print()
print('end')
"""


"""
	matrixbinary
	
import functools
for s in range(20,320,20):
	dimM = s
	dimN = s
	matrix1 = MatrixBinary(random=(dimM,dimN))
	matrix2 = MatrixBinary(random=(dimM,dimN))
	# matrix1 = MatrixBoolean(random=(dimM,dimN))
	# matrix2 = MatrixBoolean(random=(dimM,dimN))
	t1 = datetime.datetime.now()
	for _ in range(s):
		# matrix = [[0 for _ in range(matrix1.dimN)] for _ in range(matrix1.dimM)]
		#	for m in range(matrix1.dimM):
		# 		for n in range(matrix2.dimN):
		# 			l = (matrix1.get_value(m, i) & matrix2.get_value(i, n) for i in range(matrix1.dimN))
		# 			# with functools package
		# 			matrix[m][n] = functools.reduce(lambda x, y: x | y, l)

		matrixM = [0]*matrix1.dimM
		for m in range(matrix1.dimM):
			line = [('0' if (matrix1.matrixM[m] & matrix2.matrixN[n]) == 0 else '1') for n in range(matrix2.dimN)]
			matrixM[m] = int('0b' + ''.join(line), 2)
		# matrixN = [0]*matrix2.dimN
		# for n in range(matrix2.dimN):
		# 	line = [('0' if (matrix2.matrixN[n] & matrix1.matrixM[m]) == 0 else '1') for m in range(matrix1.dimM)]
		# 	matrixN[n] = int('0b' + ''.join(line), 2)
	
		matrix = [MatrixBinary.get_int2str(m, dimN) for m in matrixM]
		matrixN = [int('0b' + ''.join(line[n] for line in matrix), 2) for n in range(dimN)]

	t2 = datetime.datetime.now()
	print(s, ':', t2 - t1)
"""


"""
	multiplication

n = 1000
loop = 10
m = MatrixBinary(random=(n, n))
print(m)

t1 = datetime.datetime.now()
s = m
for i in range(1, loop):
	s = s * m
t2 = datetime.datetime.now()
print(m)
print(t2 - t1)
"""

"""
	PERFORMANCE MATRIX_BINARY
from graphm import MatrixBinary
import datetime

for n in range(10,210,10):
	m = MatrixBinary(random=(n, n))
	#print(m)
	
	t1 = datetime.datetime.now()
	mc = m.get_closure_slides_dict()
	t2 = datetime.datetime.now()
	print(n, " : ", t2 - t1)
"""

"""
	PERFORMANCE MATRIX_BINARY_SLIDES
from graphm import MatrixBinarySlides
from graphm import MatrixBinary
import datetime

n = 10
for n in range(50,550,50):
	for _ in range(10):
		m = MatrixBinary(random=(n, n))
		#print(m)
		
		t1 = datetime.datetime.now()
		mc = m.get_closure_slides()
		mbs = MatrixBinarySlides(binary=mc)
		t2 = datetime.datetime.now()
		#print(mbs)
		print(mbs.deep, n, " : ", t2 - t1)
"""
	
	