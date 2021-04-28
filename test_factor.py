from graphm.factor import Factor
"""
"""
number = 242
d = Factor(number)
print(d)

"""
r = 242
print(r, Factor.get_coefficients(r))
r = 11
print(r, Factor.get_power(r))

number = 242
print('number', number)
coefficients = Factor.get_coefficients(number)
print('coefficients', coefficients)
elementaries = Factor.get_elementaries(coefficients)
print('elementaries', elementaries)
facto = Factor.factor(elementaries)
print('facto', facto)

import datetime
t1 = datetime.datetime.now()
for _ in range(1000000):
	for s in  'sdfsgfqghsdfhdhhhhhhsfgh':
		s.zfill(10)
		#s.rjust(10, '0')
t2 = datetime.datetime.now()
print(" : ", t2 - t1)
"""