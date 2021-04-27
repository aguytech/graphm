'''
Created on Apr 26, 2021

@author: nikita
'''
from copy import deepcopy

class Factor(object):
	'''
	classdocs
	'''

	def __init__(self, number: int):
		'''
		Constructor
		'''
		self.number= number
		self.coefficients = Factor.get_coefficients(number)
		self.elementaries = Factor.get_elementaries(self.coefficients)
		self.fact, self.count = Factor.factor(self.elementaries)
	
	def __repr__(self):
		return f"number: {self.number}\nfacto: {self.facto}\ncount: {self.count}"
	
	def __str__(self):
		def str_rec(fact):
			if isinstance(fact[0], set):
				return fact[0].pop()
			p = ''
			for d in fact:
				index, content = d.popitem()
				content = str_rec(content)
				if index == 0 and str(content) == '0':
					p += f"{index} + "
				elif str(content) == '0':
					p += f"{index} + "
				else:
					p += f"{index}*({content}) + "
					
			return p.rstrip(' +')
		
		fact = deepcopy(self.fact)
		p = str_rec(fact)
		return p
	
	@staticmethod
	def _dict_add(d: dict, index: int, item: iter) -> None:
		""" add in place item in sets contained in passed dictionary
		""" 
		if index in d:
			d[index].add(item)
		else:
			d[index] = {item}
		
	@staticmethod
	def get_coefficients(number: int) -> list:
		num = Factor.get_int2list(number)
		num.reverse()
		return [i for i in range(len(num)) if num[i] == '1']

	@staticmethod
	def get_int2list(number: int) -> list:
		return list(bin(number)[2:])

	@staticmethod
	def get_bases(number: int) -> list:
		length = len(Factor.get_int2list(number))
		return [2**i for i in range(1, length)]

	@staticmethod
	def get_power(number: int) -> set:
		n = list(bin(number)[2:])
		n.reverse()
		p = {2**i for i,n in enumerate(n) if n =='1'}
		return p if p else {0}

	@staticmethod
	def get_elementaries(coefficients: iter):
		return [Factor.get_power(c) for c in coefficients]
		
	def calculate(self, obj: object):
		if not hasattr(obj, '__add__'):
			raise ValueError("The given object has no method for addition")
		if not hasattr(obj, '__mul__'):
			raise ValueError("The given object has no method for multiplication")
		
		def bases(obj: object, max_e: int):
			elements = {0: obj}
			indexes = {i: 2**i for i in range(1, max_e.bit_length() + 1)}
			indexes[0] = 0
			for index in indexes:
				elements[indexes[index]] = elements[indexes[index - 1]] * elements[indexes[index - 1]]
			return elements
		
		def str_rec(fact):
			if isinstance(fact[0], set):
				return fact[0].pop()
			p = ''
			for d in fact:
				index, content = d.popitem()
				content = str_rec(content)
				if index == 0 and str(content) == '0':
					p += f"{index} + "
				elif str(content) == '0':
					p += f"{index} + "
				else:
					p += f"{index}*({content}) + "
					
			return p.rstrip(' +')
		
		max_e = max({i for l in self.elementaries for i in l})
		bases = bases(obj, max_e)
		fact = deepcopy(self.fact)
		p = str_rec(fact)
		return p

	@staticmethod
	def factor(elementaries: iter):
		def factorec(indexes: iter, fact: list, count: int):
			if not indexes or not fact:
				return (fact, count)
			
			for ii in range(len(indexes)):
				count += 1
				index = indexes[ii]
				index_s = {index}
				content = [fact[i] for i in range(len(fact)) if index in fact[i]]
				[fact.remove(i) for i in content]
				content = [v.difference(index_s) if v.difference(index_s) else {0} for v in content]
				if len(content):
					content, count = factorec(indexes[ii+1:], content, count)
				if content:
					fact.append({index: content})
			return (fact, count)
		
		indexes = list(set.union(*elementaries, {0}))
		indexes.sort(reverse=True)
		count = 0
		fact = [i.copy() for i in elementaries]
		fact
		return factorec(indexes, fact, count)
				
		
		
		
		
			
		