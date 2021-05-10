import graphm.factor
import graphm.matrixbinary

Factor =  graphm.factor.Factor
MatrixBinary =  graphm.matrixbinary.MatrixBinary

"""
	tests operations
"""
m = 1000
print('exponent, bit_length, bit_length_h, bit_length_s, exponent, operations, operations_h, operations_s, exponent, binary, binary_h, binary_s')
for i in range(2, m):
	f = Factor(i)
	f_h = Factor(i, optimize='hard')
	f_s = Factor(i, optimize='soft')
	ops = f.operations()
	ops_h = f_h.operations()
	ops_s = f_s.operations()
	binary = bin(i)[2:]
	print(i, f.exponent.bit_length(), f_h.exponent.bit_length(), f_s.exponent.bit_length(), i, ops, ops_h, ops_s, i, binary, bin(i)[2:], bin(f.exponent)[2:], sep=',')

"""
	tests on matrix

def matrix_product(matrix, expo):
	mr = matrix.copy()
	for _ in range(1, f):
		mr *= matrix
	return mr
	
s = 200
for f in range(100, 1100, 100):
	print('exponent:', f)
	print('-------------- matrix')
	m = MatrixBinary(random=(s,s))
	mu = MatrixBinary(unity=s)
	mi = m + mu
	print(mi)
	
	print('-------------- factor')
	factor = Factor(f)
	print('factor:', factor)
	result, count = factor.power(mi)
	print('result:', result)
	print('operations:', count)
	
	mr = matrix_product(mi, f)
	print('-------------- test')
	print('test:', result == mr)
	print()
print('end')
"""


"""
	tests on numbers
"""

n = 2
for f in (0, 242, 1024, 1023, 65536, 65535):
	factor = Factor(f)
	print(f)
	print(factor)
	result, count = factor.power(n)
	print(result)
	print(count)
	print(result == n**f)
	print()


n = 65536
f = Factor(n)
print(n ,f)
n = 1024
f = Factor(n)
print(n ,f)
n = 1023
f = Factor(n)
print(n ,f)
n = 0
f = Factor(n)
print(n ,f)

"""
test on the gap between 2** et 2**2**i
"""
import math
base = 4
l = [2**i for i in range(base,12)]
for i in l:
	print(int(math.log2(i // base)), i.bit_length() - base.bit_length())

l = [2**i for i in range(12)]
for i in l:
	print(int(math.log2(i)), i.bit_length())

m = 8
i2 = [2**i for i in range(m)]
i22 = [2**2**i for i in range(m)]

lc = {}
for i in range(len(i22)):
	c = 0
	i22_tmp = i22[i-1]
	while i22_tmp < i22[i]:
		c += 1
		i22_tmp = i22_tmp + i22_tmp
	lc[i22[i]] = c

print(lc)

"""
"""
exponent = 242
f = Factor(exponent)
result, count = f.power(2)
print(result, count)
result, count = f.power(3)
print(result, count)

"""
"""
n = 1023
n = 242
f = Factor(n)
print(n ,f)
#f.str_factor()
r = f.power(2)
print(n ,r)

l = [{2: [{1}]}, {1: [{0}]}, {0: [{0}]}]
exponent = 212
print('exponent', exponent)
exponents = Factor.get_exponentsof2(exponent)
print('exponents', exponents)
elementaries = Factor.get_elementaries(exponents)
print('elementaries', elementaries)
factor = Factor.get_factorization(elementaries)
print('factor', factor)

print()
exponent = 11
print('exponent', exponent)
exponents = Factor.get_exponentsof2(exponent)
print('exponents', exponents)
elementaries = Factor.get_elementaries(exponents)
print('elementaries', elementaries)
factor = Factor.get_factorization(elementaries)
print('factor', factor)

"""
import datetime
t1 = datetime.datetime.now()
for _ in range(1000000):
	for s in  'sdfsgfqghsdfhdhhhhhhsfgh':
		s.zfill(10)
		#s.rjust(10, '0')
t2 = datetime.datetime.now()
print(" : ", t2 - t1)
"""

