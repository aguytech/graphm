'''
Created on Apr 26, 2021

@author: salem Aguemoun
'''
import functools
import random as rnd
import graphm.amatrix

class MatrixBoolean(graphm.amatrix.AMatrix):
	""" Manage a boolean matrix
	
	.. NOTE:: For inherited class variables see :class:`graphm.amatrix.AMatrix`
	
	.. CAUTION:: Instance variables
	
	:var list matrix: matrix with integers 0/1
	"""

	def __init__(self, **d) -> 'MatrixBoolean':
		"""Set the matrix properties with type given by one option in:
		
		* **matrix** get a boolean matrix
		* **empty** get 2 dimensions of an empty matrix
		* **random** get 2 dimensions of randomized matrix
		* **unit** get the dimension of unit matrix

		:param dict \*\*d: options to specify the type of matrix
		
			:empty: (tuple) dimensions for matrix (dimM: int, dimN: int)
			:matrix: (list) matrix in [str, ...] or [[int,...], ...] or (str, ...) or ((int,...), ...)
			:random: (tuple) dimensions for matrix (dimM: int, dimN: int)
			:unit: (int) dimensions for square matrix
			
		For default options see :class:`AMatrix.__init__`
			
		:return: the matrix
		:rtype: MatrixBoolean
		"""
		super().__init__(**d)
		
	def __add__(self, matrix: 'MatrixBoolean') -> 'MatrixBoolean':
		""" Return the result of the sum of this instance and that given in argument
		
		:param MatrixBoolean matrix: matrix to be added to the instance
		:return: the result of the sum of this instance and that given in argument
		:rtype: MatrixBoolean
		
		>>> m = MatrixBoolean(matrix=['00001', '00100', '00010'])
		>>> m2 = MatrixBoolean(matrix=['00001', '00000', '10011'])
		>>> m + m2
		00001,00100,10011
		"""
		if not isinstance(matrix, MatrixBoolean):
			raise ValueError("argument must be an instance of class 'MatrixBoolean")
		if matrix.dimM != self.dimM or matrix.dimN != self.dimN:
			raise ValueError("Matrix have wrong dimensions")
		
		r = MatrixBoolean(empty=(self.dimM, self.dimN))
		for m in range(self.dimM):
			for n in range(self.dimN):
				r.matrix[m][n] = self.get_value(m, n) | matrix.get_value(m, n)
		return r 
		
	def __eq__(self, matrix: 'MatrixBoolean') -> bool:
		""" Return equality between itself and argument 
		
		:param MatrixBoolean matrix: matrix to be added to the instance
		:return: True if this instance equals to that given
		:rtype: bool
		
		>>> m = MatrixBoolean(matrix=['00001', '00100', '00010'])
		>>> m2 = MatrixBoolean(matrix=['00001', '00100', '00010'])
		>>> m == m2
		True
		"""
		if not isinstance(matrix, MatrixBoolean) or \
			self.dimM != matrix.dimM or self.dimN != matrix.dimN or self.matrix != matrix.matrix:
			return False
		return True
	
	def __mul__(self, matrix: 'MatrixBoolean') -> 'MatrixBoolean':
		""" Return the matrix multiplication with a logical '&'
		between instance and that passed in argument
		
		:param MatrixBoolean matrix: matrix to be added to the instance
		:return: the result of the multiplication of this instance and that given in argument
		:rtype: MatrixBoolean

		>>> m = MatrixBoolean(matrix=['00001', '00100'])
		>>> m2 = MatrixBoolean(matrix=['001', '000', '111', '101', '100'])
		>>> m * m2
		100,111
		"""
		# wrong dimensions
		if matrix.dimM != self.dimN:
			raise ValueError("Matrix have wrong dimensions")
		
		r = MatrixBoolean(empty=(self.dimM, matrix.dimN))
		for m in range(self.dimM):
			for n in range(matrix.dimN):
				l = (self.get_value(m, i) & matrix.get_value(i, n) for i in range(self.dimN))
				# with functools package
				r.matrix[m][n] = functools.reduce(lambda x, y: x | y, l)
				#r.matrix[n][m] = 1 if sum(l) > 0 else 0
				#r.matrix[n][m] = sum(self.matrix[n][i] * matrix.matrix[i][m] for i in range(self.self.dimN))
		return r

	def __repr__(self) -> str:
		""" Return a linear representation of matrix
		
		:return: a linear representation of the matrix separated by comma
		
		>>> m = MatrixBoolean(matrix=['00001', '00100', '00010'])
		>>> repr(m)
		'00001,00100,00010'
		"""
		return  ",".join("".join(str(n) for n in m) for m in self.matrix)

	def __str__(self) -> str:
		""" Return dimensions of matrix and matrix in 2 dimensions
		
		:return: a 2 dimensions representation of the matrix
		
		>>> m = MatrixBoolean(matrix=['00001', '00100', '00010'])
		>>> print(m)
		dim 3,5
		00001
		00100
		00010
		"""
		return  f"dim {self.dimM},{self.dimN}" +"\n" \
			+ "\n".join("".join(str(n) for n in m) for m in self.matrix)
	
	def copy(self) -> 'MatrixBoolean':
		""" Return a copy of matrix
		
		:return: copy of matrix
		:rtype: MatrixBoolean
		
		>>> m = MatrixBoolean(matrix=['001', '000', '111', '101', '100'])
		>>> m.copy()
		001,000,111,101,100
		"""
		return MatrixBoolean(matrix=self.matrix)
		
	def get_value(self, m: int, n: int) -> int:
		""" Return value of the cell at position m, n
		
		:param int m: row of value
		:param int n: column of value
		:param int value: value of cell
		
		>>> m = MatrixBoolean(matrix=['00001', '00100', '00010'])
		>>> print(m.get_value(0, 0))
		0
		>>> print(m.get_value(1, 2))
		1
		"""
		return self.matrix[m][n]
	
	def set_from_empty(self, empty: int) -> None:
		""" Set an empty matrix containing only 0
		
		:param tuple empty: containing 2 dimensions of matrix: (rows, columns)
		
			:dimM: (int) number of rows
			:dimN: (int) number of columns
		
		>>> m = MatrixBoolean(empty=(4,8))
		>>> m
		00000000,00000000,00000000,00000000
		"""
		dimM, dimN = empty
		self._set_dim(dimM, dimN)
		self.matrix = [[0 for _ in range(dimN) ] for _ in range(dimM)]

	def set_from_matrix(self, matrix: list) -> None:
		""" Set content of the matrix  from the given matrix 
		get a boolean matrix containing list of string or list of list of integers
		
		:param (list) matrix: matrix in formats [str, ...] or [[int,...], ...] or (str, ...) or ((int,...), ...) 
		
		>>> m = MatrixBoolean(matrix=['00001', '00100', '00010'])
		>>> m
		00001,00100,00010
		"""
		lenLine = len(matrix[0]) if matrix else 0
		self._set_dim(len(matrix), lenLine)
		
		self.matrix = []
		for line in matrix:
			# wrong length for line 
			if len(line) != lenLine:
				raise ValueError(f"Wrong length for {line}")
			# string to list for matrix line
			if isinstance(line, str):
				line = [int(i) for i in line]
			self.matrix.append(line)

	def set_from_random(self, random: tuple, level: int=200) -> None:
		""" Set a matrix containing random booleans in integer representation
		
		the level represents the quantity of 0 compared to 1 (0-10)
		Reflexivity is the possibility for one node to go to itself
		
		:param tuple random: containing 2 dimensions of matrix: (rows, columns)
		
			:dimM: (int) number of rows
			:dimN: (int) number of columns
		
		:param int level=0: (0-10), quantity of 0 compared to 1
		:param bool reflexive: if True allow reflexive nodes, default is False
		
		>>> m = MatrixBoolean(random=(4,8))
		>>> (m.dimM,m.dimN)
		(4, 8)
		"""
		dimM, dimN = random
		self._set_dim(dimM, dimN)
		
		level_max = 1000
		self.matrix = [[1 if rnd.randrange(level_max) < level else 0 for _ in range(dimN)] for _ in range(dimM)]
		# reflexivity
		if self.isreflexive:
			self.matrix = [[self.matrix[m][n] if m != n else 1 for n in range(dimN)] for m in range(dimM)]
		
	def set_from_unit(self, unit: int) -> None:
		""" Set an unit matrix: an empty square matrix with diagonal to 1

		:param int unit: number of rows and columns
		
		>>> m = MatrixBoolean(unit=4)
		>>> print(m)
		dim 4,4
		1000
		0100
		0010
		0001
		"""
		dim = unit
		self._set_dim(dim, dim)
		self.matrix = [[0 if i != j else 1 for i in range(dim) ] for j in range(dim)]
	
	def set_value(self, m: int, n: int, value: int) -> None:
		""" set value of the element at position m, n
		
		:param int m: value of row
		:param int n: value of column
		:param int value: value of cell
		
		>>> m = MatrixBoolean(matrix=['00001', '00100', '00010'])
		>>> m.set_value(0, 0, 1)
		>>> print(m)
		dim 3,5
		10001
		00100
		00010
		"""
		self.matrix[m][n] = value
	
	def transposed(self) -> 'MatrixBoolean':
		""" Return the transpose of this matrix
		Give the diagonal symmetry of matrix
		
		:return: the transpose of this matrix
		:rtype: MatrixBinary

		>>> m = MatrixBoolean(matrix=[[0, 0, 0, 0, 1], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0]])
		>>> m2 = m.transposed()
		>>> m2
		000,000,010,001,100
		"""
		matrix = MatrixBoolean(empty=(self.dimN, self.dimM))
		for m in range(self.dimM):
			for n in range(self.dimN):
				matrix.matrix[n][m] = self.matrix[m][n]
		return matrix
