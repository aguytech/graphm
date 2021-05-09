'''
Created on Apr 26, 2021

@author: salem Aguemoun
'''
import functools
import graphm.matrixboolean

class Matrix(graphm.matrixboolean.MatrixBoolean):
	""" Manage a arithmetic matrix
	
	.. CAUTION:: Instance variables
	
	:var list matrix: matrix with real numbers
	:var int dimM: number of rows
	:var int dimN: number of columns
	"""

	def __init__(self, **d) -> 'Matrix':
		"""Set the matrix properties with type given by one option in:
		
		:matrix: get a matrix
		:empty: get 2 dimensions of an empty matrix
		:random: get 2 dimensions of randomized matrix
		:unity: get the dimension of unity matrix

		:param dict \*\*d: options to specify the type of matrix
		
			:matrix: (list) matrix in [[int,...], ...] or ((int,...), ...)
			:empty: dimensions for matrix (dimM: int, dimN: (tuple) int)
			:random: dimensions for matrix (dimM: int, dimN: (tuple) int)
			:unity: (int) dimensions for square matrix
			
		:return: the matrix
		:rtype: Matrix
		"""
		super().__init__(**d)
		
	def __add__(self, matrix: 'Matrix') -> 'Matrix':
		""" Return the result of the sum of this instance and that given in argument
		
		:param Matrix matrix: matrix to be added to the instance
		:return: the result of the sum of this instance and that given in argument
		:rtype: Matrix
		
		>>> m = Matrix(matrix=[[0,10,4,2], [1,3,5,7]])
		>>> m2 = Matrix(matrix=[[4,5,8,2], [10,5,7,4]])
		>>> print(m + m2)
		dim 2,4
		4,15,12,4
		11,8,12,11
		"""
		# wrong dimensions
		if matrix.dimM != self.dimM or matrix.dimN != self.dimN:
			raise ValueError("Matrix have wrong dimensions")
		
		r = Matrix(empty=(self.dimM, self.dimN))
		for m in range(self.dimM):
			for n in range(self.dimN):
				r.matrix[m][n] = self.get_value(m, n) + matrix.get_value(m, n)
		return r 
			
	def __mul__(self, matrix: 'Matrix') -> 'Matrix':
		""" Return the matrix multiplication with a logical '&'
		between instance and that passed in argument
		
		:param Matrix matrix: matrix to be added to the instance
		:return: the result of the multiplication of this instance and that given in argument
		:rtype: Matrix

		>>> m = Matrix(matrix=[[0,10,4,2], [1,3,5,7], [2,-1,5,3]])
		>>> m2 = Matrix(matrix=[[4,2], [1,2], [2,3], [1,1]])
		>>> print(m * m2)
		dim 3,2
		20,34
		24,30
		20,20
		"""
		# wrong dimensions
		if matrix.dimM != self.dimN:
			raise ValueError("Matrix have wrong dimensions")
		
		r = Matrix(empty=(self.dimM, matrix.dimN))
		for m in range(self.dimM):
			for n in range(matrix.dimN):
				l = (self.get_value(m, i) * matrix.get_value(i, n) for i in range(self.dimN))
				# with functools package
				r.matrix[m][n] = functools.reduce(lambda x, y: x + y, l)
				#r.matrix[n][m] = 1 if sum(l) > 0 else 0
				#r.matrix[n][m] = sum(self.matrix[n][i] * matrix.matrix[i][m] for i in range(self.dimN))
		return r

	def __repr__(self) -> str:
		""" Return a linear representation of matrix
		
		:return: a linear representation of the matrix separated by comma
		
		>>> m = Matrix(matrix=['00001', '00100', '00010'])
		>>> repr(m)
		'0,0,0,0,1  0,0,1,0,0  0,0,0,1,0'
		"""
		return  "  ".join(",".join(str(n) for n in m) for m in self.matrix)

	def __str__(self) -> str:
		""" Return dimensions of matrix and matrix in 2 dimensions
		
		:return: a 2 dimensions representation of the matrix
		
		>>> m = Matrix(matrix=['00001', '00100', '00010'])
		>>> print(m)
		dim 3,5
		0,0,0,0,1
		0,0,1,0,0
		0,0,0,1,0
		"""
		return  f"dim {self.dimM},{self.dimN}" +"\n" \
			+ "\n".join(",".join(str(n) for n in m) for m in self.matrix)
	
	def __sub__(self, matrix: 'Matrix') -> 'Matrix':
		""" Return the result of the substraction of this instance and that given in argument
		
		:param Matrix matrix: matrix to be added to the instance
		:return: the result of the sum of this instance and that given in argument
		:rtype: Matrix
		
		>>> m = Matrix(matrix=[[0,10,4,2], [1,3,5,7]])
		>>> m2 = Matrix(matrix=[[4,5,8,2], [10,5,7,4]])
		>>> print(m - m2)
		dim 2,4
		-4,5,-4,0
		-9,-2,-2,3
		"""
		# wrong dimensions
		if matrix.dimM != self.dimM or matrix.dimN != self.dimN:
			raise ValueError("Matrix have wrong dimensions")
		
		r = Matrix(empty=(self.dimM, self.dimN))
		for m in range(self.dimM):
			for n in range(self.dimN):
				r.matrix[m][n] = self.get_value(m, n) - matrix.get_value(m, n)
		return r 
			
		
