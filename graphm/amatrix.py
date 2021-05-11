'''
Created on Apr 26, 2021

@author: salem Aguemoun
'''
class AMatrix(object):
	"""Abstract class for matrix (fake abstract)
	
	Defines methods:
	\__init__()
	_set_dim()
	get_dim()
	
	Shows what needs to be instantiated
	
	:var bool reflexive: Default value for the matrix reflexivity.
	
		if True matrix is reflexive and for example generated matrices have the diagonal unity

	.. WARNING:: Not to be instantiated, just to be inherited
	
	.. CAUTION:: Instance variables
	
	:var int dimM: number of rows
	:var int dimN: number of columns
	:var bool isreflexive: if True matrix is reflexive and for example generated matrices have the diagonal unity

	"""
	isreflexive = False
	
	def __init__(self, **d) -> object:
		"""Set the matrix property with type given by one option in:
		
		* **matrix** get a matrix (depends of caller object)
		* **empty** get 2 dimensions of an empty matrix
		* **random** get 2 dimensions of randomized matrix
		* **unity** get the dimension of unity matrix

		:param dict \*\*d: options to specify the type of matrix
		
			:empty: (tuple) dimensions for matrix (dimM: int, dimN: int)
			:matrix: (list) matrix in [str, ...] or [[int,...], ...] or (str, ...) or ((int,...), ...)
			:random: (tuple) dimensions for matrix (dimM: int, dimN: int)
			:unity: (int) dimensions for square matrix
			
		:return: the matrix
		:rtype: object
		"""
		# call the good method to initialize object
		for attr in ('matrix', 'matrices', 'boolean', 'empty', 'nodes_edges', 'random', 'unit'):
			if attr in d:
				self._call_init(f"set_from_{attr}", **d)
				break
		
		self.isreflexive = d['reflexive'] if 'reflexive' in d else AMatrix.isreflexive

	def __add__(self, matrix: 'AMatrix') -> 'AMatrix':
		""" Return the sum of the matrix and that passed in argument
		
		:param: AMatrix matrix: matrix to be added to the instance
		:Return: :class:AMatrix
		:rtype: object
		 """
		pass
	
	def __mul__(self, matrix: 'AMatrix') -> 'AMatrix':
		""" Return the multiplication of the matrix and the one passed in argument
		
		:param: :class:`AMatrix.AMatrix` About my class AMatrix matrix: matrix to be added to the instance
		"""
		pass
	
	def __repr__(self) -> str:
		""" Return a linear representation """
		pass
	
	def __str__(self) -> str:
		""" Return a 2 dimensions representation """
		pass
	
	def _call_init(self, attr: str, **d) -> None:
		""" call method to initialize object if exists
		
		:param str attr: the name of method to call
		:param dict \*\*d: dictionary of arguments to pass
		"""
		if hasattr(self, attr):
			foo = getattr(self, attr)
			foo(**d)
		else:
			raise ValueError(f"Class '{self.__class__}' does not have the method '{attr}' for initialization")
		
	def _set_dim(self, dimM:int, dimN:int) -> None:
		""" Set properties dimensions of instance
		
		:param int dimM: number of rows
		:param int dimN: number of columns
		"""
		self.dimM = dimM
		self.dimN = dimN
	
	def get_dim(self) -> tuple:
		""" Return dimensions of matrix
		
		:returns: tuple (rows,columns)
		:rtype: tuple
		"""
		return (self.dimM, self.dimN)
	
	def set_matrix(self, matrix: list) -> None:
		""" Set content of the matrix with one given """
		pass

	def set_matrix_empty(self, dimM: int, dimN: int) -> None:
		""" Set an empty matrix with given dimensions
		
		:param int dimM: number of rows
		:param int dimN: number of columns
		"""
		pass

	def set_matrix_random(self, dimM: int, dimN: int) -> None:
		""" Set a matrix with a randomized content
		
		:param int dimM: number of rows
		:param int dimN: number of columns
		"""
		pass
	
	def set_matrix_unity(self, dim) -> None:
		""" Set an empty matrix with diagonal to 1
		
		:param int dim: number of rows and columns (square matrix)
		"""
		pass
	
	def transposed(self) -> None:
		""" Return the transpose of this matrix
		
		flips matrix over its diagonal
		"""
		pass
	
	