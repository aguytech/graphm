from graphm.factor import Factor
"""
number = 242
f = Factor(number)
print(f)

number = 11
f = Factor(number)
print(f)
"""

"""
"""
r = Factor.get_bases(8)


n = 242
f = Factor(n)
print(f)
n = 65536
f = Factor(n)
n = 1024
f = Factor(n)
n = 0
f = Factor(n)
n = f.calculate(2)
print()
n = 1023
print(Factor(n))

"""
l = [{2: [{1}]}, {1: [{0}]}, {0: [{0}]}]
number = 212
print('number', number)
coefficients = Factor.get_coefficients(number)
print('coefficients', coefficients)
elementaries = Factor.get_elementaries(coefficients)
print('elementaries', elementaries)
facto = Factor.factor(elementaries)
print('facto', facto)

print()
number = 11
print('number', number)
coefficients = Factor.get_coefficients(number)
print('coefficients', coefficients)
elementaries = Factor.get_elementaries(coefficients)
print('elementaries', elementaries)
facto = Factor.factor(elementaries)
print('facto', facto)
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

