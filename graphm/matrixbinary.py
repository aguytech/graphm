'''
Created on Apr 26, 2021

@author: salem Aguemoun
'''
import random as rnd
import graphm.factor
import graphm.amatrix
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
	:var int dimM: rows number of matrix
	:var int dimN: columns number of matrix
	"""

	def __init__(self, **d) -> 'MatrixBinary':
		""" Set the matrix properties with type given by one in:
		
		* **matrix** get a binary matrixM and dimN
		* **reference** get a MatrixBinary matrix by reference
		* **matrices** get the 2 matrices matrixM & matrixN
		* **boolean** get a boolean matrix
		* **empty** get 2 dimensions of an empty matrix
		* **random** get 2 dimensions of randomized matrix
		* **unit** get the dimension of unit matrix

		:param dict \*\*d: options to specify the type of matrix
		
			with following indexes:
			
			:matrix: (tuple) matrixM in [int, ...] and dimN: int
			:matrces: (tuple) matrixM in [int, ...] and dimN: int
			:boolean: (list) matrix in [str, ...] or [[int,...], ...] or (str, ...) or ((int,...), ...)
			:empty: (tuple) dimensions for matrix (dimM: int, dimN: int)
			:random: (tuple) dimensions for matrix (dimM: int, dimN: int)
			:unit: (int) dimensions for square matrix
			
		For default options see :class:`AMatrix.__init__`
		
		"""
		super().__init__(**d)
	
	def __deepcopy__(self) -> 'MatrixBinary':
		return MatrixBinary(matrices=(self.matrixM, self.matrixN))
	
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

	def closure_reflexive(self, full=False) -> dict:
		""" Return the transitive closure of itself in a new matrix
		using an internal optimized product
		
		If argument 'full' is False, the transitive closure stop when closure(d) = closure(d-1)
		
		:param bool full: if True calculates all ranks, otherwise only until a stabilized closure
			
			default = False
		
		:return: The transitive closure and the deep of stabilized closure
		:rtype: tuple(MatrixBinary: closure, int: deep)
		
		>>> m = MatrixBinary(boolean=['00001', '00100', '00010', '01010', '00010'])
		>>> result = m.closure_reflexive()
		>>> result['closure']
		11111,01110,01110,01110,01111
		"""
		if self.dimM != self.dimN:
			raise ValueError("Matrix have wrong dimensions")
		
		matrixM = MatrixBinary.get_matrixX_united(self.matrixM, self.dimM)
		matrixN = MatrixBinary.get_matrixX_united(self.matrixN, self.dimN)
		
		deep = 0
		for _ in range(1, self.dimM):
			deep += 1
			matrixM_new = [0] * self.dimM
			for m in range(self.dimM):
				matrixM_new[m] = int('0b' + ''.join([('0' if (matrixM[m] & matrixN[n]) == 0 else '1') for n in range(self.dimN)]), 2)
			if not full:
				if matrixM_new == matrixM:
					break

			matrixM= matrixM_new
		return {
			'matrix': self,
			'closure': MatrixBinary(matrix=(matrixM, self.dimN)),
			'reflexive': True,
			'deep': deep,
			}

	def closure_reflexive_optimized(self, optimize='soft') -> dict:
		""" Return the transitive closure of itself in a new matrix
		using class :class:`Factor` to optimize products
		
		If argument 'full' is False, the transitive closure stop when closure(d) = closure(d-1)
		
		:return: The transitive closure with a deep of stabilized closure
		:rtype: MatrixBinary
		
		>>> m = MatrixBinary(boolean=['00001', '00100', '00010', '01010', '00010'])
		>>> result = m.closure_reflexive_optimized()
		>>> result['closure']
		11111,01110,01110,01110,01111
		"""
		if self.dimM != self.dimN:
			raise ValueError("Matrix have wrong dimensions")
		
		matrix = self.copy()
		matrix.matrixM = MatrixBinary.get_matrixX_united(self.matrixM, self.dimM)
		matrix.matrixN = MatrixBinary.get_matrixX_united(self.matrixN, self.dimN)
		
		factor = Factor(self.dimM - 1, optimize=optimize)
		closure, operations = factor.power(matrix)
		return {
			'matrix': self,
			'closure': closure,
			'reflexive': True,
			'operations': operations
			}

	def closure_matrix(self, add=False, full=False) -> dict:
		""" Return the transitive closure of itself and intermediate adjacency matrices
		using an internal optimized product
		
		If argument 'full' is False, the transitive closure stop when closure(d) = closure(d-1)
		
		:param bool add: if True adds unit matrix otherwise no
			
			default = False
			
		:param bool full: if True calculates all ranks, otherwise only until a stabilized closure
			
			default = False
		
		:return: The transitive closure with intermediate adjacency matrices and the deep of stabilized closure
		:rtype: tuple(MatrixBinary: closure, int: deep, list(MatrixBinary): intermediate matrices)
		
		>>> m = MatrixBinary(boolean=['00001', '00100', '00010', '01010', '00010'])
		>>> result = m.closure_matrix()
		>>> result['closure']
		01111,01110,01110,01110,01110
		
		>>> m = MatrixBinary(boolean=['10001', '01100', '00110', '01010', '00011'])
		>>> result = m.closure_matrix()
		>>> result['closure']
		11111,01110,01110,01110,01111
		"""
		if self.dimM != self.dimN:
			raise ValueError("Matrix have wrong dimensions")
		
		if add:
			matrix = MatrixBinary(matrices=(
				MatrixBinary.get_matrixX_united(self.matrixM, self.dimM),
				MatrixBinary.get_matrixX_united(self.matrixN, self.dimN)
				))
			reflexive = True
		else:
			matrix = MatrixBinary(matrices=(self.matrixM, self.matrixN))
			reflexive = MatrixBinary.is_reflexive(self)
		
		matrices = [matrix]
		matrixM = matrix.matrixM[:]
		closureM = matrix.matrixM[:]
		closureM_tmp = matrix.matrixM
		
		deep = 0
		for i in range(1, self.dimM):
			deep += 1
			for m in range(self.dimM):
				matrixM[m] = int('0b' + ''.join([('0' if (matrices[i-1].matrixM[m] & matrix.matrixN[n]) == 0 else '1') for n in range(self.dimN)]), 2)
	
			closureM = [closureM[m] | matrixM[m] for m in range(self.dimM)]
			if not full:
				if closureM == closureM_tmp:
					break
			matrices.append(MatrixBinary(matrix=(matrixM, self.dimN)))
			closureM_tmp = closureM
					
		return {
			'matrix': self,
			'matrices': matrices,
			'closure': MatrixBinary(matrix=(closureM, self.dimN)),
			'reflexive': reflexive,
			'deep': deep,
			}
	
	def closure_slides(self, add=False,  full=False) -> dict:
		""" Return the transitive closure of itself and intermediate adjacency matrices matrixM
		using an internal optimized product
		
		If argument 'full' is False, the transitive closure stop when closure(d) = closure(d-1)
		
		:param bool add: if True adds unit matrix otherwise no
			
			default = False
			
		:param bool full: if True calculates all ranks, otherwise only until a stabilized closure
			
			default = False
		
		:return: The transitive closure with intermediate adjacency matrices matrixM
		:rtype: tuple(MatrixBinary: closure, int: deep, list(matrixM): matrice slides)
		
		>>> m = MatrixBinary(boolean=['00001', '00100', '00010', '01010', '00010'])
		>>> result = m.closure_slides()
		>>> result['closure']
		01111,01110,01110,01110,01110
		"""
		if self.dimM != self.dimN:
			raise ValueError("Matrix have wrong dimensions")
		
		if add:
			matrixM = MatrixBinary.get_matrixX_united(self.matrixM, self.dimM)
			matrixN = MatrixBinary.get_matrixX_united(self.matrixN, self.dimN)
			reflexive = True
		else:
			matrixM, matrixN = self.matrixM[:], self.matrixN
			reflexive = self.is_reflexive(self)

		matrix = self.copy()
		matrices = [matrixM]
		closureM = matrix.matrixM[:]
		closureM_tmp = matrix.matrixM[:]
		
		deep = 0
		for i in range(1, self.dimM):
			deep += 1
			matrixM = [0] * self.dimM
			for m in range(self.dimM):
				matrixM[m] = int('0b' + ''.join([('0' if (matrices[i-1][m] & matrixN[n]) == 0 else '1') for n in range(self.dimN)]), 2)
			
			closureM = [closureM[m] | matrixM[m] for m in range(self.dimM)]
			if not full:
				if closureM == closureM_tmp:
					break
			matrices.append(matrixM)
			closureM_tmp = closureM
						
		return {
			'matrix': self,
			'matrices': matrices,
			'closure': MatrixBinary(matrix=(closureM, self.dimN)),
			'reflexive': reflexive,
			'deep': deep,
			}

	def copy(self) -> 'MatrixBinary':
		""" Return a copy of matrix
		
		:return: copy of matrix
		:rtype: MatrixBinary
		
		>>> m = MatrixBinary(boolean=['001', '000', '111', '101', '100'])
		>>> m.copy()
		001,000,111,101,100
		"""
		return self.__deepcopy__()
		
	@staticmethod
	def get_edges_count(matrix: 'MatrixBinary') -> int:
		""" Give the number of edges in matrix
		
		:return: the number of edges in matrix
		:rtype: int
		
		>>> m =  MatrixBinary(boolean=['000', '000', '000'])
		>>> MatrixBinary.get_edges_count(m)
		0
		
		>>> m =  MatrixBinary(boolean=['010010', '001000', '010101', '010010', '000000', '000000'])
		>>> MatrixBinary.get_edges_count(m)
		8
		"""
		matrixMS = [MatrixBinary.get_int2str(line, matrix.dimN ) for line in matrix.matrixM]
		return len([i for line in matrixMS for i in line if i == '1'])
		
	@staticmethod
	def get_int2str(line: int, dim: int) -> str:
		""" Return the converted  boolean string from binary integer,
		string length is adjusted by to dim.
		
		dim is the dimension of line
		
		.. WARNING :: Use dimN for matrixM & dimM for matrixN
		
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
	def get_matrix_formated(matrix: 'MatrixBinary', style='int') -> any:
		""" Return the formated matrix passed in argument
		
		:param str style: style of export of closure
			* **int** return 0/1 integers
			* **str** Return string of '0'/'1'
			* **bin** return binary integers

		:return: the formated matrix of transitive closure
		:rtype: list
		
		>>> m =  MatrixBinary(boolean=['010010', '001000', '010100', '010010', '000000', '000000'])
		
		>>> print(MatrixBinary.get_matrix_formated(m))
		[[0, 1, 0, 0, 1, 0], [0, 0, 1, 0, 0, 0], [0, 1, 0, 1, 0, 0], [0, 1, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
		
		>>> print(MatrixBinary.get_matrix_formated(m, style='str'))
		['010010', '001000', '010100', '010010', '000000', '000000']
		
		>>> print(MatrixBinary.get_matrix_formated(m, style='bin'))
		[18, 8, 20, 18, 0, 0]
		"""
		if style == "int":
			return [[int(i) for i in MatrixBinary.get_int2str(m, matrix.dimN)]for m in matrix.matrixM]
		elif style == "str":
			return [MatrixBinary.get_int2str(m, matrix.dimN) for m in matrix.matrixM]
		elif style == "bin":
			return matrix.matrixM[:]
	
	@staticmethod
	def get_matrix_desunited(matrix : 'MatrixBinary') -> 'MatrixBinary':
		""" Returns the MatrixBinary matrix to which the unit matrix has been added
		:param MatrixBinary matrix: 
		
		:return: returns the matrix plus the unit matrix
		:rtype: MatrixBinary

		>>> m = MatrixBinary.get_matrix_desunited(MatrixBinary(boolean=['010010', '001000', '010100', '010010', '000000', '000000']))
		>>> print(m)
		dim 6,6
		010010
		001000
		010100
		010010
		000000
		000000
		
		>>> m = MatrixBinary.get_matrix_desunited(MatrixBinary(boolean=['110010', '011000', '011100', '010110', '000010', '000001']))
		>>> print(m)
		dim 6,6
		010010
		001000
		010100
		010010
		000000
		000000
		"""
		desunit = [2**(matrix.dimM) - 2**i -1 for i in range(matrix.dimM-1,-1,-1)]
		matrix = matrix.copy()
		matrix.matrixM = [matrix.matrixM[i] & desunit[i] for i in range(matrix.dimM)]
		matrix.matrixN = [matrix.matrixN[i] & desunit[i] for i in range(matrix.dimN)]
		return matrix

	@staticmethod
	def get_matrix_united(matrix : 'MatrixBinary') -> 'MatrixBinary':
		""" Returns the MatrixBinary matrix to which the unit matrix has been added
		:param MatrixBinary matrix: 
		
		:return: returns the matrix plus the unit matrix
		:rtype: MatrixBinary

		>>> m = MatrixBinary.get_matrix_united(MatrixBinary(boolean=['010010', '001000', '010100', '010010', '000000', '000000']))
		>>> print(m)
		dim 6,6
		110010
		011000
		011100
		010110
		000010
		000001
		
		>>> m = MatrixBinary.get_matrix_united(MatrixBinary(boolean=['110010', '011000', '011100', '010110', '000010', '000001']))
		>>> print(m)
		dim 6,6
		110010
		011000
		011100
		010110
		000010
		000001
		"""
		unit = [2**i for i in range(matrix.dimM-1, -1, -1)]
		matrix = matrix.copy()
		matrix.matrixM = [matrix.matrixM[i] | unit[i] for i in range(matrix.dimM)]
		matrix.matrixN = [matrix.matrixN[i] | unit[i] for i in range(matrix.dimN)]
		return matrix

	@staticmethod
	def get_matrixX_desunited(matrixX: list, dimX: int) -> list:
		""" Returns the single matrix (M or N) to which the unit matrix has been added
		
		.. WARNING :: for matrixM use dimN and for matrixN use dimM
		
		:param list matrixX: matrixM or matrixN
		
		:return: returns the matrix matrixX (M or N) plus the unit matrix
		:rtype: list

		>>> m = MatrixBinary(boolean=['010010', '001000', '010100', '010010', '000000', '000000'])
		>>> m.matrixM = MatrixBinary.get_matrixX_desunited(m.matrixM, m.dimN)
		>>> print(m)
		dim 6,6
		010010
		001000
		010100
		010010
		000000
		000000
		
		>>> m = MatrixBinary(boolean=['110010', '011000', '011100', '010110', '000010', '000001'])
		>>> m.matrixM = MatrixBinary.get_matrixX_desunited(m.matrixM, m.dimN)
		>>> print(m)
		dim 6,6
		010010
		001000
		010100
		010010
		000000
		000000
		"""
		desunit = [2**dimX - 2**i -1 for i in range(dimX-1,-1,-1)]
		return [matrixX[i] & desunit[i] for i in range(dimX)]

	@staticmethod
	def get_matrixX_united(matrixX: list, dimX: int) -> list:
		""" Returns the single matrix (M or N) to which the unit matrix has been added
		
		.. WARNING :: for matrixM use dimN and for matrixN use dimM
		
		:param list matrixX: matrixM or matrixN
		
		:return: returns the matrix matrixX (M or N) plus the unit matrix
		:rtype: list

		>>> m = MatrixBinary(boolean=['010010', '001000', '010100', '010010', '000000', '000000'])
		>>> m.matrixM = MatrixBinary.get_matrixX_united(m.matrixM, m.dimN)
		>>> print(m)
		dim 6,6
		110010
		011000
		011100
		010110
		000010
		000001
		
		>>> m = MatrixBinary(boolean=['110010', '011000', '011100', '010110', '000010', '000001'])
		>>> m.matrixM = MatrixBinary.get_matrixX_united(m.matrixM, m.dimN)
		>>> print(m)
		dim 6,6
		110010
		011000
		011100
		010110
		000010
		000001
		"""
		unit = [2**i for i in range(dimX - 1, -1, -1)]
		return [matrixX[i] | unit[i] for i in range(dimX)]

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

	@staticmethod
	def is_reflexive(matrix: 'MatrixBinary') -> bool:
		""" return True if matrix is unit
		
		:param MatrixBinary matrix: matrix of graph
		
		:return: True if matrix is unit
		:rtype: bool

		>>> m = MatrixBinary(boolean=[[1, 0, 0, 0, 1], [0,1, 1, 0, 0], [0, 0, 1, 1, 0]])
		>>> MatrixBinary.is_reflexive(m)
		False

		>>> m = MatrixBinary(boolean=[[0, 0, 0, 0, 1], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 1, 1], [0, 0, 0, 1, 0]])
		>>> MatrixBinary.is_reflexive(m)
		False

		>>> m = MatrixBinary(boolean=[[1, 0, 0, 0, 1], [0, 1, 1, 0, 0], [0, 0, 1, 1, 0], [0, 0, 0, 1, 0], [0, 0, 0, 1, 1]])
		>>> MatrixBinary.is_reflexive(m)
		True
		"""
		if matrix.dimM != matrix.dimN:
			return False
		
		unitM = [2**i for i in range(matrix.dimM - 1, -1, -1)]
		for m in range(matrix.dimM):
			if matrix.matrixM[m] != matrix.matrixM[m] | unitM[m]:
				return False
		return True
		
	@staticmethod
	def is_symmetric(matrix: 'MatrixBinary') -> bool:
		""" Return true if the matrix is symmetric

		:param MatrixBinary matrix: matrix of graph
		
		:return: True if the matrix is symmetric
		:rtype: bool
		
		>>> m =  MatrixBinary(boolean=['010010', '001000', '010100', '010010', '000000', '000000'])
		>>> MatrixBinary.is_symmetric(m)
		False

		>>> m = MatrixBinary(boolean=['011010', '101000', '110100', '101010', '100100', '101000'])
		>>> MatrixBinary.is_symmetric(m)
		False

		>>> m = MatrixBinary(boolean=['011010', '101000', '110100', '001010', '100100', '000000'])
		>>> MatrixBinary.is_symmetric(m)
		True
		"""
		if matrix.dimM != matrix.dimN:
			return False
		
		for i in range(matrix.dimM):
			if matrix.matrixM[i] != matrix.matrixN[i]:
				return False
		return True
	
	@staticmethod
	def is_symmetric_pre(matrix: 'MatrixBinary') -> bool:
		""" returns True if the matrix has minimal symmetry with predecessor
		one back edge for each edge
		
		.. IMPORTANT:: return True if each edge has one edge back
		
		:param MatrixBinary matrix: matrix of graph
		
		:return: True if the matrix has minimal symmetry with predecessor
		:rtype: bool
		
		>>> m =  MatrixBinary(boolean=['010010', '001000', '010100', '010010', '000000', '000000'])
		>>> MatrixBinary.is_symmetric_pre(m)
		False

		>>> m = MatrixBinary(boolean=['011010', '101000', '110100', '101010', '100100', '101000'])
		>>> MatrixBinary.is_symmetric_pre(m)
		True

		>>> m = MatrixBinary(boolean=['011010', '101000', '110100', '001010', '100100', '000000'])
		>>> MatrixBinary.is_symmetric_pre(m)
		True
		"""
		if matrix.dimM != matrix.dimN:
			return False
		
		for i in range(matrix.dimM):
			mask = 2**(matrix.dimM-i)-1
			if (matrix.matrixM[i] & mask) & (matrix.matrixN[i] & mask)  != (matrix.matrixM[i] & mask):
				return False
		return True
	
	@staticmethod
	def is_symmetric_suc(matrix: 'MatrixBinary') -> bool:
		""" returns True if the matrix has minimal symmetry with successor
		one edge for each back edge
		
		.. IMPORTANT:: return True if each back edge has one edge
		
		:param MatrixBinary matrix: matrix of graph
		
		:return: True True if the matrix has minimal symmetry with successor
		:rtype: bool
		
		>>> m =  MatrixBinary(boolean=['010010', '001000', '010100', '010010', '000000', '000000'])
		>>> MatrixBinary.is_symmetric_suc(m)
		False

		>>> m = MatrixBinary(boolean=['011011', '101011', '110100', '001010', '100100', '000000'])
		>>> MatrixBinary.is_symmetric_suc(m)
		True

		>>> m = MatrixBinary(boolean=['011010', '101000', '110100', '001010', '100100', '000000'])
		>>> MatrixBinary.is_symmetric_suc(m)
		True
		"""
		if matrix.dimM != matrix.dimN:
			return False
		
		for i in range(matrix.dimN):
			mask = 2**(matrix.dimN-i)-1
			if (matrix.matrixN[i] & mask) & (matrix.matrixM[i] & mask)  != (matrix.matrixN[i] & mask):
				return False
		return True
	
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
	
	def paths_cycle(self, node_start:int, deep: int=0) -> dict:
		""" Return a dictionary of paths of cycles found starting from node
		
		.. IMPORTANT:: You can limit the deep (rank) of searching by give deep in argument
		
		:param int node_start: the starting node to search paths
		:param int deep: limit of rank from starting node to find paths of cycles

		:return: paths of cycles
		:rtype: dict

			:paths_cycle: (list) all paths of cycles
			:nodes_reached: (set) all reached nodes including starting node

		>>> m = MatrixBinary(boolean=['00001', '00100', '00010', '00000', '01001'])
		>>> m.paths_cycle(4)
		{'reflexive': False, 'paths_cycle': [], 'nodes_reached': {1, 2, 3, 4}, 'deep': 4}
		
		>>> m = MatrixBinary(boolean=['010010', '001000', '010100', '010010', '000000', '000000'])

		>>> m.paths_cycle(0)
		{'reflexive': False, 'paths_cycle': [[1, 2], [1, 2, 3]], 'nodes_reached': {0, 1, 2, 3, 4}, 'deep': 5}
		
		>>> m.paths_cycle(4)
		{'reflexive': False, 'paths_cycle': [], 'nodes_reached': {4}, 'deep': 0}
		"""
		nodes_reached = {node_start}
		paths_cycle = []
		paths_cycle_set = set()
		paths = [[node_start]]
		deep_final = deep if deep else min(self.dimM, self.dimN)
		matrixMS = [MatrixBinary.get_int2str(line, self.dimN) for line in self.matrixM]
		# successors without reflexive  ones
		successors_all = {m: [n for n in range(self.dimN) if matrixMS[m][n] == '1' and m != n] for m in range(self.dimM)}

		# no successors or itself
		if self.matrixM[node_start] in (0, 2**(self.dimM - node_start - 1)):
			paths = []
		
		deep = 0
		while deep < deep_final and paths:
			paths_tmp = paths
			paths = []
			for path in paths_tmp:
				successors = successors_all[path[deep]]
				for node in successors:
					nodes_reached.add(node)
					if node not in path:
						paths.append(path + [node])
					else:
						path_cycle = path[path.index(node):]
						path_cycle_set = frozenset(path_cycle)
						if path_cycle_set not in paths_cycle_set:
							paths_cycle.append(path_cycle)
							paths_cycle_set.add(path_cycle_set)
			deep += 1
		return {
			'reflexive': MatrixBinary.is_reflexive(self),
			'paths_cycle': paths_cycle,
			'nodes_reached': nodes_reached,
			'deep': deep,
			}
	
	def paths_from(self, node_start:int, deep: int=0) -> dict:
		""" Return a dictionary of all paths starting from node
		
		.. IMPORTANT:: You can limit the deep (rank) of searching by give deep in argument
		
		:param int node_start: the starting node to search paths
		:param int deep: limit of rank from starting node to find paths of cycles

		:return: paths
		:rtype: dict

			:paths_final: (list) all paths which access to maximal deep
			:paths_ended: (list) all paths which deep less than maximal one
			:paths_cycle: (list) all paths of elementary cycles
			:nodes_reached: (set) all reached nodes including starting node

		>>> m = MatrixBinary(boolean=['010010', '001000', '010100', '010010', '000000', '000000'])
	
		>>> m.paths_from(0)
		{'reflexive': False, 'paths_deep': [], 'paths_ended': [[0, 4], [0, 1, 2, 3, 4]], 'paths_cycle': [[1, 2], [1, 2, 3]], 'nodes_reached': {0, 1, 2, 3, 4}, 'deep': 5}
	
		>>> m.paths_from(0,2)
		{'reflexive': False, 'paths_deep': [[0, 1, 2]], 'paths_ended': [[0, 4]], 'paths_cycle': [], 'nodes_reached': {0, 1, 2, 4}, 'deep': 2}
		
		>>> m.paths_from(5)
		{'reflexive': False, 'paths_deep': [], 'paths_ended': [], 'paths_cycle': [], 'nodes_reached': {5}, 'deep': 0}
		"""
		paths_ended = []
		paths_cycle = []
		paths_cycle_set = set()
		paths = [[node_start]]
		nodes_reached = {node_start}
		deep_final = deep if deep else min(self.dimM, self.dimN)
		matrixMS = [MatrixBinary.get_int2str(line, self.dimN) for line in self.matrixM]
		# successors without reflexive  ones
		successors_all = {m: [n for n in range(self.dimN) if matrixMS[m][n] == '1' and m != n] for m in range(self.dimM)}

		# no successors or itself
		if self.matrixM[node_start] in (0, 2**(self.dimM - node_start - 1)):
			paths = []
		
		deep = 0
		while deep < deep_final and paths:
			paths_tmp = paths
			paths = []
			for path in paths_tmp:
				successors = successors_all[path[deep]]
				if successors:
					for node in successors:
						nodes_reached.add(node)
						if node not in path:
							paths.append(path + [node])
						else:
							path_cycle = path[path.index(node):]
							path_cycle_set = frozenset(path_cycle)
							if path_cycle_set not in paths_cycle_set:
								paths_cycle.append(path_cycle)
								paths_cycle_set.add(path_cycle_set)
				else:
					paths_ended.append(path)
			deep += 1

		return {
			'reflexive': MatrixBinary.is_reflexive(self),
			'paths_deep': paths,
			'paths_ended': paths_ended,
			'paths_cycle': paths_cycle,
			'nodes_reached': nodes_reached,
			'deep': deep,
			}
	
	def paths_from_to(self, node_start: int, node_end: int, deep: int=0) -> dict:
		""" Return a dictionary of all paths starting from node 'node_start' to 'node_end'
		
		.. IMPORTANT:: You can limit the deep (rank) of searching by give deep in argument
		
		:param int node_start: the starting node
		:param int node_end: the ending node
		:param int deep: limit of rank from starting node to find paths of cycles

		:return: paths
		:rtype: dict

			:count: (int) iterations count 
			:nodes_reached: (set) all reached nodes including starting node
			:paths_final: (list) all paths which access to maximal deep
			:reached: (bool) True if node_end is reached by node_start

		>>> m = MatrixBinary(boolean=['010010', '001000', '010100', '010010', '000000', '000000'])
	
		>>> m.paths_from_to(0, 3)
		{'reflexive': False, 'nodes_reached': {0, 1, 2, 4}, 'paths_final': [[0, 1, 2, 3]], 'reached': True, 'deep': 3, 'count': 6}
	
		>>> m.paths_from_to(0, 5)
		{'reflexive': False, 'nodes_reached': {0, 1, 2, 3, 4}, 'paths_final': [], 'reached': False, 'deep': 5, 'count': 8}
		
		>>> m.paths_from_to(5 ,5)
		{'reflexive': False, 'nodes_reached': {5}, 'paths_final': [], 'reached': False, 'deep': 0, 'count': 1}
		
		>>> m = MatrixBinary(boolean=['010010', '001000', '010100', '010010', '000000', '000001'])
	
		>>> m.paths_from_to(5 ,5)
		{'reflexive': False, 'nodes_reached': {5}, 'paths_final': [], 'reached': True, 'deep': 0, 'count': 1}
		"""
		count = 1
		reached = False
		nodes_reached = {node_start}
		paths = [[node_start]]
		paths_final = []
		deep_final = deep if deep else min(self.dimM, self.dimN)
		matrixMS = [MatrixBinary.get_int2str(line, self.dimN) for line in self.matrixM]
		reflexive = MatrixBinary.is_reflexive(self)
		# successors without reflexive  ones
		successors_all = {m: [n for n in range(self.dimN) if matrixMS[m][n] == '1' and m != n] for m in range(self.dimM)}

		if node_end == node_start and matrixMS[node_start][node_end] == '1':
			reached = True
		# no successors or itself
		elif self.matrixM[node_start] in (0, 2**(self.dimM - node_start - 1)):
			paths = []
		
		deep = 0
		while not reached and paths and deep < deep_final:
			paths_tmp = paths
			paths = []
			for path in paths_tmp:
				successors = successors_all[path[deep]]
				for node in successors:
					count += 1
					if node == node_end:
						paths_final.append(path + [node])
						reached = True
					else:
						if node not in path:
							nodes_reached.add(node)
							paths.append(path + [node])
			deep += 1
			
		return {
			'reflexive': reflexive,
			'nodes_reached': nodes_reached,
			'paths_final': paths_final,
			'reached': reached,
			'deep': deep,
			'count': count,
			}
	
	def report(self) -> dict:
		""" Return a report of c properties
				
		:return: a report of matrix properties
		:rtype: dict
		
			:matrix: (list) original matrix in format 'str'
			:closure: (list) transitive closure in format 'str'

			:reflexive: (bool) if true graph is reflexive
			:symmetric: (bool) if true graph is symmetric
			:symmetric_pre: (bool) if true matrix has minimal symmetry with predecessor (each edge has a back edge)
			:symmetric_suc: (bool) if true matrix has minimal symmetry with successor (each back edge has an edge)
			
		:return: a report of matrix properties
		:rtype: dict

		.. IMAGE:: files/m.svg

		>>> m = MatrixBinary(boolean=['010010', '001000', '010100', '010010', '000000', '000000'])
		>>> print(m)
		dim 6,6
		010010
		001000
		010100
		010010
		000000
		000000

		>>> print(m.report())
		{'symmetric': False, 'symmetric_pre': False, 'symmetric_suc': False, 'reflexive': False, 'matrix': ['010010', '001000', '010100', '010010', '000000', '000000']}

		.. IMAGE:: files/m2.svg

		>>> m = MatrixBinary(boolean=['010010', '001001', '010100', '010010', '000000', '100000'])
		>>> print(m)
		dim 6,6
		010010
		001001
		010100
		010010
		000000
		100000

		>>> print(m.report())
		{'symmetric': False, 'symmetric_pre': False, 'symmetric_suc': False, 'reflexive': False, 'matrix': ['010010', '001001', '010100', '010010', '000000', '100000']}
		"""
		report = {
			'symmetric': MatrixBinary.is_symmetric(self),
			'symmetric_pre': MatrixBinary.is_symmetric_pre(self),
			'symmetric_suc': MatrixBinary.is_symmetric_suc(self),
			'reflexive': MatrixBinary.is_reflexive(self),
			}
		
		report['matrix'] = MatrixBinary.get_matrix_formated(self, style='str')
			
		return report

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
		len_line = len(matrix[0]) if matrix else 0
		self._set_dim(len(matrix), len_line)
		
		matrixM = []
		for line in matrix:
			# transform list lines in str lines 
			if isinstance(line, list):
				line = ''.join(str(i) for i in line)
			if len(line) != len_line:
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
		self.matrixM = [0] * dimM
		self.matrixN = [0] * dimN
	
	def set_from_matrix(self, matrix: tuple) -> None:
		""" Set content of the matrix  from the matrixM and dimN
		get a binary matrix contains a list of integers and with the number of columns
		
		:param tuple m: contains following indexes
		
			:matrixM: (list) rows with integers
			:dimN: (int) the number of columns
					
		>>> m = MatrixBinary(matrix=([1, 4, 2], 5))
		>>> m
		00001,00100,00010
		"""
		matrixM, self.dimN = matrix
		self.matrixM = matrixM[:]
		self.dimM = len(self.matrixM)
		self.matrixM2N()
	
	def set_from_matrices(self, matrices: tuple) -> None:
		""" Set content of the matrix  from the matrices: matrixM & matrixN
		get a binary matrix contains a list of integers and with the number of columns
		
		:param tuple m: contains following indexes
		
			:matrixM: (list) rows of matrix with integers
			:matrixN: (list) columns of matrix with integers
					
		>>> m = MatrixBinary(matrices=([1, 4, 2],[0, 0, 2, 1, 4]))
		>>> m
		00001,00100,00010
		"""
		matrixM, matrixN = matrices
		self.matrixM = matrixM[:]
		self.matrixN = matrixN[:]
		self.dimM = len(self.matrixM)
		self.dimN = len(self.matrixN)
	
	def set_from_nodes_edges(self, nodes_edges: tuple) -> None:
		""" Set boolean matrix from nodes or edges
		
		.. NOTE:: if edges are given without nodes, the nodes are generate from edges automatically
		
		:param tuple nodes_edges: tuple(node, edges)
		
			:edges: (iter) edges in format 'in,out' or [in, out] or (in, out)
			:nodes: (iter) names of nodes in iterable of strings

		>>> m = MatrixBinary(nodes_edges=(['A','B','C','D','E'], ('A-D','D-A','D-C','C-A','B-C','B-B')))
		>>> print(m)
		dim 5,5
		00010
		01100
		10000
		10100
		00000
		
		>>> m = MatrixBinary(nodes_edges=((),('A-D','D-A','D-C','C-A','B-C','B-B')))
		>>> print(m)
		dim 4,4
		0001
		0110
		1000
		1010
				
		>>> m = MatrixBinary(nodes_edges=(['A','B','C','D','E'],()))
		>>> print(m)
		dim 5,5
		00000
		00000
		00000
		00000
		00000
		"""
		def convert_edges(edges: iter) -> list:
			""" Convert edges to list of single elements
			
			:param list edges: edges of graph
			
			:return: edges in single elements
			:rtype: list
			"""
			if not edges:
				return []
			
			# str
			if isinstance(edges, str):
				edges = [(i, j) for i, j in edges.split(',')]
			# iter(str)
			elif isinstance(edges[0], str):
					edges = [[i for i in edge.split('-')] for edge in edges]
			# dict
			elif isinstance(edges, dict):
				edges = [(str(a), str(b)) for a, b in edges.items()]
			else:
				edges = [(str(a), str(b)) for a, b in edges]
			
			return edges
	
		def convert_nodes(nodes: iter) -> list:
			""" Convert edges to list of single elements
			
			:param list edges: edges of graph
			
			:return: edges in single elements
			:rtype: list
			"""
			if not nodes:
				return []
			
			if isinstance(nodes, str):
				nodes = nodes.split(',')
			nodes = [str(i) for i in nodes]
			
			return nodes

		nodes, edges = nodes_edges
		
		edges = convert_edges(edges)

		nodes_edges = {node for edge in edges for node in edge} if edges else set()
		if nodes:
			nodes = list(nodes_edges | set(nodes))
			nodes.sort()
		else:
			nodes = list(nodes_edges)
			nodes.sort()
		
		# dim
		self.dimM = len(nodes)
		self.dimN = self.dimM
		
		# matrix
		matrix = [['0' for _ in range(self.dimN)] for _ in range(self.dimM)]
		nodes_rev = {node: i for i,node in enumerate(nodes)}
		for edgeIn, edgeOut in edges:
			matrix[nodes_rev[edgeIn]][nodes_rev[edgeOut]] = '1'
		self.matrixM = [int('0b' + ''.join(line), 2) for line in matrix]
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

	def set_from_reference(self, matrix) -> None:
		""" Set content of the matrix  from the matrixM given and dimN
		get a binary matrix contains a list of integers and with the number of columns
		
		.. WARNING:: matrix is passed by reference !
		
		:param tuple m: contains following indexes
		
			:matrixM: (list) rows with integers
			:dimN: (int) the number of columns
					
		>>> m = MatrixBinary(matrix=([1, 4, 2], 5))
		>>> m
		00001,00100,00010
		"""
		matrixM, self.dimN = matrix
		self.matrixM = matrixM
		self.dimM = len(self.matrixM)
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

	def str(self) -> str:
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
	
	def str_report(self) -> str:
		""" Return a string of report() content
		
			See MatrixBinary.report()
		
		>>> m = MatrixBinary(boolean=['010010', '001000', '010100', '010010', '000000', '000000'])
		>>> print(m.str_report())
		matrix: ['010010', '001000', '010100', '010010', '000000', '000000']
		reflexive               False
		symmetric               False
		symmetry predecessor    False
		symmetry successor      False
		"""
		trans = {
		'symmetric': 'symmetric              ',
		'symmetric_pre': 'symmetry predecessor   ',
		'symmetric_suc': 'symmetry successor     ',
		'reflexive': 'reflexive              ',
		}
		
		data = self.report()
		report = f"matrix: {data.pop('matrix')}"
		
		data = sorted(data.items())
		for k, v in data:
			report += f"\n{trans[k]} {v}"
		
		return report

	def transposed(self) -> 'MatrixBinary':
		""" Return the transpose of this matrix
		The diagonal symmetry of matrix
		
		:return: the transpose of this matrix
		:rtype: MatrixBinary

		>>> m = MatrixBinary(boolean=[[0, 0, 0, 0, 1], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0]])
		>>> m2 = m.transposed()
		>>> m2
		000,000,010,001,100
		"""
		return MatrixBinary(matrices=(self.matrixN[:], self.matrixM[:]))
	

