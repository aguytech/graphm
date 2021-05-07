'''
Created on Apr 26, 2021

@author: salem Aguemoun
'''
import random as rnd
import graphm.factor
Factor = graphm.factor.Factor

class MatrixBinary(graphm.amatrix.AMatrix):
	""" Manage a boolean matrix with binary lines
	
	Increase performance of boolean matrices
	with usage of integers (binary) for representation of list of booleans
	for lines and columns
	
	.. NOTE:: For inherited class variables see :class:`graphm.amatrix.AMatrix`
	
	.. CAUTION:: Instance variables
	
	:var list matrixM: contents binary integers for rows
	:var list matrixN: contents binary integers for columns
	"""

	def __init__(self, **d) -> 'MatrixBinary':
		""" Set the matrix properties with type given by one in:
		
		* **matrix** get a binary matrixM and dimN
		* **boolean** get a boolean matrix
		* **empty** get 2 dimensions of an empty matrix
		* **random** get 2 dimensions of randomized matrix
		* **unit** get the dimension of unit matrix

		:param dict \*\*d: options to specify the type of matrix
		
			with following indexes:
			
			:matrix: (tuple) matrixM in [int, ...] and dimN: int
			:boolean: (list) matrix in [str, ...] or [[int,...], ...] or (str, ...) or ((int,...), ...)
			:empty: (tuple) dimensions for matrix (dimM: int, dimN: int)
			:random: (tuple) dimensions for matrix (dimM: int, dimN: int)
			:unit: (int) dimensions for square matrix
			
		For default options see :class:`AMatrix.__init__`
			
		:return: the matrix
		:rtype: MatrixBinary
		"""
		super().__init__(**d)
	
	def __add__(self, matrix: object) -> 'MatrixBinary':
		""" Return the result of a logical '|'  between values of instance and that passed in argument
		
		:param MatrixBinary matrix: matrix to be added to the instance
		:return: the result of the sum of this instance and that given in argument
		:rtype: MatrixBinary
		
		>>> m = MatrixBinary(boolean=['00001', '00100', '00010'])
		>>> m2 = MatrixBinary(boolean=['00001', '00000', '10011'])
		>>> m + m2
		00001,00100,10011
		 """
		if not isinstance(matrix, MatrixBinary):
			raise TypeError(f"Unsupported type of argument :{type(matrix)} for addition'")
		if matrix.dimM != self.dimM or matrix.dimN != self.dimN:
			raise ValueError("Wrong dimensions between matrices")

		matrixM = [self.matrixM[m] | matrix.matrixM[m] for m in range(self.dimM)]
		return MatrixBinary(matrix=(matrixM, self.dimN))
	
	def __eq__(self, matrix: 'MatrixBinary') -> bool:
		""" Return equality between itself and argument 
		
		:param MatrixBinary matrix: matrix to be added to the instance
		:return: True if this instance equals to that given
		:rtype: bool
		
		>>> m = MatrixBinary(boolean=['00001', '00100', '00010'])
		>>> m2 = MatrixBinary(boolean=['00001', '00100', '00010'])
		>>> m == m2
		True
		"""
		if not isinstance(matrix, MatrixBinary):
			return False

		return self.dimM == matrix.dimM and self.matrixM == matrix.matrixM
	
	def __mul__(self, matrix: 'MatrixBinary') -> 'MatrixBinary':
		""" Return the matrix multiplication with a logical '&'
		between instance and that passed in argument
		
		:param MatrixBinary matrix: matrix to be added to the instance
		:return: the result of the multiplication of this instance and that given in argument
		:rtype: MatrixBinary

		>>> m = MatrixBinary(boolean=['00001', '00100'])
		>>> m2 = MatrixBinary(boolean=['001', '000', '111', '101', '100'])
		>>> m * m2
		100,111
		 """
		if not isinstance(matrix, MatrixBinary):
			raise TypeError(f"Unsupported type of argument :{type(matrix)} for addition'")
		if matrix.dimM != self.dimN:
			raise ValueError("Matrix must to be square, dimM equals to dimN")
		
		matrixM = [0]*self.dimM
		for m in range(self.dimM):
			line = [('0' if (self.matrixM[m] & matrix.matrixN[n]) == 0 else '1') for n in range(matrix.dimN)]
			matrixM[m] = int('0b' + ''.join(line), 2)
		return MatrixBinary(matrix=(matrixM, matrix.dimN))

	def __repr__(self) -> str:
		""" Return a linear representation of the matrix in boolean view
		
		Each rows of matrix are separated by a comma

		:return: a linear representation of the matrix separated by comma
		
		>>> m = MatrixBinary(boolean=['00001', '00100', '00010'])
		>>> m.__repr__()
		'00001,00100,00010'
		"""
		return ",".join(MatrixBinary.get_int2str(m, self.dimN) for m in self.matrixM)

	def __str__(self) -> str:
		""" Return dimensions of matrix and matrix in 2 dimensions in boolean view
		
		Each rows of matrix are on a separated line
		
		:return: a 2 dimensions representation of the matrix
		:rtype: str
		
		>>> m = MatrixBinary(boolean=['00001', '00100', '00010'])
		>>> print(m)
		dim 3,5
		00001
		00100
		00010
		"""
		return f"dim {self.dimM},{self.dimN}" +"\n" \
			+ "\n".join(MatrixBinary.get_int2str(m, self.dimN) for m in self.matrixM)

	@staticmethod
	def add_unit(matrix : 'MatrixBinary') -> 'MatrixBinary':
		""" Return matrix added of unit matrix
		:param MatrixBinary matrix: 
		
		:return: matrix added of unit matrix
		:rtype: MatrixBinary
		"""
		unit = [2**i for i in range(matrix.dimM-1, -1, -1)]
		matrix.matrixM = [matrix.matrixM[i] | unit[i] for i in range(matrix.dimM)]
		matrix.matrixN = [matrix.matrixN[i] | unit[i] for i in range(matrix.dimN)]
		return matrix

	def copy(self) -> 'MatrixBinary':
		""" Return a copy of matrix
		
		:return: copy of matrix
		:rtype: MatrixBinary
		
		>>> m = MatrixBinary(boolean=['001', '000', '111', '101', '100'])
		>>> m.copy()
		001,000,111,101,100
		"""
		return MatrixBinary(matrix=([i for i in self.matrixM],self.dimN))
		
	def export2list(self) -> list:
		""" Return the matrix content in a list
		
		:return: list of integers 0/1 in 2 dimensions of matrix contents
		:rtype: list

		>>> m = MatrixBinary(boolean=['00001', '00100', '00010'])
		>>> m.export2list()
		[[0, 0, 0, 0, 1], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0]]
		"""
		return [[int(i) for i in MatrixBinary.get_int2str(line, self.dimN)] for line in self.matrixM]
	
	@staticmethod
	def get_M2N(matrixM: 'MatrixBinary', dimN: int) -> list:
		""" Return the transpose of the matrixM (list of rows) given
		
		Convert rows of matrix to columns
		
		:param 'MatrixBinary' matrix: matrix content
		:param int dimN: dimension of matrixN, number of columns
		
		:return: the transpose of the matrix
		:rtype: list
		
		>>> MatrixBinary.get_M2N([1, 4, 2], 5)
		[0, 0, 2, 1, 4]
		"""
		line = [MatrixBinary.get_int2str(n, dimN) for n in matrixM]
		return [int('0b' + ''.join(l[n] for l in line), 2) for n in range(dimN)]
		#return [int('0b' + ''.join(l[n] for l in matrix), 2) for n in range(dim)]
	
	def get_closure_reflective_count(self, add=True, full=False) -> tuple:
		""" Return the transitive closure of itself in a new matrix
		using an internal optimized product
		
		If argument 'full' is False, the transitive closure stop when closure(d) = closure(d-1)
		
		:param bool add: if True adds unit matrix otherwise no
			
			default = True
			
		:param bool full: if True calculates all ranks, otherwise only until a stabilized closure
			
			default = False
		
		:return: The transitive closure with a deep of stabilized closure and deep
		:rtype: tuple(MatrixBinary, int)
		
		>>> m = MatrixBinary(boolean=['00001', '00100', '00010', '01010', '00010'])
		>>> closure, count = m.get_closure_reflective_count()
		>>> closure
		11111,01110,01110,01110,01111
		
		>>> m = MatrixBinary(boolean=['00001', '00100', '00010', '01010', '00010'])
		>>> closure = m.get_closure_reflective(add=False)
		>>> closure
		01110,01110,01110,01110,01110
		"""
		if self.dimM != self.dimN:
			raise ValueError("Matrix have wrong dimensions")
		
		if add:
			matrixM = MatrixBinary.get_unit_added(self.matrixM, self.dimM)
			matrixN = MatrixBinary.get_unit_added(self.matrixN, self.dimN)
		else:
			matrixM, matrixN = self.matrixM, self.matrixN
		matrixM_tmp = matrixM[:]

		deep = 1
		# loops on n-1
		for _ in range(1, self.dimM):
			# mul
			for m in range(self.dimM):
				matrixM[m] = int('0b' + ''.join([('0' if (matrixM[m] & matrixN[n]) == 0 else '1') for n in range(self.dimN)]), 2)
			if not full:
				if matrixM == matrixM_tmp:
					break
			matrixM_tmp = matrixM[:]
			deep += 1
		return (MatrixBinary(matrix=(matrixM, self.dimN)), deep)

	def get_closure_reflective(self, add=True, full=False) -> 'MatrixBinary':
		""" Return the transitive closure of itself in a new matrix
		using an internal optimized product
		
		If argument 'full' is False, the transitive closure stop when closure(d) = closure(d-1)
		
		:param bool add: if True adds unit matrix otherwise no
			
			default = True
			
		:param bool full: if True calculates all ranks, otherwise only until a stabilized closure
			
			default = False
		
		:return: The transitive closure with a deep of stabilized closure
		:rtype: MatrixBinary
		
		>>> m = MatrixBinary(boolean=['00001', '00100', '00010', '01010', '00010'])
		>>> m.get_closure_reflective()
		11111,01110,01110,01110,01111
		"""
		if self.dimM != self.dimN:
			raise ValueError("Matrix have wrong dimensions")
		
		if add:
			matrixM = MatrixBinary.get_unit_added(self.matrixM, self.dimM)
			matrixN = MatrixBinary.get_unit_added(self.matrixN, self.dimN)
		else:
			matrixM, matrixN = self.matrixM, self.matrixN
		matrixM_tmp = matrixM[:]
		
		# loops on n-1
		for _ in range(1, self.dimM):
			# mul
			for m in range(self.dimM):
				matrixM[m] = int('0b' + ''.join([('0' if (matrixM[m] & matrixN[n]) == 0 else '1') for n in range(self.dimN)]), 2)
			if not full:
				if matrixM == matrixM_tmp:
					break
			matrixM_tmp = matrixM[:]
		return MatrixBinary(matrix=(matrixM, self.dimN))

	def get_closure_reflective_optimized(self, optimize='soft', add=True) -> 'MatrixBinary':
		""" Return the transitive closure of itself in a new matrix
		using class :class:`Factor` to optimize products
		
		If argument 'full' is False, the transitive closure stop when closure(d) = closure(d-1)
		
		:return: The transitive closure with a deep of stabilized closure
		:rtype: MatrixBinary
		
		>>> m = MatrixBinary(boolean=['00001', '00100', '00010', '01010', '00010'])
		>>> closure, count = m.get_closure_reflective_optimized()
		>>> closure
		11111,01110,01110,01110,01111
		"""
		if self.dimM != self.dimN:
			raise ValueError("Matrix have wrong dimensions")
		
		if add:
			matrix = self.copy()
			matrix.matrixM = MatrixBinary.get_unit_added(self.matrixM, self.dimM)
			matrix.matrixN = MatrixBinary.get_unit_added(self.matrixN, self.dimN)
		else:
			matrix = self
		
		factor = Factor(self.dimM - 1, optimize=optimize)
		return factor.power(matrix)

	def get_closure_matrix(self, full=False) -> tuple:
		""" Return the transitive closure of itself and intermediate adjacency matrices
		using an internal optimized product
		
		If argument 'full' is False, the transitive closure stop when closure(d) = closure(d-1)
		
		:param bool full: if True calculates all ranks, otherwise only until a stabilized closure
			
			default = False
		
		:return: The transitive closure with intermediate adjacency matrices
		:rtype: tuple with list of MatrixBinary & closure in MatrixBinary
		
		>>> m = MatrixBinary(boolean=['00001', '00100', '00010', '01010', '00010'])
		>>> closure, matrices = m.get_closure_matrix()
		>>> closure
		01111,01110,01110,01110,01110
		
		>>> m = MatrixBinary(boolean=['10001', '01100', '00110', '01010', '00011'])
		>>> closure, matrices = m.get_closure_matrix()
		>>> closure
		11111,01110,01110,01110,01111
		"""
		if self.dimM != self.dimN:
			raise ValueError("Matrix have wrong dimensions")
		
		matrix = self.copy()
		matrices = [matrix]
		matrixM = matrix.matrixM
		closureM = matrix.matrixM[:]
		closureM_tmp = matrix.matrixM[:]
		
		# loops on n-1
		for i in range(1, self.dimM):
			# mul
			for m in range(self.dimM):
				matrixM[m] = int('0b' + ''.join([('0' if (matrices[i-1].matrixM[m] & self.matrixN[n]) == 0 else '1') for n in range(self.dimN)]), 2)
			matrices.append(MatrixBinary(matrix=(matrixM, self.dimN)))
			closureM = [closureM[m] | matrixM[m] for m in range(self.dimM)]
			if not full:
				if closureM == closureM_tmp:
					break
			closureM_tmp = closureM
						
		return (MatrixBinary(matrix=(closureM, self.dimN)), matrices)

	def get_closure_slides(self,  full=False) -> list:
		""" Return the transitive closure of itself and intermediate adjacency matrices matrixM
		using an internal optimized product
		
		If argument 'full' is False, the transitive closure stop when closure(d) = closure(d-1)
		
		:param bool full: if True calculates all ranks, otherwise only until a stabilized closure
			
			default = False
		
		:return: The transitive closure with intermediate adjacency matrices matrixM
		:rtype: tuple with list of matrixM & closure in MatrixBinary
		
		>>> m = MatrixBinary(boolean=['00001', '00100', '00010', '01010', '00010'])
		>>> slides, closure = m.get_closure_slides()
		>>> closure
		[[14, 14, 14, 14, 14], [2, 2, 10, 14, 10], [10, 10, 14, 14, 14], [14, 14, 14, 14, 14]]
		"""
		if self.dimM != self.dimN:
			raise ValueError("Matrix have wrong dimensions")
		
		matrix = self.copy()
		result = [matrix.matrixM]
		matrixM = matrix.matrixM
		closureM = matrix.matrixM[:]
		closureM_tmp = matrix.matrixM[:]
		
		# loops on n-1
		for i in range(1, self.dimM):
			# mul
			for m in range(self.dimM):
				#line = [('0' if (result[i-1][m] & self.matrixN[n]) == 0 else '1') for n in range(self.dimN)]
				#matrixM[m] = int('0b' + ''.join(line), 2)
				matrixM[m] = int('0b' + ''.join([('0' if (result[i-1][m] & self.matrixN[n]) == 0 else '1') for n in range(self.dimN)]), 2)
			
			closureM = [closureM[m] | matrixM[m] for m in range(self.dimM)]
			if not full:
				if closureM == closureM_tmp:
					break
			result.append(matrixM[:])
			closureM_tmp = closureM
						
		return (closureM, result)

	def get_connect(self) -> dict:
		""" Return information about the full connectivity of this matrix 
		
		:return: informations about connectivity in a dictionary with indexes:
		:rtype: dict
		
			with following indexes:
			
			:connect: (bool) True if matrix is connected
			:deep: (int) The minimal deep of this state
			:matrix: (:class:`MatrixBinary`) The first adjacency matrix of full connectivity
		
		>>> m = MatrixBinary(boolean=['0000', '0010', '1001', '0101'])
		>>> m.get_connect()
		{'connect': False, 'deep': 4, 'matrix': 1000,1111,1111,1111}
		
		>>> m = MatrixBinary(boolean=['0100', '0010', '1001', '0101'])
		>>> m.get_connect()
		{'connect': True, 'deep': 3, 'matrix': 1111,1111,1111,1111}
	"""
		# wrong dimensions
		if self.dimM != self.dimN:
			raise ValueError("Matrix have wrong dimensions")
		
		# get matrix + unit matrix
		unit = [2**i for i in range(self.dimM-1, -1, -1)]
		matrixM = [self.matrixM[i] | unit[i] for i in range(self.dimM)]
		matrixN = [self.matrixN[i] | unit[i] for i in range(self.dimN)]

		deep = 1
		maskInit = 2**self.dimM - 1
		
		# test
		connect = maskInit in matrixM
		
		# loops on n-2
		while connect == False and deep < self.dimM:
			deep += 1
			mask = maskInit
			# mul
			for m in range(self.dimM):
				#line = [('0' if (matrixM[m] & matrixN[n]) == 0 else '1') for n in range(self.dimN)]
				matrixM[m] = int('0b' + ''.join([('0' if (matrixM[m] & matrixN[n]) == 0 else '1') for n in range(self.dimN)]), 2)
				mask = mask & matrixM[m]
			
			if mask == maskInit:
				connect = True

		#result
		matrix = MatrixBinary(matrix=(matrixM, self.dimN))
		return {'connect': connect, 'deep': deep, 'matrix': matrix}

	#TODO
	def get_connect_nodes(self, inM: int, outM: int) -> dict:
		""" Return information about the connectivity between
		one starting and one ending nodes in this matrix 
		
		:param in inM: node number to start
		:param in outM: node number to end
		
		:return: informations about connectivity between 2 nodes
		:rtype: dict
		
		:connect: (bool) True if matrix is connected
		:deep: (int) The minimal deep of this state
		:matrix: (:class:`MatrixBinary`) The first adjacency matrix of full connectivity
		
		>>> m = MatrixBinary(boolean=['0000', '0010', '1001', '0101'])
		>>> m.get_connect_nodes(1,2)
		{'connect': True, 'deep': 1, 'matrix': 1000,0110,1011,0101}
	"""
		# wrong dimensions
		if self.dimM != self.dimN:
			raise ValueError("Matrix have wrong dimensions")
		
		deep = 1
		connect = False
		mask = 2**(self.dimN - outM)
		unit = [2**i for i in range(self.dimM-1, -1, -1)]
		matrixM = [self.matrixM[i] | unit[i] for i in range(self.dimM)]
		matrixN = [self.matrixN[i] | unit[i] for i in range(self.dimN)]
		
		#test
		if (matrixM[inM] & mask) == mask:
			connect = True

		# loops on n-2
		while connect == False and deep < self.dimM:
			deep += 1
			# mul
			for m in range(self.dimM):
				#line = [('0' if (matrixM[m] & matrixN[n]) == 0 else '1') for n in range(self.dimN)]
				matrixM[m] = int('0b' + ''.join(('0' if (matrixM[m] & matrixN[n]) == 0 else '1') for n in range(self.dimN)), 2)

			if (matrixM[inM] & mask) == mask:
				connect = True
			
		#result
		matrix = MatrixBinary(matrix=(matrixM, self.dimN))
		return {'connect': connect, 'deep': deep, 'matrix': matrix}

	@staticmethod
	def get_int2str(line: int, dim: int) -> str:
		""" Return the converted  boolean string from binary integer,
		string length is adjusted by to dim.
		
		dim is the dimension of line
		
		:param int line: line of boolean in integer representation
		:param int dim: number of nodes
		
		:return: boolean strings
		:rtype: str

		>>> MatrixBinary.get_int2str(36, 10)
		'0000100100'
		"""
		s = bin(line)[2:]
		return s.zfill(dim)

	@staticmethod
	def get_str2int(line: str) -> int:
		""" Return the converted binary integer from boolean str,
		
		:param str line: a string of boolean representing the row m of the matrix
		
		:return: integer representing the row m of the matrix
		:rtype: int

		>>> MatrixBinary.get_str2int('0000100100')
		36
		"""
		return int('0b' + line, 2)

	def get_transpose(self) -> 'MatrixBinary':
		""" Return the transpose of this matrix
		Give the diagonal symmetry of matrix
		
		:return: the transpose of this matrix
		:rtype: MatrixBinary

		>>> m = MatrixBinary(boolean=[[0, 0, 0, 0, 1], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0]])
		>>> m2 = m.get_transpose()
		>>> m2
		000,000,010,001,100
		"""
		matrix = MatrixBinary(empty=(self.dimN, self.dimM))
		matrix.matrixM = self.matrixN[:]
		matrix.matrixN = self.matrixM[:]
		return matrix
	
	def matrixM2N(self) -> None:
		""" set the transpose of the matrixM (list of rows) of itself
		
		Convert rows of this matrix to columns

		>>> m = MatrixBinary(boolean=['001', '000', '111', '101', '100'])
		>>> m.matrixN = []
		>>> m.matrixM2N()
		>>> m.matrixN
		[7, 4, 22]
		"""
		matrix = [MatrixBinary.get_int2str(m, self.dimN) for m in self.matrixM]
		self.matrixN = [int('0b' + ''.join(line[n] for line in matrix), 2) for n in range(self.dimN)]
	
	@staticmethod
	def get_unit_added(matrixX: list, dimX: int) -> list:
		""" Return respectively matrixX (M or N) added of unit matrix
		
		:param list matrixX: matrixM or matrixN
		:return: matrixX (M or N) added of unit matrix
		:rtype: list
		"""
		unit = [2**i for i in range(dimX - 1, -1, -1)]
		return [matrixX[i] | unit[i] for i in range(dimX)]

	def str(self):
		""" Return a representation on 2 dimensions of 2 matrices.
		the original one and its transposed
		
		:return: a 2 dimensions representation of the matrix and its transposed
		:rtype: str
		
		>>> m = MatrixBinary(boolean=['00001', '00100', '00010'])
		>>> m.str()
		'\\n00001\\n00100\\n00010\\n-------\\n000\\n000\\n010\\n001\\n100'
		"""
		return "\n" \
			+ "\n".join(MatrixBinary.get_int2str(m, self.dimN) for m in self.matrixM) \
			+ "\n-------\n" \
			+ "\n".join(MatrixBinary.get_int2str(n, self.dimM) for n in self.matrixN)
	
	def set_from_boolean(self, boolean: list) -> None:
		""" Set content of the matrix  from the boolean matrix given
		get a boolean matrix containing list of string or list of list of integers
		
		:param list/tuple matrix: matrix in formats [str, ...] or [[int,...], ...] or (str, ...) or ((int,...), ...)
		
		>>> m = MatrixBinary(boolean=['00001', '00100', '00010'])
		>>> m
		00001,00100,00010
		
		>>> m = MatrixBinary(boolean=[['0', '0', '0', '0', '1'], ['0', '0', '1', '0', '0'], ['0', '0', '0', '1', '0']])
		>>> m
		00001,00100,00010
		
		>>> m = MatrixBinary(boolean=[[0, 0, 0, 0, 1], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0]])
		>>> m
		00001,00100,00010
		"""
		matrix = boolean
		lenLine = len(matrix[0]) if matrix else 0
		self._set_dim(len(matrix), lenLine)
		
		matrixM = []
		for line in matrix:
			# transform list lines in str lines 
			if isinstance(line, list):
				line = ''.join(str(i) for i in line)
			if len(line) != lenLine:
				raise ValueError("Wrong length for {line}")
			matrixM.append(int('0b' + line, 2))
	
		self.matrixM = matrixM
		self.matrixM2N()
	
	def set_from_empty(self, empty: tuple) -> None:
		""" Set an empty matrix containing only 0
		
		:param tuple empty: containing 2 dimensions of matrix: (rows, columns)
		
			:dimM: (int) number of rows
			:dimN: (int) number of columns
		
		>>> m = MatrixBinary(empty=(4,8))
		>>> m
		00000000,00000000,00000000,00000000
		"""
		dimM, dimN = empty
		self._set_dim(dimM, dimN)
		self.matrixM = [0 for _ in range(dimM)]
		self.matrixN = [0 for _ in range(dimN)]
	
	def set_from_matrix(self, matrix) -> None:
		""" Set content of the matrix  from the matrixM given and dimN
		get a binary matrix contains a list of integers and with the number of columns
		
		:param tuple m: contains following indexes
		
			:matrixM: (list) rows with integers
			:dimN: (int) the number of columns
					
		>>> m = MatrixBinary(matrix=([1, 4, 2], 5))
		>>> m
		00001,00100,00010
		"""
		matrixM, self.dimN = matrix
		self.matrixM = matrixM
		# TODO: remove
		#self.matrixM = matrixM[:]
		self.dimM = len(self.matrixM)
		self.matrixM2N()
	
	def set_from_random(self, random: tuple, level: int=200) -> None:
		""" Set a matrix containing random booleans in integer representation
		
		the level represents the quantity of 0 compared to 1 (0-10)
		Reflexivity is the possibility for one node to go to itself
		
		:param int level: the filling level of the matrix: 1 - 1000
		:param tuple random: containing 2 dimensions of matrix: (rows, columns)
		
			:dimM: (int) number of rows
			:dimN: (int) number of columns
		
		:param int level=0: (0-10), quantity of 0 compared to 1
		
		>>> m = MatrixBinary(random=(4,8))
		>>> (m.dimM,m.dimN)
		(4, 8)
		"""
		dimM, dimN = random
		self._set_dim(dimM, dimN)
		
		level_max = 1000
		matrix = [['1' if rnd.randrange(level_max) < level else '0' for _ in range(dimN)] for _ in range(dimM)]
		# reflexivity
		if self.isreflexive:
			matrix = [[matrix[m][n] if m != n else '1' for n in range(dimN)] for m in range(dimM)]
		
		self.matrixM = [int('0b' + ''.join(line), 2) for line in matrix]
		self.matrixM2N()

	def set_from_unit(self, unit: int) -> None:
		""" Set an unit matrix: an empty square matrix with diagonal to 1

		:param int unit: number of rows and columns
		
		>>> m = MatrixBinary(unit=4)
		>>> print(m)
		dim 4,4
		1000
		0100
		0010
		0001
		"""
		#self.matrixM = [int('0b' + ''.join(('1' if i == j else '0') for i in range(dim)), 2) for j in range(dim)]
		#self.matrixN = [int('0b' + ''.join(('1' if i == j else '0') for i in range(dim)), 2) for j in range(dim)]

		dim = unit
		matrix = (2**i for i in range(dim - 1, -1, -1))
		self.matrixM = [i  for i in matrix]
		self.matrixN = [i  for i in matrix]
		self._set_dim(dim, dim)

	
