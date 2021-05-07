'''
Created on Apr 26, 2021

@author: salem Aguemoun
'''
from copy import deepcopy

class Factor(object):
	'''
	classdocs
	'''

	def __init__(self, exponent: int, optimize: str=''):
		''' instantiate an object with the required exponent and a method of product optimization
		
		:param int exponent: initial exponent of product
		:param str optimize: the method used to optimize the product: None, 'soft' or 'hard'
		
			default: None
		'''
		self.set_number(exponent, optimize)
		self.real = True
		self.coefficients = Factor.get_exponents(self.number)
		self.elementaries = Factor.get_elementaries(self.coefficients, real=self.real)
		self.factorization, self.count = Factor.get_factorization(self.elementaries, real=self.real)
	
	def __repr__(self):
		return f"number: {self.number}\nfactorization: {self.factorization}\ncount: {self.count}"
	
	def __str__(self):
		string = str(self.factorization)
		d = {	': ': '*', ',': ' +', '[': '(', 	']': ')', '{': '', '}': ''}
		for s, r in d.items():
			string = string.replace(s, r)
		string = string[1:-1] if string[0] == '(' else string
		return string
		
	def operations(self):
		def set_bases(max_factor: int):
			indexes = [2**i for i in range(1, max_factor.bit_length())]
			bases = {1: 1}
			for i in range(len(indexes)):
				bases[indexes[i]] = 1
			return bases
		
		def add_bases(factor):
			factor_loop = max(bases.keys())
			loop = factor.bit_length() - factor_loop.bit_length()
			for _ in range(loop):
				factor_loop *= 2
				bases[factor_loop] = 1

		def calc(factor, factorsof):
			factor_final = factor * factorsof
			if factor_final not in bases.keys():
				add_bases(factor_final)
			return bases[factor_final]
		
		def set_content(result, content, ops):
			if content != 0:
				content = content + result
				ops += 1
			else:
				content = result
			return (content, ops)
			
		def calcrec(factorization, factor=1, ops=0):
			content = 0

			for element in factorization:
				if isinstance(element, dict):
					factor_loop, factors = element.popitem()
					if isinstance(factors, int):
						result = calc(factor_loop, factors)
					else:
						result, ops = calcrec(factors, factor * factor_loop, ops)
					content, ops = set_content(result, content, ops)
				else:
					result = calc(factor, element)
					content, ops = set_content(result, content, ops)
			return (content, ops)
		
		ops = 0
		if self.factorization:
			max_factor = max({i for l in self.elementaries for i in l})
			bases = set_bases(max_factor)
			factorization = deepcopy(self.factorization)
			_, ops = calcrec(factorization)
			# -1 for the first element in bases
			ops += len(bases) - 1
		return (ops)

	def power(self, obj: object):
		def set_bases(obj: object, max_factor: int):
			indexes = [2**i for i in range(1, max_factor.bit_length())]
			bases = {1: obj}
			base_tmp = bases[1]
			for i in range(len(indexes)):
				base_tmp *= base_tmp
				bases[indexes[i]] = base_tmp
			return bases
		
		def add_bases(factor):
			factor_loop = max(bases.keys())
			loop = factor.bit_length() - factor_loop.bit_length()
			base_tmp = bases[factor_loop]
			for _ in range(loop):
				base_tmp *= base_tmp
				factor_loop *= 2
				bases[factor_loop] = base_tmp

		def calc(factor, factorsof):
			factor_final = factor * factorsof
			if factor_final not in bases.keys():
				add_bases(factor_final)
			return bases[factor_final]
		
		def set_content(result, content, ops):
			if content != 1:
				content = content * result
				ops += 1
			else:
				content = result
			return (content, ops)
			
		def calcrec(factorization, factor=1, ops=0):
			content = 1
			
			for element in factorization:
				if isinstance(element, dict):
					factor_loop, factors = element.popitem()
					if isinstance(factors, int):
						result = calc(factor_loop, factors)
					else:
						result, ops = calcrec(factors, factor * factor_loop, ops)
					content, ops = set_content(result, content, ops)
				else:
					result = calc(factor, element)
					content, ops = set_content(result, content, ops)
			return (content, ops)
		
		if not hasattr(obj, '__mul__'):
			raise ValueError("The given object has no method for multiplication")
		
		ops = 0
		if obj and self.factorization:
			max_factor = max({i for l in self.elementaries for i in l})
			bases = set_bases(obj, max_factor)
			factorization = deepcopy(self.factorization)
			result, ops = calcrec(factorization)
			# -1 for the first element in bases
			ops += len(bases) - 1
		elif obj and not self.factorization:
			result = obj
		else:
			result = None
		return (result, ops)

	@staticmethod
	def get_bases(number: int) -> list:
		length = len(Factor.get_int2list(number))
		return [2**i for i in range(1, length)]

	@staticmethod
	def get_elementaries(coefficients: iter, real: bool=False):
		"""
		:param bool real: if True return the real factor format: 2**factor
		"""
		elementaries = [Factor.get_power(c) for c in coefficients]
		if real:
			elementaries = [{2**i for i in s} for s in elementaries]
		return elementaries 
		
	@staticmethod
	def get_exponents(number: int) -> list:
		num = Factor.get_int2list(number)
		num.reverse()
		return [i for i in range(len(num)) if num[i] == '1']

	@staticmethod
	def get_factorization(elementaries: iter, real: bool=False):
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
			""" return deep element which inside a set
			""" 
			result = [i for j in content for i in j]
			result.sort(reverse=True)
			return result
		
		def remove(content: list, index_s: set):
			""" return content reduced by index
			"""
			return [i.difference(index_s) if i.difference(index_s) else {neutral} for i in content]
		
		def unique(content: list, index: int):
			""" return the unique element according to the index and content
			"""
			content = content[0].pop()
			if content and content != neutral:
				if content != index:
					result= {index: content}
				else:
					result= content
			else:
				result= index
			return result
		
		def factorec(indexes: iter, factorization: list, count: int=0):
			if not indexes or not factorization:
				return (factorization, count)
			
			for index in indexes:
				if isin(factorization, index):
					count += 1
					selected= [i for i in factorization if isinstance(i, set) and index in i]
					[factorization.remove(i) for i in selected]
					content = remove(selected, {index})
					if isunique(content):
						if len(content) == 1:
							factorization.append(unique(content, index))
						else:
							factorization.append({index: deep(content)})
					elif content:
						content, count = factorec(indexes[indexes.index(index) +1:], content, count)
						factorization.append({index: content})
						
			return (factorization, count)
		
		neutral = 1 if real else 0
		indexes = list(set.union(*elementaries, {neutral}))
		indexes.sort(reverse=True)
		factorization = [i.copy() for i in elementaries]
		return factorec(indexes, factorization)
		
	@staticmethod
	def get_int2list(number: int) -> list:
		return list(bin(number)[2:])

	@staticmethod
	def get_power(number: int) -> set:
		n = list(bin(number)[2:])
		n.reverse()
		p = {2**i for i,n in enumerate(n) if n =='1'}
		return p if p else {0}

	def set_number(self, number: int, optimize: str):
		def hard(number):
			return int('1' + '0' * (number.bit_length()), 2)
		
		def soft(number: int, number2: int) -> int:
			if number2[1:2] == '1':
				number = hard(number)
			else:
				index = number2.find('1', 1)
				number = number2[0:index-  1] + '1'  + '0'*(len(number2) - index)
				number = int('0b' + number, 2)
			return number
				
		if number and optimize and number.bit_length() > 1:
			number2 = bin(number)[2:]
			if number2.count('1') > 1:
				if optimize == 'hard':
					number = hard(number)
				elif optimize == 'soft':
					number = soft(number, number2)
			
		self.number = number

	# TODO: wrong string replace
	def str_factor(self):
		string = str(self.factorization)
		d = {	': ': '*', ',': ' *', '[': '(', 	']': ')', '{': '', '}': ''}
		for s, r in d.items():
			string = string.replace(s, r)
		indexes = list(set.union(*self.elementaries))
		indexes.sort(reverse=True)
		for index in indexes:
			string = string.replace(str(index), str(2**index))
		return string.strip('()')
		

		