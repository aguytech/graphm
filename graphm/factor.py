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
		self.result= None
		coefficients = Factor.get_coefficients(number)
		elementaries = Factor.get_elementaries(coefficients)
		self.fact, self.count = Factor.factor(elementaries)
	
	def __repr__(self):
		return f"number: {self.number}\nfacto: {self.facto}\ncount: {self.count}\nresult: {self.result}"
	
	def __str__(self):
		def str_rec(fact):
			for d in fact:
				index, content = d.popitem()
				content = str_rec(content)
				p = f"{index}*( {content} ) + "
		
		l = [{8: [{1: [{0: [{0}]}]}, {0: [{0}]}]}, {4: [{2: [{1: [{0: [{0}]}]}, {0: [{0}]}]}, {1: [{0: [{0}]}]}, {0: [{0}]}]}, {2: [{1: [{0: [{0}]}]}, {0: [{0}]}]}, {1: [{0: [{0}]}]}, {0: [{0}]}]
		fact = deepcopy(self.fact)
		p = str_rec(self.fact)
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
	def get_power(number: int) -> set:
		n = list(bin(number)[2:])
		n.reverse()
		p = {2**i for i,n in enumerate(n) if n =='1'}
		return p if p else {0}

	@staticmethod
	def get_elementaries(coefficients: iter):
		return [Factor.get_power(c) for c in coefficients]
		
	@staticmethod
	def get_calculate(factors: iter, obj: object):
		if not hasattr(obj, '__add__'):
			raise ValueError("The given object has no method for addition")
		if not hasattr(obj, '__mul__'):
			raise ValueError("The given object has no method for multiplication")
		
		
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
			
"""			
			deep += 1
			index = indexes.pop()
			index_s = {index}
			content = [fact[i] for i in range(len(fact)) if index in fact[i] and not isinstance(fact[i], dict)]
			[fact.remove(v) for v in content if not isinstance(content, dict)]
			content = [v.difference(index_s) if v.difference(index_s) else {0} for v in content]
			
			fact_d = factorec(indexes, fact, deep)
			fact.append({index: content})
			
			factorec(indexes, fact, deep)




			found = [fact[i] for i in range(len(fact)) if index in fact[i]]
			not_found = [fact[i] for i in range(len(fact)) if index not in fact[i]]
			found = [i if i else {0} for i in found]
			fact.append({index: found})
"""		
		
		
		
		
		
		
			
		