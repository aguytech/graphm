#from graphm.amatrix import AMatrix
import random
from graphm.amatrix import AMatrix

class MatrixBinary(AMatrix):
	""" Manage a boolean matrix with binary lines
	
	Increase performance of boolean matrices
	with usage of integers (binary) for representation of list of booleans
	for lines and columns
	
	.. CAUTION:: Instance variables
	
	:var int dimM: number of rows
	:var int dimN: number of columns
	:var list matrix: matrix with integers representation of lines
	:var list/tuple matrixM: contents binary integers for rows
	:var list/tuple matrixN: contents binary integers for columns
	"""

	def __init__(self, **d) -> 'MatrixBinary':
		""" Set the matrix properties with type given by one in:
		
		* **matrix** get a binary matrixM and dimN
		* **boolean** get a boolean matrix
		* **empty** get 2 dimensions of an empty matrix
		* **random** get 2 dimensions of randomized matrix
		* **unity** get the dimension of unity matrix

		:param dict \*\*d: options to specify the type of matrix
		
			with following indexes:
			
			:matrix: (tuple) matrixM in [int, ...] and dimN: int
			:boolean: (list) matrix in [str, ...] or [[int,...], ...] or (str, ...) or ((int,...), ...)
			:empty: (tuple) dimensions for matrix (dimM: int, dimN: int)
			:random: (tuple) dimensions for matrix (dimM: int, dimN: int)
			:unity: (int) dimensions for square matrix
			
		:return: the matrix
		:rtype: MatrixBinary
		"""
		if 'boolean' in d:
			self.set_matrix_boolean(d['boolean'])
		else:
			super().__init__(**d)
	
	def __add__(self, matrix: 'MatrixBinary') -> 'MatrixBinary':
		""" Return the result of a logical '|'  between values of instance and that passed in argument
		
		:param MatrixBinary matrix: matrix to be added to the instance
		:return: the result of the sum of this instance and that given in argument
		:rtype: MatrixBinary
		
		>>> m = MatrixBinary(boolean=['00001', '00100', '00010'])
		>>> m2 = MatrixBinary(boolean=['00001', '00000', '10011'])
		>>> m + m2
		00001,00100,10011
		 """
		# wrong dimensions
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
		# wrong dimensions
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
	
	def get_closure(self) -> 'MatrixBinary':
		""" Return the transitive closure of this matrix
		
		The transitive closure stop when closure(d) = closure(d-1)
		Deep of closure is defined by this equality
		
		:return: The transitive closure with a deep of stabilized closure
		:rtype: MatrixBinary
		
		>>> m = MatrixBinary(boolean=['00001', '00100', '00010', '01010', '00010'])
		>>> m.get_closure()
		11111,01110,01110,01110,01111
		"""
		# wrong dimensions
		if self.dimM != self.dimN:
			raise ValueError("Matrix have wrong dimensions")
		
		# get matrix + unity matrix
		unity = [2**i for i in range(self.dimM-1, -1, -1)]
		matrixM = [self.matrixM[i] | unity[i] for i in range(self.dimM)]
		matrixN = [self.matrixN[i] | unity[i] for i in range(self.dimN)]
		matrixM_tmp = matrixM[:]
		
		# loops on n-2
		for i in range(2, self.dimM):
			# mul
			for m in range(self.dimM):
				matrixM[m] = int('0b' + ''.join([('0' if (matrixM[m] & matrixN[n]) == 0 else '1') for n in range(self.dimN)]), 2)
			if matrixM == matrixM_tmp:
				break
			matrixM_tmp = matrixM[:]
		# result
		#return (MatrixBinary(matrix=(matrixM, self.dimN)), l)
		return MatrixBinary(matrix=(matrixM, self.dimN))

	def get_closure_full(self) -> 'MatrixBinary':
		""" Return the transitive closure of this matrix
		
		The transitive closure stop when deep  = dimension - 1
		deep = self.dim - 1
		
		.. NOTE:: This method is used for the benchmark
		
		:return: The transitive closure with a deep of stabilized closure
		:rtype: MatrixBinary
		
		>>> m = MatrixBinary(boolean=['00001', '00100', '00010', '01010', '00010'])
		>>> m.get_closure_full()
		11111,01110,01110,01110,01111
		"""
		# wrong dimensions
		if self.dimM != self.dimN:
			raise ValueError("Matrix have wrong dimensions")
		
		# get matrix + unity matrix
		unity = [2**i for i in range(self.dimM-1, -1, -1)]
		matrixM = [self.matrixM[i] | unity[i] for i in range(self.dimM)]
		matrixN = [self.matrixN[i] | unity[i] for i in range(self.dimN)]
		
		# loops on n-2
		for i in range(2, self.dimM):
			# mul
			for m in range(self.dimM):
				matrixM[m] = int('0b' + ''.join([('0' if (matrixM[m] & matrixN[n]) == 0 else '1') for n in range(self.dimN)]), 2)
		# result
		return MatrixBinary(matrix=(matrixM, self.dimN))

	def get_closure_matrix_full(self) -> list:
		""" Return the transitive closure of this matrix and intermediate adjacency matrices
		
		.. NOTE:: Deep of closure is equal to matrix dimension  - 1
		
		:return: closure of matrix itself and intermediate adjacency matrices
		:rtype: list
			
			:index: (int) deep: deep of closure
			:values: (:class:`MatrixBinary`) matrix: adjacency matrices
			
			* [0]: transitive closure
			* [..]: adjacency matrices of intermediate deeps. Slides contains :class:`MatrixBinary`
		
		>>> m = MatrixBinary(boolean=['0000', '0010', '1001', '0101'])
		>>> m.get_closure_matrix_full()
		[0000,0010,1001,0101, 0000,1001,0101,0111, 0000,0101,0111,1111]
		"""
		# wrong dimensions
		if self.dimM != self.dimN:
			raise ValueError("Matrix have wrong dimensions")
		
		m = MatrixBinary(matrix=(self.matrixM, self.dimN))
		l = [m]
		matrixM = list(m.matrixM)

		# loops on n-2
		for i in range(2, self.dimM):
			# mul
			for m in range(self.dimM):
				matrixM[m] = int('0b' + ''.join([('0' if (l[i-2].matrixM[m] & self.matrixN[n]) == 0 else '1') for n in range(self.dimN)]), 2)
			l.append(MatrixBinary(matrix=(matrixM, self.dimN)))
		
		# result
		return l

	def get_closure_matrix_dict(self) -> dict:
		""" Return the transitive closure of this matrix and intermediate adjacency matrices
		
		Deep of closure is defined by equality of matrice(d) = matrice(d-1)
		
		:return: closure of matrix itself and intermediate adjacency matrices
		:rtype: dict
		
			:index: (int) deep: deep
			:values: (:class:`MatrixBinary`) matrix: adjacency matrices 
		
			* [0]: transitive closure
			* [..]: adjacency matrices of intermediate deeps. Slides contains :class:`MatrixBinary`
		
		>>> m = MatrixBinary(boolean=['0000', '0010', '1001', '0101'])
		>>> m.get_closure_matrix_dict()
		{1: 0000,0010,1001,0101, 2: 0000,1001,0101,0111, 3: 0000,0101,0111,1111}
		"""
		# wrong dimensions
		if self.dimM != self.dimN:
			raise ValueError("Matrix have wrong dimensions")
		
		d = {1: MatrixBinary(matrix=(self.matrixM, self.dimN))}
		matrixM = list(d[1].matrixM)

		# loops on n-2
		for i in range(2, self.dimM):
			# mul
			for m in range(self.dimM):
				matrixM[m] = int('0b' + ''.join([('0' if (d[i-1].matrixM[m] & self.matrixN[n]) == 0 else '1') for n in range(self.dimN)]), 2)
			d[i] = MatrixBinary(matrix=(matrixM, self.dimN))
		
		# result
		return d

	def get_closure_slides(self) -> list:
		""" Return the transitive closure of this matrix with intermediate adjacency matricesM
		
		Deep of closure is defined by equality of matrice(d) = matrice(d-1)
		
		:return: closure of matrix itself and intermediate adjacency matrices
		:rtype: list
		
			:index: (int) deep: deep
			:values: (list) matrixM: adjacency matrices with only rows
		
			* [0]: transitive closure
			* [..]: adjacency matrices of intermediate deeps. Slides contains rows with only matrixM
		
		>>> m = MatrixBinary(boolean=['0000', '0010', '1001', '0101'])
		>>> m.get_closure_slides()
		[[0, 15, 15, 15], [0, 2, 9, 5], [0, 9, 5, 7], [0, 5, 7, 15]]
		"""
		# wrong dimensions
		if self.dimM != self.dimN:
			raise ValueError("Matrix have wrong dimensions")
		
		matrixM = list(self.matrixM)
		closure = matrixM[:]
		closure_tmp = matrixM[:]
		l=[[], matrixM[:]]

		# loops on n-2
		for i in range(2, self.dimM):
			# mul
			for m in range(self.dimM):
				line = [('0' if (l[i-1][m] & self.matrixN[n]) == 0 else '1') for n in range(self.dimN)]
				matrixM[m] = int('0b' + ''.join(line), 2)

			closure = [closure[m] | matrixM[m] for m in range(self.dimM)]
			if closure != closure_tmp:
				closure_tmp = closure[:]
				l.append(matrixM[:])
			else:
				break

		l[0] = closure
		# result
		return (l)

	def get_closure_slides_dict(self) -> dict:
		""" Return the transitive closure of this matrix and intermediate adjacency matricesM
		
		Deep of closure is defined by equality of matrice(d) = matrice(d-1)
		
		:return: closure of matrix itself and intermediate adjacency matrices
		:rtype: dict
		
			:index: (int) deep: deep
			:values: (list) matrixM: adjacency matrices with only rows
		
			* [0]: transitive closure
			* [..]: adjacency matrices of intermediate deeps. Slides contains rows with only matrixM
		
		>>> m = MatrixBinary(boolean=['0000', '0010', '1001', '0101'])
		>>> m.get_closure_slides()
		[[0, 15, 15, 15], [0, 2, 9, 5], [0, 9, 5, 7], [0, 5, 7, 15]]
		"""
		# wrong dimensions
		if self.dimM != self.dimN:
			raise ValueError("Matrix have wrong dimensions")
		
		d = {1: self.matrixM[:]}
		matrixM = list(self.matrixM)

		# loops on n-2
		for i in range(2, self.dimM):
			# mul
			for m in range(self.dimM):
				matrixM[m] = int('0b' + ''.join([('0' if (d[i-1][m] & self.matrixN[n]) == 0 else '1') for n in range(self.dimN)]), 2)
			
			if matrixM != d[i-1]:
				d[i] = matrixM[:]
			else:
				break
		
		# result
		return d

	def get_closure_slides_full(self) -> list:
		""" Return the transitive closure of this matrix and intermediate adjacency matricesM
			* first elements: transitive closure
			* other elements: adjacency matrices of intermediate deeps. Slides contains rows with only matrixM
		
		.. NOTE:: Deep of closure is equal to matrix dimension  - 1
		
		:return: closure of matrix itself and intermediate adjacency matrices
		:rtype: dict
		
			:index: (int) deep: deep
			:values: (list) matrixM: adjacency matrices with only rows
		
		>>> m = MatrixBinary(boolean=['0000', '0010', '1001', '0101'])
		>>> m.get_closure_slides_full()
		[[0, 15, 15, 15], [0, 2, 9, 5], [0, 9, 5, 7], [0, 5, 7, 15]]
		"""
		# wrong dimensions
		if self.dimM != self.dimN:
			raise ValueError("Matrix have wrong dimensions")
		
		matrixM = list(self.matrixM)
		closure = matrixM[:]
		l=[[], matrixM[:]]

		# loops on n-2
		for i in range(2, self.dimM):
			# mul
			for m in range(self.dimM):
				line = [('0' if (l[i-1][m] & self.matrixN[n]) == 0 else '1') for n in range(self.dimN)]
				matrixM[m] = int('0b' + ''.join(line), 2)

			closure = [closure[m] | matrixM[m] for m in range(self.dimM)]
			l.append(matrixM[:])

		l[0] = closure
		# result
		return (l)

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
		
		# get matrix + unity matrix
		unity = [2**i for i in range(self.dimM-1, -1, -1)]
		matrixM = [self.matrixM[i] | unity[i] for i in range(self.dimM)]
		matrixN = [self.matrixN[i] | unity[i] for i in range(self.dimN)]

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
		unity = [2**i for i in range(self.dimM-1, -1, -1)]
		matrixM = [self.matrixM[i] | unity[i] for i in range(self.dimM)]
		matrixN = [self.matrixN[i] | unity[i] for i in range(self.dimN)]
		
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

	def get_copy(self) -> 'MatrixBinary':
		""" Return a copy of matrix
		
		:return: copy of matrix
		:rtype: MatrixBinary
		
		>>> m = MatrixBinary(boolean=['001', '000', '111', '101', '100'])
		>>> m.get_copy()
		001,000,111,101,100
		"""
		return MatrixBinary(matrix=([i for i in self.matrixM],self.dimN))
		
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
		return s.rjust(dim, '0')

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
	
	def set_matrix(self, m) -> None:
		""" Set content of the matrix  from the matrixM given and dimN
		get a binary matrix contains a list of integers and with the number of columns
		
		:param tuple m: contains following indexes
		
			:matrixM: (list) rows with integers
			:dimN: (int) the number of columns
					
		>>> m = MatrixBinary(matrix=([1, 4, 2], 5))
		>>> m
		00001,00100,00010
		"""
		matrixM, self.dimN = m
		self.matrixM = matrixM[:]
		self.dimM = len(self.matrixM)
		self.matrixM2N()
	
	def set_matrix_boolean(self, matrix: list) -> None:
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
	
	def set_matrix_empty(self, dimM: int, dimN: int) -> None:
		""" Set an empty matrix containing only 0
		
		:param int dimM: number of rows
		:param int dimN: number of columns
		
		>>> m = MatrixBinary(empty=(4,8))
		>>> m
		00000000,00000000,00000000,00000000
		"""
		self.matrixM = [0 for _ in range(dimM)]
		self.matrixN = [0 for _ in range(dimN)]
		self._set_dim(dimM, dimN)
	
	def set_matrix_random(self, dimM: int, dimN: int, level: int=0, reflexive: bool=False) -> None:
		""" Set a matrix containing random booleans in integer representation
		
		the level represents the quantity of 0 compared to 1 (0-10)
		Reflexivity is the possibility for one node to go to itself
		
		:param int dimM: number of rows
		:param int dimN: number of columns
		:param int level=0: (0-10), quantity of 0 compared to 1
		:param bool reflexive: if True allow reflexive nodes, default is False
		
		>>> m = MatrixBinary(random=(4,8))
		>>> (m.dimM,m.dimN)
		(4, 8)
		"""
		self._set_dim(dimM, dimN)
		
		# TOKEEP
		#self.matrixM = [random.getrandbits(dimN) for _ in range(dimM)]
		
		chars = [
			"00000100010001000010000100010110010000100010000100010010001000011001101010001001000101000010010000001010000010000001000010000010001010001001000010100001000010000010000011000001010000100010010000000101000010100000100000010100000100001000000100000001010000010010000010000100000011001000101000001000000101000001000100001001010000010000101000010010000000101000000110000001000000000100001000000001000000010000010001000100001000010000001001000010001000010000001000100001000110000000100100000101000001000000101000001100000100001000001000100000100100001000000100001000001000000100000001000010000001000000010100000010000010000001000000010000100000010000000101000001001000001000010000001100000010100000100000010100000100010000000101000001000000100001001000000010100000011000000100000000010000100000000100000001",
			"00000100010001000010000100000010010000100010000100000010001000010001100000001001000001000000010000001010000010000001000010000010001000000001000010000001000010000010000001000000010000100000010000000101000000100000100000010000000100001000000100000001010000010010000010000100000011000000101000001000000101000001000100000001010000010000001000010010000000101000000110000001000000000100001000000001000000010000010001000100001000010000001001000010001000010000001000100001000110000000100100000100000001000000101000001000000100001000001000100000000100001000000100001000001000000100000001000010000001000000010100000010000010000001000000010000100000010000000101000001001000001000010000001100000010100000100000010100000100010000000101000001000000100001001000000010100000011000000100000000010000100000000100000001",
			 "00000100010001000010000100000010010000000010000100000010001000010001000000001001000001000000010000000010000010000001000010000010001000000001000010000001000010000010000001000000010000100000010000000100000000100000100000010000000100001000000100000001010000010000000010000100000010000000101000001000000100000001000100000001010000010000001000000010000000101000000100000001000000000100001000000001000000010000010001000100001000010000001001000000001000010000001000100001000100000000100100000100000001000000001000001000000100001000001000100000000100001000000100001000001000000100000001000010000001000000010000000010000010000001000000010000100000010000000101000001000000001000010000001000000010100000100000010000000100010000000101000001000000100000001000000010100000010000000100000000010000100000000100000001",
			"00000100010000000010000100000000010000000010000100000010001000000001000000001000000001000000010000000010000010000001000010000010001000000001000010000001000010000010000001000000010000100000010000000100000000100000100000010000000100001000000100000001010000010000000010000100000010000000101000001000000100000001000100000001010000010000001000000010000000101000000100000001000000000100001000000001000000010000010001000000001000010000000001000000001000010000001000100000000100000000100000000100000001000000001000001000000100001000001000100000000100001000000100001000001000000100000001000010000001000000010000000010000010000001000000010000100000010000000101000001000000001000010000001000000010100000100000010000000100010000000101000001000000100000001000000010100000010000000100000000010000100000000100000001",
			"00000100010000000000000100000000000000000010000100000010000000000001000000001000000000000000010000000010000010000001000010000010001000000001000000000001000010000000000001000000010000000000010000000100000000000000100000010000000100001000000100000001000000010000000010000000000010000000100000001000000100000001000000000001000000010000001000000010000000001000000100000001000000000100001000000001000000010000010001000000000000010000000000000000001000010000001000000000000100000000100000000000000001000000001000001000000100001000001000100000000100000000000100001000000000000100000001000000000001000000010000000000000010000001000000010000100000010000000100000001000000001000000000001000000010000000100000010000000100000000000100000001000000100000001000000000100000010000000100000000010000100000000100000001",
			"00000100000000000000000100000000000000000010000000000010000000000001000000000000000000000000010000000000000000000001000000000000000000000001000000000001000000000000000001000000000000000000010000000000000000000000100000000000000100000000000000000001000000010000000000000000000010000000000000001000000000000001000000000001000000000000001000000010000000000000000100000001000000000100000000000001000000010000010000000000000000010000000000000000001000000000001000000000000100000000000000000000000001000000000000000000000100000000000000000000000100000000000100000000000000000100000000000000000001000000000000000000000010000000000000010000000000000000000100000001000000000000000000001000000000000000100000000000000100000000000100000000000000100000001000000000000000010000000100000000010000000000000100000001",
			"00000100000000000000000000000000000000000000000000000010000000000000000000000000000000000000010000000000000000000000000000000000000000000001000000000000000000000000000001000000000000000000000000000000000000000000100000000000000100000000000000000001000000000000000000000000000010000000000000001000000000000001000000000001000000000000001000000000000000000000000100000000000000000100000000000000000000010000010000000000000000000000000000000000000000000000001000000000000000000000000000000000000001000000000000000000000000000000000000000000000100000000000000000000000000000100000000000000000000000000000000000000000010000000000000010000000000000000000100000000000000000000000000001000000000000000100000000000000100000000000100000000000000100000000000000000000000010000000000000000010000000000000000000001",
			"00000100000000000000000000000000000000000000000000000010000000000000000000000000000000000000010000000000000000000000000000000000000000000001000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000010000000000000000000000000000001000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000010000010000000000000000000000000000000000000000000000001000000000000000000000000000000000000001000000000000000000000000000000000000000000000100000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000001000000000000000000000000000000100000000000000000000000000000000000000000000000000010000000000000000000000000000000000000001",
			"00000100000000000000000000000000000000000000000000000010000000000000000000000000000000000000010000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000001000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000001",
			"00000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000001",
		]

		matrixM = []
		for _ in range(dimM):
			j = random.randint(0,200)
			matrixM.append(int("0b" + chars[level][j:j+dimN], 2))
		# reflexivity
		if not reflexive:
			unity_null = [''.join('1' if m != n else '0' for n in range(dimN)) for m in range(dimM)]
			unity_null = [int("0b" + line, 2) for line in unity_null]
			matrixM = [unity_null[i] & matrixM[i] for i in range(dimM) ]
		
		self.matrixM = matrixM
		self.matrixM2N()

	def set_matrix_unity(self, dim: int) -> None:
		""" Set an unity matrix: an empty square matrix with diagonal to 1

		:param int dim: number of rows and columns
		
		>>> m = MatrixBinary(unity=4)
		>>> print(m)
		dim 4,4
		1000
		0100
		0010
		0001
		"""
		#self.matrixM = [int('0b' + ''.join(('1' if i == j else '0') for i in range(dim)), 2) for j in range(dim)]
		#self.matrixN = [int('0b' + ''.join(('1' if i == j else '0') for i in range(dim)), 2) for j in range(dim)]

		unity = (2**i for i in range(dim - 1, -1, -1))
		self.matrixM = [i  for i in unity]
		self.matrixN = [i  for i in unity]
		self._set_dim(dim, dim)

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
	
	
