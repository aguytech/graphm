
"""
	PERFORMANCE MATRIX_BOOLEAN
"""
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
	PERFORMANCE MATRIX_BINARY
"""
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
	
	