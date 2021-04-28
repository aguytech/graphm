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
		return f"number: {self.number}\nfact: {self.fact}\ncount: {self.count}"
	
	def __str__(self):
		def str_rec(fact):
			if isinstance(fact, int):
				return str(fact[0].pop())
			p = ''
			for d in fact:
				index, content = d.popitem()
				content = str_rec(content)
				if index == 0 and content == '0':
					p += f"{index} + "
				elif content == '0':
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
		def bases(obj: object, max_e: int):
			bases = {0: obj}
			indexes = {i: 2**(i-1) if i > 0 else 0 for i in range(max_e.bit_length() + 1)}
			for index in range(1, len(indexes)):
				bases[indexes[index]] = bases[indexes[index - 1]] * bases[indexes[index - 1]]
			return bases
		
		def calc(fact):
			if isinstance(fact[0], set):
				index = fact[0].pop()
				return bases[index]
			for d in fact:
				index, content = d.popitem()
				content = calc(content)
				if index == 0 and str(content) == '0':
					p = f"{index} + "
				elif str(content) == '0':
					p = f"{index} + "
				else:
					p = f"{index}*({content}) + "
					
			return p.rstrip(' +')
		
		if not hasattr(obj, '__add__'):
			raise ValueError("The given object has no method for addition")
		if not hasattr(obj, '__mul__'):
			raise ValueError("The given object has no method for multiplication")
		
		max_e = max({i for l in self.elementaries for i in l})
		bases = bases(obj, max_e)
		fact = deepcopy(self.fact)
		p = calc(fact)
		return p

	@staticmethod
	def factor(elementaries: iter):
		def isunique(content: list):
			""" return True if each element in content set is unique in content
			""" 
			return len([i for c in content for i in c]) == len({i for c in content for i in c})
		def isin(content: list, index: int):
			""" return True if each element in content set is unique in content
			""" 
			if [1 for i in content if isinstance(i, int) and index == i] \
			or [1 for i in content if isinstance(i, set) and index in i]:
				return True
		def deep(content: list):
			""" return deep element wich inside a set
			""" 
			return [next(iter(i)) if len(i) == 1 else i for i in content]
		def remove(content: list, index_s: set):
			""" return content reduced by index
			"""
			return [i.difference(index_s) if i.difference(index_s) else {0} for i in content]
		def unique(content: list, index: int):
			""" return the unique element according to the index and content
			"""
			content = content[0].pop()
			if index and content:
				r = {index: content}
			elif index:
				r = index
			elif content:
				r = content
			else:
				r = 0
			return r
		def factorec(indexes: iter, fact: list, count: int):
			if not indexes or not fact:
				return (fact, count)
			
			for index in indexes:
				
				if isin(fact, index):
					count += 1
					content = [i for i in fact if isinstance(i, set) and index in i]
					[fact.remove(i) for i in content]
					content = remove(content, {index})
					if isunique(content):
						if len(content) == 1:
							fact.append(unique(content, index))
						else:
							fact.append({index: deep(content)})
					elif content:
						content, count = factorec(indexes[indexes.index(index) +1:], content, count)
						fact.append({index: content})
						
			return (fact, count)
		
		indexes = list(set.union(*elementaries, {0}))
		indexes.sort(reverse=True)
		fact = [i.copy() for i in elementaries]
		return factorec(indexes, fact, 0)
		
		