'''
Created on Apr 26, 2021

@author: salem Aguemoun
'''
import graphm.matrixbinary
import graphm.matrixbinaryclosure
MatrixBinary = graphm.matrixbinary.MatrixBinary
MatrixBinaryClosure = graphm.matrixbinaryclosure.MatrixBinaryClosure


class MatrixBinarySlides(MatrixBinaryClosure):
	""" Manage binary closure and intermediate matrices
	
	This class give a lot of tools to manipulate and analyse
	a graph with its transitive closure
	
	.. NOTE:: Closure can comes from MatrixBinary:
		
		:closure_matrix():
			
			:matrix: MatrixBinary: original matrix
			:matrices: MatrixBinary: intermediate matrices
			:closure: MatrixBinary closure: transitive closure
			:reflexive: bool: if matrix is reflexive
			:deep: int deep: deep rank of closure
			
		:closure_slides(): (MatrixBinary, deep, list(matrixM))
			
			:matrix: MatrixBinary: original matrix
			:matrices: list: intermediate matrices in matrixM
			:closure: MatrixBinary closure: transitive closure
			:reflexive: bool: if matrix is reflexive
			:deep: int deep: deep rank of closure
		 
	.. CAUTION:: Instance variables
	
	:var list closureM: integers rows of transitive closure
	:var list closureMS: strings rows of transitive closure
	:var list closureN:  integers columns of transitive closure
	:var list closureNS: strings columns of transitive closure
	:var int deep: max deep for transitive closure
	:var int dim: dimension of square matrix
	:var MatrixBinary matrix: original matrix come from closure
	:var bool reflexive: if True closure is reflexive
	:var list slidesM: integers rows of adjacency matrices
	:var list slidesMS: strings rows of adjacency matrices
	:var list slidesN:  integers columns of adjacency matrices
	:var list slidesNS: strings columns of adjacency matrices
	:var list unit: diagonal matrix with integers

	**Graph for the majority of examples** 
	
	.. IMAGE:: files/m.svg

	"""

	def __init__(self, d) -> 'MatrixBinarySlides':
		""" Set closure, intermediate matrices and properties
		
		:param dict d: options to specify the type of matrix
		
			with following indexes:
			
			:matrix: MatrixBinary: original matrix
			:closure: MatrixBinary: transitive closure
			:reflexive: bool: if matrix is reflexive
			
			optional indexes:
			
			:matrices: list: intermediate matrices (MatrixBinary or matrix)
			:deep: int deep: deep rank of closure
			:operations: int: number of operations
		"""
		self.set_closure_binary(**d)

	def get_deep_node_reached(self, node_start: int, node_end: int) -> int:
		""" Return the deep of shortest path between the given starting & ending nodes
		
		:param int node_start: starting node
		:param int node_end: ending node
		
		:return: the deep of shortest path or -1 if the path does not exists
		:rtype: set
		
		.. WARNING:: deep start from 0. 0 means the distance between nodes is 1

		>>> m = MatrixBinary(boolean=['01001', '00100', '01010', '00001', '01010'])
		>>> mbs = MatrixBinarySlides(m.closure_slides())
		
		>>> mbs.get_deep_node_reached(0,4)
		0
		>>> mbs.get_deep_node_reached(4,0)
		-1
		"""
		mask = 2**(self.dim - node_end - 1)
		for deep in range(self.deep):
			if self.slidesM[deep][node_start] & mask == mask:
				return deep
		return -1
		
	@staticmethod
	def get_slide_MS2NS(slide: list) -> list:
		""" Return the transpose of the slide.
		swapped slidesM and slidesN
		
		Convert rows of this matrix to columns

		:return: the transpose of the slide
		:rtype: list
		
		>>> m = MatrixBinary(boolean=['00001', '00100', '00010', '00000', '01001'])
		>>> mbs = MatrixBinarySlides(m.closure_slides())
		>>> closure = mbs.get_closure(style='str')
		
		>>> print(closure)
		['01111', '00110', '00010', '00000', '01111']
		
		>>> print(mbs.get_slide_MS2NS(closure))
		['00000', '10001', '11001', '11101', '10001']
		"""
		dim = len(slide)
		return [''.join(str(slide[m][n]) for m in range(dim)) for n in range(dim)]
	
	def set_closure_binary(self, matrix: 'MatrixBinary', closure: object, matrices: list, reflexive, deep: int=-1, **d) -> None:
		""" Set properties of this object from closure binary
		
		:param object closure: transitive closure MatrixBinary class or matrixM list
		
		>>> m = MatrixBinary(boolean=['00001', '00100', '00010', '00000', '01001'])
		
		>>> mbs = MatrixBinarySlides(m.closure_matrix())
		>>> print(mbs)
		dim=5 reflexive=False deep=4
		01111
		00110
		00010
		00000
		01111
		
		>>> mbs = MatrixBinarySlides(m.closure_slides())
		>>> print(mbs)
		dim=5 reflexive=False deep=4
		01111
		00110
		00010
		00000
		01111
		
		>>> mbs = MatrixBinarySlides(m.closure_slides(add=True))
		>>> print(mbs)
		dim=5 reflexive=True deep=4
		11111
		01110
		00110
		00010
		01111
		"""
		if not isinstance(closure, MatrixBinary):
			raise TypeError(f"Wrong type '{closure}' for closure")
		
		self.closure = closure
		self.matrix = matrix
		self.deep = deep
		self.reflexive = reflexive

		self.dim = closure.dimM
		self.closureM = closure.matrixM
		self.closureN = closure.matrixN
		self.closureMS = [self.int2str(m) for m in self.closureM]
		self.closureNS = MatrixBinarySlides.get_MS2NS(self.closureMS)
		self.unit = [2**i for i in range(self.dim - 1,  -1, -1)]

		if matrices:
			if isinstance(matrices[0], list):
				self.slidesM = matrices
			elif isinstance(matrices[0], MatrixBinary):
				self.slidesM = [m.matrixM for m in matrices]
			else:
				raise TypeError(f"Wrong type '{type(matrices)}' for matrices")
		else:
			self.slidesM = []
		self.slidesMS = [[self.int2str(m) for m in self.slidesM[i]] for i in range(self.deep)]

	def slides_MS2NS(self) -> None:
		""" Transpose matrices of all slides
		Converts slidesM & slidesMS  and set slidesN and slidesNS
		
		>>> m = MatrixBinary(boolean=['00001', '00100', '00010', '00000', '01001'])
		>>> mbs = MatrixBinarySlides(m.closure_slides())
		
		>>> print(mbs.slidesM[0])
		[1, 4, 2, 0, 9]
		>>> print(mbs.slidesMS[0])
		['00001', '00100', '00010', '00000', '01001']
		
		>>> mbs.slides_MS2NS()

		>>> print(mbs.slidesN[0])
		[0, 1, 8, 4, 17]
		>>> print(mbs.slidesNS[0])
		['00000', '00001', '01000', '00100', '10001']
		"""
		self.slidesN = []
		self.slidesNS = []
		
		for i in range(self.deep):
			sMS = self.slidesMS[i]
			self.slidesMS.append(sMS)
			
			sNS = [''.join(sMS[n][m] for n in range(self.dim)) for m in range(self.dim)]
			self.slidesNS.append(sNS)
			
			self.slidesN.append([int('0b' + m, 2) for m in sNS])


		
