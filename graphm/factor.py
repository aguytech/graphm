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
		facto, count = Factor.factor(elementaries)
		print('gag')
		
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
	def get_calculate(factors: iter, foo: callable):
		if not callable(foo):
			raise ValueError("You need to give a callable function")
		
		
	@staticmethod
	def factor(elementaries: iter):
		def factorec(indexes: iter, fact: list, count: int):
			if not indexes or not fact:
				return (fact, count)
			
			index = indexes.pop()
			index_s = {index}
			
			count += 1
			for item in range(len(indexes)):
				pass
			
			content_index = [fact[i] for i in range(len(fact)) if index in fact[i]]
			content_not_index = [fact[i] for i in range(len(fact)) if index not in fact[i]]
			content_index = [v.difference(index_s) if v.difference(index_s) else {0} for v in content_index]
			fact.clear()
			
			count_keep = count
			if len(content_index) > 1:
				content_index, count_i = factorec(indexes[:], content_index, count)
				count = count_i
			if len(content_not_index) > 1:
				content_not_index, count_ni = factorec(indexes[:], content_not_index, count)
				count = count + (count_ni - count_keep)
			
			if content_index:
				fact.append({index: content_index})
			if content_not_index:
				fact.append(content_not_index)
			
			return (fact, count)
			
		indexes = list(set.union(*elementaries))
		indexes.sort(reverse=True)
		count = 0
		fact = [i.copy() for i in elementaries]
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
		
		
		
		
		
		
			
		