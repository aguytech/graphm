from graphm.factor import Factor
exp = 16
max = 1024

"""
import math

base = 4
l = [2**i for i in range(base,12)]
for i in l:
	print(int(math.log2(i // base)), i.bit_length() - base.bit_length())

l = [2**i for i in range(12)]
for i in l:
	print(int(math.log2(i)), i.bit_length())

c = 0
lc = {}
n = 16
while n < max:
	c += 1
	n += n
	lc[c] = (n, n//exp, int(math.log(n//exp, 2)))

print(lc)

c = 0
lc = {}
n = 16
while n < max:
	c += 1
	n += n
	lc[c] = (n, n//exp)

print(lc)

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
number = 242
f = Factor(number)
result, count = f.calculate(2)
print(result, count)
result, count = f.calculate(3)
print(result, count)
"""

"""
n = 2
for f in (0, 242, 1024, 1023, 65536, 65535):
	factor = Factor(f)
	print(f)
	print(factor)
	result, count = factor.calculate(n)
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

"""
n = 1023
n = 242
f = Factor(n)
print(n ,f)
#f.str_factor()
r = f.calculate(2)
print(n ,r)

l = [{2: [{1}]}, {1: [{0}]}, {0: [{0}]}]
number = 212
print('number', number)
exponents = Factor.get_exponents(number)
print('exponents', exponents)
elementaries = Factor.get_elementaries(exponents)
print('elementaries', elementaries)
factor = Factor.get_factor(elementaries)
print('factor', factor)

print()
number = 11
print('number', number)
exponents = Factor.get_exponents(number)
print('exponents', exponents)
elementaries = Factor.get_elementaries(exponents)
print('elementaries', elementaries)
factor = Factor.get_factor(elementaries)
print('factor', factor)
"""

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

