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
		self.factors, self.count = Factor.factor(self.elementaries)
	
	def __repr__(self):
		return f"number: {self.number}\nfactors: {self.factors}\ncount: {self.count}"
	
	def __str__(self):
		string = str(self.factors)
		d = {	': ': '*', ',': ' +', '[': '(', 	']': ')', '{': '', '}': ''}
		for s, r in d.items():
			string = string.replace(s, r)
		return string.strip('()')
		
	# TODO: wrong string replace
	def str_factor(self):
		string = str(self.factors)
		d = {	': ': '*', ',': ' *', '[': '(', 	']': ')', '{': '', '}': ''}
		for s, r in d.items():
			string = string.replace(s, r)
		indexes = list(set.union(*self.elementaries))
		indexes.sort(reverse=True)
		for index in indexes:
			string = string.replace(str(index), str(2**index))
		return string.strip('()')
		
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
#			indexes = {i: 2**(i-1) if i >0 else 0 for i in range(max_e.bit_length() + 1)}
#			indexes_factor = {i: 2**(indexes[i]) for i in range(len(indexes))}
			indexes = {i: 2**i for i in range(max_e.bit_length())}
			indexes_factor = {i: 2**(indexes[i]) for i in range(len(indexes))}
			index_dec = [indexes[i] for i in range(len(indexes) - 1)]
			index_dec.insert(0,1)
			
			base_tmp = bases[0]
			for i in range(len(indexes)):
				for ii in range(index_dec[i]):
					base_tmp = base_tmp * base_tmp
				bases[indexes[i]] = base_tmp
			return bases

		def calc(elements, content):
			if isinstance(elements, list):
				for element in elements:
					result = content * bases[element] if content else bases[element]
			else:
				result = content * bases[elements] if content else bases[elements]
			return result
		def power(element, power, content):
			result = element
			for _ in range(1, power):
				result = result * element
			return  content * result if content else result
		
		def calcrec(factors, element):
			if isinstance(factors, int):
				return calc(factors, element)
			
			for elements in factors:
				if isinstance(elements, dict):
					index, value = elements.popitem()
					result = calcrec(value, bases(index))
					content = power(bases[index],result, content)
				else:
					content = calc(elements, content)
			return content
		
		if not hasattr(obj, '__add__'):
			raise ValueError("The given object has no method for addition")
		if not hasattr(obj, '__mul__'):
			raise ValueError("The given object has no method for multiplication")
		
		if obj:
			bases = bases(obj, max({i for l in self.elementaries for i in l}))
			factors = deepcopy(self.factors)
			result = calcrec(factors, None)
		else:
			result = None
		return result

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
			r = [next(iter(i)) if len(i) == 1 else i for i in content]
			r.sort(reverse=True)
			return r
		def remove(content: list, index_s: set):
			""" return content reduced by index
			"""
			return [i.difference(index_s) if i.difference(index_s) else {0} for i in content]
		def unique(content: list, index: int):
			""" return the unique element according to the index and content
			"""
			content = content[0].pop()
			if content:
				if content != index:
					r = {index: content}
				else:
					r = content
			else:
				r = index
			return r
		def factorec(indexes: iter, factors: list, count: int):
			if not indexes or not factors:
				return (factors, count)
			
			for index in indexes:
				if isin(factors, index):
					count += 1
					selected= [i for i in factors if isinstance(i, set) and index in i]
					[factors.remove(i) for i in selected]
					content = remove(selected, {index})
					if isunique(content):
						if len(content) == 1:
							factors.append(unique(content, index))
						else:
							factors.append({index: deep(content)})
					elif content:
						content, count = factorec(indexes[indexes.index(index) +1:], content, count)
						factors.append({index: content})
						
			return (factors, count)
		
		indexes = list(set.union(*elementaries, {0}))
		indexes.sort(reverse=True)
		factors = [i.copy() for i in elementaries]
		return factorec(indexes, factors, 0)
		
		