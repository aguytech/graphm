'''
Created on Apr 26, 2021

@author: nikita
'''

class Factor(object):
	'''
	classdocs
	'''

	def __init__(self, number: int):
		'''
		Constructor
		'''
		coefficients = Factor.get_coefficients(number)
		elementaries = Factor.get_elementaries(coefficients)
		facto = Factor.factor(elementaries)
		
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
	def get_power(number: int) -> set:
		p = list(bin(number)[2:])
		p.reverse()
		return {2**i for i,n in enumerate(p) if n =='1'}

	@staticmethod
	def get_elementaries(coefficients: iter):
		return [Factor.get_power(c) for c in coefficients]
		
	@staticmethod
	def factor(elementaries: iter):
		def factorec(elements: iter, elementaries, fact: list, deep: int):
			if elements:
				deep += 1
				element = elements.pop()
				indexes = [i for i in range(len(elementaries)) if element in elementaries[i]]
				set_e = {element}
				fact[element] = [elementaries[i].difference(set_e) for i in indexes]
				[elementaries.pop() for i in indexes]
				
				factorec(elements[:], elementaries, fact[element], deep)
				reduced = [i.difference(element) for i in elementaries]
				fact = {element: [i for i in reduced if i]}
				factorec(elements, fact[element], deep)
			
		elements = list(set.union(*elementaries))
		elements.sort()
		tmp = [i.copy() for i in elementaries]
		deep = 0
		fact = {}
		factorec(elements, tmp, fact, deep)
		return (fact, deep)
			
		
		
		
		
		
		
			
		