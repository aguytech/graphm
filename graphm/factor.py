'''
Created on Apr 26, 2021

@author: salem Aguemoun
'''
from copy import deepcopy

class Factor(object):
	"""
	- Factorize a product in exponent of 2
	- Reduce the number of operations to calculate the power of an object
	- Give a toolbox to manipulate binary operations
	
	.. WARNING:: to use the method power(), the object class must have implemented method __mul__()
	
	.. CAUTION:: Instance variables
	
	:var list exponentsof2: the exponents of 2 representing the given exponent
	:var list count: number of loops to get factorization
	:var list elementaries: exponents of 2 present in the factorization
	:var list factorization: factorization of exponent of 2 of product
	:var int exponent: exponent of calculated power
	:var bool real: if True the exponents of 2 are representing with a calculated format 2**e otherwise just e
	"""

	def __init__(self, exponent: int, optimize: str=''):
		''' instantiate an object with the required exponent and a method of product optimization
		
		:param int exponent: initial exponent of product
		:param str optimize: the method used to optimize the product: None, 'soft' or 'hard'
		
			default: None

		>>> factor = Factor(1)
		>>> print(factor)
		exponent: 1
		factorization: 1
		count: 1
		
		>>> factor = Factor(256)
		>>> print(factor)
		exponent: 256
		factorization: 256
		count: 1
		
		>>> factor = Factor(2125)
		>>> print(factor)
		exponent: 2125
		factorization: 256*2 + 16*4 + 4*(2 + 1) + 1
		count: 4
		
		>>> factor = Factor(2125, optimize='soft')
		>>> print(factor)
		exponent: 2176
		factorization: 256*2 + 16*2
		count: 2
		
		>>> factor = Factor(2125, optimize='hard')
		>>> print(factor)
		exponent: 4096
		factorization: 256*16
		count: 1
		'''
		self._set_exponent(exponent, optimize)
		self.real = True
		self.exponentsof2 = Factor.get_exponentsof2(self.exponent)
		self.elementaries = Factor.get_elementaries(self.exponentsof2, real=self.real)
		self.factorization, self.count = Factor.get_factorization(self.elementaries, real=self.real)
	
	def __repr__(self):
		"""
		Give a string representation of factorization
		
		:return: a string representation of factorization
		
		>>> factor = Factor(242)
		>>> repr(factor)
		'16*(4*(2 + 1) + 2 + 1) + 2'
		
		>>> factor = Factor(242)
		>>> repr(factor)
		'16*(4*(2 + 1) + 2 + 1) + 2'
		
		>>> factor = Factor(2125)
		>>> repr(factor)
		'256*2 + 16*4 + 4*(2 + 1) + 1'
		"""
		string = str(self.factorization)
		d = {	': ': '*', ',': ' +', '[': '(', 	']': ')', '{': '', '}': ''}
		for s, r in d.items():
			string = string.replace(s, r)
		string = string[1:-1] if string[0] == '(' else string
		return string
	
	def __str__(self):
		"""
		Give:
		
			* final exponent
			* string representation of factorization (repr())
			* loops count to factorize
		
		:return: exponent, factorization and loops count to factorize
		
		>>> factor = Factor(242)
		>>> repr(factor)
		'16*(4*(2 + 1) + 2 + 1) + 2'
		
		>>> factor = Factor(32767)
		>>> repr(factor)
		'256*(16*(4 + 2 + 1) + 4*(2 + 1) + 2 + 1) + 16*(4*(2 + 1) + 2 + 1) + 4*(2 + 1) + 2 + 1'
		"""
		return f"exponent: {self.exponent}\nfactorization: {repr(self)}\ncount: {self.count}"
		
	def operations(self) -> int:
		"""
		Give the number of operations to calculate the factorized power
		
		:return: the number of operations to calculate the factorized power
		:rtype: int
		
		>>> factor = Factor(242)
		>>> factor.operations()
		11
		
		>>> factor = Factor(32767)
		>>> factor.operations()
		28
		"""
		def set_bases(max_exponent: int) -> dict:
			"""
			Set intial bases from elementaries of the first level
			the bases are the powers of the object found in elementaries
			
			:param int max_exponent: the highest exponent found in elementaries
			
			:return: bases
			:rtype: dict
			"""
			indexes = [2**i for i in range(1, max_exponent.bit_length())]
			bases = {1: 1}
			for i in range(len(indexes)):
				bases[indexes[i]] = 1
			return bases
		
		def add_bases(exponent: int) -> None:
			"""
			Add bases to existing bases due to distribution of factorization
			
			:param int exponent: exponent found in distribution of factorization
			
			:return: bases
			:rtype: dict
			"""
			exponent_loop = max(bases.keys())
			loop = exponent.bit_length() - exponent_loop.bit_length()
			for _ in range(loop):
				exponent_loop *= 2
				bases[exponent_loop] = 1

		def calc(exponent, exponentsof) -> object:
			"""
			Calculate element by adding bases and returns the product power at the given exponent
			
			:param int exponent: the exponent
			:param int exponentsof: the exponent of exponent
			
			:return: the power of given object at the exponent of exponent from bases
			:rtype: object
			"""
			exponent_final = exponent * exponentsof
			if exponent_final not in bases.keys():
				add_bases(exponent_final)
			return bases[exponent_final]
		
		def set_content(result, content, ops):
			"""
			Set content from result and avoid making a product of the object with an integer
			"""
			if content != 0:
				content = content + result
				ops += 1
			else:
				content = result
			return (content, ops)
			
		def calcrec(factorization, exponent=1, ops=0):
			"""
			Recursive function to distribute factorization
			"""
			content = 0

			for element in factorization:
				if isinstance(element, dict):
					exponent_loop, exponents = element.popitem()
					if isinstance(exponents, int):
						result = calc(exponent_loop, exponents)
					else:
						result, ops = calcrec(exponents, exponent * exponent_loop, ops)
					content, ops = set_content(result, content, ops)
				else:
					result = calc(exponent, element)
					content, ops = set_content(result, content, ops)
			return (content, ops)
		
		ops = 0
		if self.factorization:
			max_exponent = max({i for l in self.elementaries for i in l})
			bases = set_bases(max_exponent)
			factorization = deepcopy(self.factorization)
			_, ops = calcrec(factorization)
			# -1 for the first element in bases
			ops += len(bases) - 1
		return (ops)

	def power(self, obj: object):
		"""
		Give the number of operations to calculate the factorized power
		
		:return: the number of operations to calculate the factorized power
		:rtype: int
		
		>>> factor = Factor(34)
		
		>>> factor.power(2)
		(17179869184, 6)
		
		>>> factor.power(3)
		(16677181699666569, 6)
		
		
		>>> factor = Factor(128)
		>>> factor.power(2)
		(4294967296, 5)
		
		>>> factor = Factor(127)
		>>> factor.power(2)
		(170141183460469231731687303715884105728, 12)
		"""
		def set_bases(obj: object, max_exponent: int):
			"""
			Set intial bases from elementaries of the first level
			the bases are the powers of the object found in elementaries
			
			:param int max_exponent: the highest exponent found in elementaries
			
			:return: bases
			:rtype: dict
			"""
			indexes = [2**i for i in range(1, max_exponent.bit_length())]
			bases = {1: obj}
			base_tmp = bases[1]
			for i in range(len(indexes)):
				base_tmp *= base_tmp
				bases[indexes[i]] = base_tmp
			return bases
		
		def add_bases(exponent):
			"""
			Add bases to existing bases due to distribution of factorization
			
			:param int exponent: exponent found in distribution of factorization
			
			:return: bases
			:rtype: dict
			"""
			exponent_loop = max(bases.keys())
			loop = exponent.bit_length() - exponent_loop.bit_length()
			base_tmp = bases[exponent_loop]
			for _ in range(loop):
				base_tmp *= base_tmp
				exponent_loop *= 2
				bases[exponent_loop] = base_tmp

		def calc(exponent, exponentsof):
			"""
			Calculate element by adding bases and returns the product power at the given exponent
			
			:param int exponent: the exponent
			:param int exponentsof: the exponent of exponent
			
			:return: the power of given object at the exponent of exponent from bases
			:rtype: object
			"""
			exponent_final = exponent * exponentsof
			if exponent_final not in bases.keys():
				add_bases(exponent_final)
			return bases[exponent_final]
		
		def set_content(result, content, ops):
			"""
			Set content from result and avoid making a product of the object with an integer
			"""
			if content != 1:
				content = content * result
				ops += 1
			else:
				content = result
			return (content, ops)
			
		def calcrec(factorization, exponent=1, ops=0):
			"""
			Recursive function to distribute factorization
			"""
			content = 1
			
			for element in factorization:
				if isinstance(element, dict):
					exponent_loop, exponents = element.popitem()
					if isinstance(exponents, int):
						result = calc(exponent_loop, exponents)
					else:
						result, ops = calcrec(exponents, exponent * exponent_loop, ops)
					content, ops = set_content(result, content, ops)
				else:
					result = calc(exponent, element)
					content, ops = set_content(result, content, ops)
			return (content, ops)
		
		if not hasattr(obj, '__mul__'):
			raise ValueError("The given object has no method for multiplication")
		
		ops = 0
		if obj and self.factorization:
			max_exponent = max({i for l in self.elementaries for i in l})
			bases = set_bases(obj, max_exponent)
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
		"""
		Give the sequence to the power of 2 to reach the given number
		
		:param int number: a integer
		
		:return: the sequence to the power of 2 to reach the given number
		:rtype: list
		
		>>> Factor.get_bases(1024)
		[2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
		
		>>> Factor.get_bases(124)
		[2, 4, 8, 16, 32, 64]
		"""
		length = len(Factor.get_int2list(number))
		return [2**i for i in range(1, length)]

	@staticmethod
	def get_elementaries(exponentsof2: iter, real: bool=False) -> list:
		"""
		Give the representation of the exponents of 2 decomposed into the exponent of 2
		 
		:param iter exponentsof2: exponents of 2 needed to represent intial exponent
		:param bool real: if True return the real exponent format: 2**exponent
		
		:return: he representation of the exponents of 2 decomposed into the exponent of 2
		:rtype: list
		
		>>> exponents = Factor.get_exponentsof2(242)
		>>> exponents
		[1, 4, 5, 6, 7]
		
		>>> Factor.get_elementaries(exponents)
		[{1}, {4}, {1, 4}, {2, 4}, {1, 2, 4}]
		
		>>> Factor.get_elementaries(exponents, real=True)
		[{2}, {16}, {16, 2}, {16, 4}, {16, 2, 4}]
		"""
		elementaries = [Factor.get_power(c) for c in exponentsof2]
		if real:
			elementaries = [{2**i for i in s} for s in elementaries]
		return elementaries 
		
	@staticmethod
	def get_exponentsof2(number: int) -> list:
		"""
		Give all the exponents of 2 needed to represent the number
		
		:param int number: number
		
		:return: all the exponents of 2 needed to represent the number
		:rtype: list(int)

		>>> Factor.get_exponentsof2(1024)
		[10]
		
		>>> Factor.get_exponentsof2(1023)
		[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
		"""
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
		"""
		Give the binary representation of the number
		
		:param int number: number
		
		:return: the binary representation of the number
		:rtype: list

		>>> Factor.get_int2list(1024)
		['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
		
		>>> Factor.get_int2list(1023)
		['1', '1', '1', '1', '1', '1', '1', '1', '1', '1']
		
		>>> Factor.get_int2list(242)
		['1', '1', '1', '1', '0', '0', '1', '0']
		"""
		return list(bin(number)[2:])

	@staticmethod
	def get_power(number: int) -> set:
		"""
		Give all the power of 2 needed to represent the number
		
		:param int number: number
		
		:return: all the power of 2 needed to represent the number
		:rtype: list(int)

		>>> Factor.get_power(1024)
		{1024}
		
		>>> Factor.get_power(1023)
		{32, 1, 2, 64, 4, 128, 256, 512, 8, 16}
		
		>>> Factor.get_power(242)
		{64, 32, 2, 128, 16}
		"""
		n = list(bin(number)[2:])
		n.reverse()
		p = {2**i for i,n in enumerate(n) if n =='1'}
		return p if p else {0}

	def _set_exponent(self, exponent: int, optimize: str) -> None:
		"""
		Set the exponent according to the chosen optimization
		
		:param int exponent: exponent of power
		:param str optimize: the optimization of factorization: None, 'soft' or 'hard'
		
			default: None
		
		:rtype: None

		>>> factor= Factor(298)
		>>> factor.exponent
		298
		
		>>> factor._set_exponent(298, 'soft')
		>>> factor.exponent
		320
		
		>>> factor._set_exponent(298, 'hard')
		>>> factor.exponent
		512
		"""
		def hard(exponent: int) -> int:
			"""
			Give the first superior exponent of exponent (entirely) 
			"""
			return int('1' + '0' * (exponent.bit_length()), 2)
		
		def soft(exponent: int, exponent2: int) -> int:
			"""
			Give the first exponent of exponent (the first highest founded from left to right)
			"""
			if exponent2[1:2] == '1':
				exponent = hard(exponent)
			else:
				index = exponent2.find('1', 1)
				exponent = exponent2[0:index-  1] + '1'  + '0'*(len(exponent2) - index)
				exponent = int('0b' + exponent, 2)
			return exponent
				
		if exponent and optimize and exponent.bit_length() > 1:
			exponent2 = bin(exponent)[2:]
			if exponent2.count('1') > 1:
				if optimize == 'hard':
					exponent = hard(exponent)
				elif optimize == 'soft':
					exponent = soft(exponent, exponent2)
			
		self.exponent = exponent

	# TODO: wrong string replace
	def str_factor(self) -> str:
		string = str(self.factorization)
		d = {	': ': '*', ',': ' *', '[': '(', 	']': ')', '{': '', '}': ''}
		for s, r in d.items():
			string = string.replace(s, r)
		indexes = list(set.union(*self.elementaries))
		indexes.sort(reverse=True)
		for index in indexes:
			string = string.replace(str(index), str(2**index))
		return string.strip('()')
		

		