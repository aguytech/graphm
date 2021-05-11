'''
Created on Apr 26, 2021

@author: salem Aguemoun
'''
import graphm.matrixbinary
MatrixBinary = graphm.matrixbinary.MatrixBinary


class MatrixBinaryClosure(object):
	""" Manage binary closure and its properties
	
	This class give a lot of tools to manipulate and analyse
	a graph with its transitive closure
	
	.. NOTE:: Closure can comes from MatrixBinary:
		
		:closure_reflexive(): 
			
			:matrix: MatrixBinary: original matrix
			:closure: MatrixBinary: transitive closure
			:reflexive: bool: if matrix is reflexive
			:deep: int deep: deep rank of closure
			
		:closure_reflexive_optimized():
			
			:matrix: MatrixBinary: original matrix
			:closure: MatrixBinary: transitive closure
			:reflexive: bool: if matrix is reflexive
			:operations: int: number of operations
			
		:closure_matrix():
			
			:matrix: MatrixBinary: original matrix
			:closure: MatrixBinary closure: transitive closure
			:reflexive: bool: if matrix is reflexive
			:deep: int deep: deep rank of closure
			
			not used:
			
			:matrices: MatrixBinary: intermediate matrices
			
		:closure_slides(): (MatrixBinary, deep, list(matrixM))
			
			:matrix: MatrixBinary: original matrix
			:closure: MatrixBinary closure: transitive closure
			:reflexive: bool: if matrix is reflexive
			:deep: int deep: deep rank of closure
			
			not used:
			
			:matrices: list: intermediate matrices in matrixM
		 
	.. CAUTION:: Instance variables
	
	:var list closureM: integers rows of transitive closure
	:var list closureMS: strings rows of transitive closure
	:var list closureN:  integers columns of transitive closure
	:var list closureNS: strings columns of transitive closure
	:var int deep: max deep for transitive closure
	:var int dim: dimension of square matrix
	:var MatrixBinary matrix: original matrix come from closure
	:var bool reflexive: if True closure is reflexive
	:var list unit: diagonal matrix with integers

	**Graph for the majority of examples** 
	
	.. IMAGE:: files/m.svg

	"""

	def __init__(self, d) -> 'MatrixBinaryClosure':
		""" Set closure and properties
		
		:param dict d: options to specify the type of matrix
		
			with following indexes:
			
			:matrix: MatrixBinary: original matrix
			:closure: MatrixBinary: transitive closure
			:reflexive: bool: if matrix is reflexive
			
			optional indexes:
			
			:deep: int deep: deep rank of closure
			:operations: int: number of operations
		"""
		self.set_closure_binary(**d)

	def __repr__(self) -> str:
		""" Return dimension, deep & reflexivity of closure
		
		:return: dimension, deep & reflexivity of closure in one line
		
		>>> m =  MatrixBinary(boolean=['010010', '001000', '010100', '010010', '000000', '000000'])

		>>> mbc = MatrixBinaryClosure(m.closure_reflexive())
		>>> repr(mbc)
		'dim=6 reflexive=True deep=3'

		>>> mbc = MatrixBinaryClosure(m.closure_slides())
		>>> repr(mbc)
		'dim=6 reflexive=False deep=3'
		"""
		return f"dim={self.dim} reflexive={self.reflexive} deep={self.deep}"
	
	def __str__(self) -> str:
		""" Return the representation of this object and the closure
		
		:return: repr() + the closure in 2 dimensions

		>>> m = MatrixBinary(boolean=['010010', '001000', '010100', '010010', '000000', '000000'])

		>>> mbc = MatrixBinaryClosure(m.closure_reflexive())
		>>> print(mbc)
		dim=6 reflexive=True deep=3
		111110
		011110
		011110
		011110
		000010
		000001

		>>> mbc = MatrixBinaryClosure(m.closure_slides())
		>>> print(mbc)
		dim=6 reflexive=False deep=3
		011110
		011110
		011110
		011110
		000000
		000000
		"""
		return self.__repr__() + "\n" + "\n".join(m for m in self.closureMS)

	def connectivity(self) -> dict:
		""" Return a report on connectivity of graph in a dictionary
		with  following indexes:
		
		:return: a report on the connectivity of graph
		:rtype: dict
		
			:graph_connected_fully: (bool) if true graph is fully connected
			:nodes_lonely: (set) lonely nodes, with no successors & ancestors
			:nodes_start: (set) starting nodes, with no ancestors
			:nodes_end: (set) ending nodes, with no successors
			:nodes_connected_not: (set) nodes not connected
			:nodes_connected: (list[set(), ..]) groups of connected nodes

		>>> m = MatrixBinary(boolean=['01001', '00100', '01010', '00001', '01010'])
		>>> mbc = MatrixBinaryClosure(m.closure_matrix())
		>>> mbc.connectivity()
		{'graph_connected_fully': False, 'nodes_lonely': set(), 'nodes_start': {0}, 'nodes_end': set(), 'nodes_connected': [{1, 2, 3, 4}], 'nodes_connected_not': {0}}
	
		>>> m = MatrixBinary(boolean=['010010', '001000', '010100', '010010', '000000', '000000'])
		>>> mbc = MatrixBinaryClosure(m.closure_matrix())
		>>> mbc.connectivity()
		{'graph_connected_fully': False, 'nodes_lonely': {5}, 'nodes_start': {0, 5}, 'nodes_end': {4, 5}, 'nodes_connected': [{1, 2, 3}], 'nodes_connected_not': {0, 4}}
		"""
		connected_fully = self.is_connected_fully()
		nodes_lonely = self.nodes_lonely()
		nodes_start = self.nodes_start()
		nodes_end = self.nodes_end()
		
		# logical 'and' between successors & ancestors
		matrix_reflexive = [self.closureM[i] & self.closureN[i] for i in range(self.dim) if i not in nodes_lonely]
		# get nodes which not have same ancestors & successors
		nodes_connected_not = {i for i in range(len(matrix_reflexive)) if matrix_reflexive[i] == 0}
		# list of connected nodes in string line format
		connected = [self.int2str(line) for line in matrix_reflexive if line != 0]
		# keep unique combinations
		connected_set = set(connected)
		# set of connected nodes
		nodes_connected = [{i for i in range(self.dim) if line[i] == '1'} for line in connected_set]
		nodes_connected = [i for i in nodes_connected if len(i) > 1]
		
		return {
			'graph_connected_fully': connected_fully,
			'nodes_lonely': nodes_lonely,
			'nodes_start': nodes_start,
			'nodes_end': nodes_end,
			'nodes_connected': nodes_connected,
			'nodes_connected_not': nodes_connected_not,
			}
	
	def get_closure(self, style='int') -> 'MatrixBinary':
		""" Return the formated matrix of transitive closure
		
		:param str style: style of export of closure
			* **int** return 0/1 integers
			* **str** Return string of '0'/'1'
			* **bin** return binary integers

		:return: the formated matrix of transitive closure
		:rtype: list
		
		>>> m =  MatrixBinary(boolean=['010010', '001000', '010100', '010010', '000000', '000000'])
		>>> mbc = MatrixBinaryClosure(m.closure_reflexive())
		
		>>> print(mbc.get_closure())
		[[1, 1, 1, 1, 1, 0], [0, 1, 1, 1, 1, 0], [0, 1, 1, 1, 1, 0], [0, 1, 1, 1, 1, 0], [0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 1]]
		
		>>> print(mbc.get_closure(style='str'))
		['111110', '011110', '011110', '011110', '000010', '000001']
		
		>>> print(mbc.get_closure(style='bin'))
		[62, 30, 30, 30, 2, 1]
		"""
		return MatrixBinary.get_matrix_formated(self.closure, style=style)
	
	@staticmethod
	def get_MS2NS(matrixXS: list) -> list:
		""" Return the transpose of the  matrixXS
		matrixXS is matrixMS or matrixNS
		
		Convert rows of this matrix to columns

		:return: the transpose matrixM
		:rtype: list
		
		>>> m = MatrixBinary(boolean=['00001', '00100', '00010', '00000', '01001'])
		>>> mbc = MatrixBinaryClosure(m.closure_slides())
		>>> closure = MatrixBinary.get_matrix_formated(mbc.closure, style='str')
		
		>>> print(closure)
		['01111', '00110', '00010', '00000', '01111']
		
		>>> print(mbc.get_MS2NS(closure))
		['00000', '10001', '11001', '11101', '10001']
		"""
		return [''.join(str(matrixXS[m][n]) for m in range(len(matrixXS))) for n in range(len(matrixXS[0]))]
	
	def int2str(self, line: int) -> str:
		""" Return the converted  boolean string from binary integer,
		string length is adjusted by to dim.
		
		dim is the dimension of line
		
		:param int line: line of boolean in integer representation
		
		:return: boolean strings
		:rtype: str

		>>> MatrixBinary.get_int2str(36, 10)
		'0000100100'
		"""
		s = bin(line)[2:]
		return s.zfill(self.dim)

	def is_connected(self) -> bool:
		""" Return true if the graph is connected
		
		at least 2 defintions:
		
			* with a reflexive closure, at least one node reaching all nodes
			* with a non reflexive closure, at least one node reaching all others nodes
			* each node are reached by at least one node which is possibly a starting node
		
		:return: true if the graph is connected
		:rtype: bool
		
		>>> m =  MatrixBinary(boolean=['010010', '001000', '010100', '010010', '000000', '000000'])
		>>> mbc = MatrixBinaryClosure(m.closure_slides())
		>>> mbc.is_connected()
		False
		
		>>> m =  MatrixBinary(boolean=['010010', '001000', '010101', '010010', '000000', '000000'])
		>>> mbc = MatrixBinaryClosure(m.closure_slides())
		>>> mbc.is_connected()
		True
		"""
		full = 2**self.dim - 1
		closureMU = MatrixBinary.get_matrixX_united(self.closureM, self.dim)
		for m in closureMU:
			if m == full:
				return True
		return False
	
	def is_connected_fully(self) -> bool:
		""" Return true if the graph is fully connected
		
		:return: true if the graph is fully connected
		:rtype: bool
		
		>>> m =  MatrixBinary(boolean=['010010', '001000', '010100', '010010', '000000', '000000'])
		>>> mbc = MatrixBinaryClosure(m.closure_reflexive())
		>>> mbc.is_connected_fully()
		False
		
		>>> m =  MatrixBinary(boolean=['010010', '001001', '010100', '010010', '000100', '100000'])
		>>> mbc = MatrixBinaryClosure(m.closure_reflexive())
		>>> mbc.is_connected_fully()
		True
		"""
		full = 2**self.dim - 1
		for m in self.closureM:
			if m != full:
				return False
		return True
	
	def is_tree(self) -> bool:
		""" Return True if the graph is a tree
		
		:return: True if the graph is a tree
		:rtype: bool
		
		>>> m =  MatrixBinary(boolean=['010010', '001000', '010100', '010010', '000000', '000000'])
		>>> mbc = MatrixBinaryClosure(m.closure_slides())
		>>> mbc.is_tree()
		False
		
		>>> m =  MatrixBinary(boolean=['010010', '001000', '000101', '000010', '000000', '000000'])
		>>> mbc = MatrixBinaryClosure(m.closure_slides())
		>>> mbc.is_tree()
		False
		
		>>> m =  MatrixBinary(boolean=['010000', '001000', '000101', '000010', '000000', '000000'])
		>>> mbc = MatrixBinaryClosure(m.closure_slides())
		>>> mbc.is_tree()
		True
		"""
		return self.is_connected() and MatrixBinary.get_edges_count(self.matrix) == (self.dim - 1)
	
	def nodes_ancestors(self, node:int) -> set:
		""" Return a set nodes that reach the given node
		
		:param int node: starting node
		
		:return: ancestors of given node
		:rtype: set

		>>> m =  MatrixBinary(boolean=['010010', '001000', '010100', '010010', '000000', '000000'])
		>>> mbc = MatrixBinaryClosure(m.closure_reflexive())
		
		>>> mbc.nodes_ancestors(4)
		{0, 1, 2, 3, 4}
		
		>>> mbc.nodes_ancestors(0)
		{0}

		>>> mbc = MatrixBinaryClosure(m.closure_slides())
		
		>>> mbc.nodes_ancestors(4)
		{0, 1, 2, 3}
		
		>>> mbc.nodes_ancestors(0)
		set()
		"""
		return {i for i in range(self.dim) if self.closureNS[node][i] == '1'}
	
	def nodes_connected(self) -> list:
		""" Return sets of connected nodes
		
		:return: sets of connected nodes
		:rtype: list
		
		>>> m = MatrixBinary(boolean=['01001', '00100', '01010', '00001', '01010'])
		>>> mbc = MatrixBinaryClosure(m.closure_matrix())
		>>> mbc.nodes_connected()
		[{1, 2, 3, 4}]
	
		>>> m = MatrixBinary(boolean=['010010', '001000', '010100', '010010', '000000', '000000'])
		>>> mbc = MatrixBinaryClosure(m.closure_matrix())
		>>> mbc.nodes_connected()
		[{1, 2, 3}]
		"""
		nodes_lonely = self.nodes_lonely()
		
		# logical 'and' between successors & ancestors
		matrix_reflexive = [self.closureM[i] & self.closureN[i] for i in range(self.dim) if i not in nodes_lonely]
		# list of connected nodes in string line format
		connected = [self.int2str(line) for line in matrix_reflexive if line != 0]
		# keep unique combinations
		connected_set = set(connected)
		# set of connected nodes
		nodes_connected = [{i for i in range(self.dim) if line[i] == '1'} for line in connected_set]
		nodes_connected = [i for i in nodes_connected if len(i) > 1]
		
		return nodes_connected
	
	def nodes_end(self) -> set:
		""" Return a set of ending nodes, with no successors
		
		:return: nodes with no successors
		:rtype: set

		>>> m =  MatrixBinary(boolean=['010010', '001000', '010100', '010010', '000000', '000000'])
		>>> mbc = MatrixBinaryClosure(m.closure_reflexive())
		>>> mbc.nodes_end()
		set()
		"""
		return {i for i in range(self.dim) if self.closureM[i] == 0}
	
	def nodes_lonely(self) -> set:
		""" Return a set of lonely nodes, with no successors & ancestors
		
		:return: nodes with no successors & ancestors
		:rtype: set

		>>> m =  MatrixBinary(boolean=['010010', '001000', '010100', '010010', '000000', '000000'])
		>>> mbc = MatrixBinaryClosure(m.closure_reflexive())
		>>> mbc.nodes_lonely()
		set()

		>>> m =  MatrixBinary(boolean=['010010', '001000', '010100', '010010', '000000', '000000'])
		>>> mbc = MatrixBinaryClosure(m.closure_slides())
		>>> mbc.nodes_lonely()
		{5}
		"""
		return self.nodes_start() & self.nodes_end()
	
	def nodes_reached_fully(self) -> set:
		""" Return a set of finally reached nodes by all, even itself
		
		.. IMPORTANT:: all, EVEN ITSELF
		
		:return: finally reached nodes by all, even itself
		:rtype: set

		>>> m =  MatrixBinary(boolean=['010010', '001000', '010100', '010010', '000000', '000000'])
		>>> mbc = MatrixBinaryClosure(m.closure_reflexive())
		>>> mbc.nodes_reached_fully()
		set()

		>>> m =  MatrixBinary(boolean=['010010', '001001', '010100', '010010', '000000', '001000'])
		>>> mbc = MatrixBinaryClosure(m.closure_reflexive())
		>>> mbc.nodes_reached_fully()
		{4}
		"""
		full = 2**self.dim - 1
		return {i for i in range(self.dim) if (self.closureN[i] == full)}
	
	def nodes_reached_fully_wow(self) -> set:
		""" Return a set of finally reached nodes by all, with or without itself 
		
		.. IMPORTANT:: all, WITH OR WITHOUT ITSELF

		:return: finally reached nodes by all, with or without itself 
		:rtype: set

		>>> m =  MatrixBinary(boolean=['010010', '001000', '010100', '010010', '000000', '000000'])
		>>> mbc = MatrixBinaryClosure(m.closure_reflexive())
		>>> mbc.nodes_reached_fully_wow()
		set()

		>>> m =  MatrixBinary(boolean=['010010', '001001', '010100', '010010', '000000', '001000'])
		>>> mbc = MatrixBinaryClosure(m.closure_reflexive())
		>>> mbc.nodes_reached_fully_wow()
		{4}
		"""
		full = 2**self.dim - 1
		return {i for i in range(self.dim) if (self.closureN[i] | self.unit[i]) == full}
	
	def nodes_reaching_all(self) -> set:
		""" Return a set of nodes finally reaching all, even itself
		
		.. IMPORTANT:: all, EVEN ITSELF
		
		:return: nodes finally reaching all, even itself
		:rtype: set

		>>> m =  MatrixBinary(boolean=['010010', '001000', '010100', '010010', '000000', '000000'])
		>>> mbc = MatrixBinaryClosure(m.closure_reflexive())
		>>> mbc.nodes_reaching_all()
		set()
		"""
		full = 2**self.dim - 1
		return {i for i in range(self.dim) if self.closureM[i] == full}
	
	def nodes_reaching_all_wow(self) -> set:
		""" Return a set of nodes finally reaching all, with or without itself
		
		.. IMPORTANT:: all, WITH OR WITHOUT ITSELF

		:return: nodes finally reaching all, with or without itself
		:rtype: set

		>>> m =  MatrixBinary(boolean=['010010', '001000', '010100', '010010', '000000', '000000'])
		>>> mbc = MatrixBinaryClosure(m.closure_reflexive())
		>>> mbc.nodes_reaching_all()
		set()
		"""
		""" Return a set of nodes reaching all, with or without itself """
		full = 2**self.dim - 1
		return {i for i in range(self.dim) if (self.closureM[i] | self.unit[i]) == full}
	
	def nodes_reflexive(self) -> set:
		"""  Return a set of finally reflexive nodes, nodes reached by themselves
		
		:return: finally reflexive nodes
		:rtype: set

		>>> m =  MatrixBinary(boolean=['010010', '001000', '010100', '010010', '000000', '000000'])
		
		>>> mbc = MatrixBinaryClosure(m.closure_reflexive())
		>>> mbc.nodes_reflexive()
		{0, 1, 2, 3, 4, 5}
		
		>>> mbc = MatrixBinaryClosure(m.closure_slides())
		>>> mbc.nodes_reflexive()
		{1, 2, 3}
		"""
		return {m for m in range(self.dim) if self.closureMS[m][m] == '1'}
	
	def nodes_start(self) -> set:
		""" Return a set of starting nodes, with no ancestors
		
		:return: nodes with no ancestors
		:rtype: set

		>>> m =  MatrixBinary(boolean=['010010', '001000', '010100', '010010', '000000', '000000'])
		>>> mbc = MatrixBinaryClosure(m.closure_reflexive())
		>>> mbc.nodes_start()
		set()

		>>> m =  MatrixBinary(boolean=['010010', '001000', '010100', '010010', '000000', '000000'])
		>>> mbc = MatrixBinaryClosure(m.closure_slides())
		>>> mbc.nodes_start()
		{0, 5}
		"""
		return {i for i in range(self.dim) if self.closureN[i] == 0}
	
	def nodes_successors(self, node: int) -> set:
		""" Return a set of nodes finally reached by the given node
		
		:param int node: ancestor of nodes returned
		
		:return: successors of given node
		:rtype: set

		>>> m =  MatrixBinary(boolean=['010010', '001000', '010100', '010010', '000000', '000000'])
		>>> mbc = MatrixBinaryClosure(m.closure_reflexive())
		>>> mbc.nodes_successors(3)
		{1, 2, 3, 4}

		>>> m =  MatrixBinary(boolean=['010010', '001000', '010100', '010010', '000000', '000000'])
		>>> mbc = MatrixBinaryClosure(m.closure_reflexive())
		>>> mbc.nodes_successors(0)
		{0, 1, 2, 3, 4}
		"""
		return {i for i in range(self.dim) if self.closureMS[node][i] == '1'}

	def paths_cycle_all(self) -> list:
		""" Return a dictionary of all paths of cycles found starting from node
		
		.. TODO:: implement the search of solutions
		
			* exclude lonely nodes
			* exclude ending nodes
			* select node which have the most successors and get cycles
			* select one node and get cycles without searching in visited nodes
			* ... until all nodes are visited
		
		.. IMPORTANT:: **Solutions : Use connectivity() to select nodes for each connected !!** 
		
		:return: paths of all cycles of graph
		:rtype: dict

			:paths_cycle: (list) all paths of cycles
			:nodes_reached: (set) all reached nodes including starting node
		"""
		# find the shortest path to complete
		
		nodes_reaching_all = self.nodes_reaching_all_wow()
		# global solution
		if nodes_reaching_all:
			node_from = nodes_reaching_all.pop()
			return {node_from: self.matrix.paths_cycle(node_from)}
		
		# solution by subsets
		raise ValueError("Needs to be implemented ;o)")
		""" TODO
		nodes_ending = self.nodes_end()
		nodes_starting = self.nodes_start()
		
		# get nodes reaching unique set of nodes and not in ending nodes
		s = set()
		nr_unique = {}
		for i in range(self.dim):
			if (self.closureM[i] not in s) and (self.closureM[i] not in nodes_ending):
				nr_unique[i] = self.closureM[i]
				s.add(self.closureM[i])
		nr_unique_count = {i: self.closureMS[i].count('1') for i in nr_unique.keys()}
		# order nodes_reaching by number of nodes reaching
		nr_sorted = sorted(nr_unique.items(), key=lambda x: nr_unique_count[x[0]])
		
		#nodes_final = 
		nodes_tmp = nr_sorted[0]
		
		nodes_reached = set()
		for node in range(self.dim):
			nr_tmp = self.nodes_successors(node)
			if nr_tmp not in nodes_reachedg:
				nodes_reaching[node] = nr_tmp
				nodes_reached.add(nr_tmp)
		#nodes_reaching = {node: self.nodes_successors(node) for node in range(self.dim)}
		
		nodes_reaching = sorted(nodes_reaching.items(), key=lambda d: len(d[1]))
		reached = False
		#while not reached:
		#	nodes
		"""
	
	def report(self) -> dict:
		""" Return a report of c properties
				
		:return: a report of matrix properties
		:rtype: dict
		
			:matrix: (list) original matrix in format 'str'
			:closure: (list) transitive closure in format 'str'

			:connected_fully: (bool) if true graph is fully connected
			:reflexive: (bool) if true graph is reflexive
			:symmetric: (bool) if true graph is symmetric
			:symmetric_pre: (bool) if True the matrix has minimal symmetry with predecessor (each edge has a back edge)
			:symmetric_suc: (bool) if True the matrix has minimal symmetry with sucessor (each back edge has a edge)
			:tree: (bool) if True the graph is a tree

			:nodes_connected: (set) groups of connected nodes
			:nodes_reached_fully: (set) nodes reached by all nodes, even itself
			:nodes_reached_fully_wow: (set) nodes reached by all others, with or without itself 
			:nodes_reaching_all: (set) nodes reaching all nodes, even itself
			:nodes_reaching_all_wow: (list[set(), ..]) nodes reaching all nodes, with or without itself 
			:nodes_start: (set) starting nodes, with no ancestors
			:nodes_end: (set) ending nodes, with no successors
			:nodes_lonely: (set) lonely nodes, with no successors & ancestors
			:nodes_reflexive: (set) reflexive nodes
			
		:return: a report of matrix properties
		:rtype: dict

		.. IMAGE:: files/m.svg

		>>> m = MatrixBinary(boolean=['010010', '001000', '010100', '010010', '000000', '000000'])
		
		>>> mbc = MatrixBinaryClosure(m.closure_slides())
		>>> print(mbc)
		dim=6 reflexive=False deep=3
		011110
		011110
		011110
		011110
		000000
		000000

		>>> print(mbc.report())
		{'symmetric': False, 'symmetric_pre': False, 'symmetric_suc': True, 'reflexive': False, 'connected_fully': False, 'nodes_reached_fully': set(), 'nodes_reached_fully_wow': set(), 'nodes_reaching_all': set(), 'nodes_reaching_all_wow': set(), 'nodes_start': {0, 5}, 'nodes_end': {4, 5}, 'nodes_lonely': {5}, 'nodes_reflexive': {1, 2, 3}, 'matrix': ['010010', '001000', '010100', '010010', '000000', '000000'], 'closure': ['011110', '011110', '011110', '011110', '000000', '000000']}

		>>> mbc = MatrixBinaryClosure(m.closure_reflexive())
		>>> print(mbc)
		dim=6 reflexive=True deep=3
		111110
		011110
		011110
		011110
		000010
		000001

		>>> print(mbc.report())
		{'symmetric': False, 'symmetric_pre': False, 'symmetric_suc': True, 'reflexive': True, 'connected_fully': False, 'nodes_reached_fully': set(), 'nodes_reached_fully_wow': set(), 'nodes_reaching_all': set(), 'nodes_reaching_all_wow': set(), 'nodes_start': set(), 'nodes_end': set(), 'nodes_lonely': set(), 'nodes_reflexive': {0, 1, 2, 3, 4, 5}, 'matrix': ['010010', '001000', '010100', '010010', '000000', '000000'], 'closure': ['111110', '011110', '011110', '011110', '000010', '000001']}
		"""
		report = {
			'symmetric': MatrixBinary.is_symmetric(self.closure),
			'symmetric_pre': MatrixBinary.is_symmetric_pre(self.closure),
			'symmetric_suc': MatrixBinary.is_symmetric_suc(self.closure),
			'reflexive': MatrixBinary.is_reflexive(self.closure),
			'connected_fully': self.is_connected_fully(),
			'nodes_reached_fully': self.nodes_reached_fully(),
			'nodes_reached_fully_wow': self.nodes_reached_fully_wow(),
			'nodes_reaching_all': self.nodes_reaching_all(),
			'nodes_reaching_all_wow': self.nodes_reaching_all_wow(),
			'nodes_start': self.nodes_start(),
			'nodes_end': self.nodes_end(),
			'nodes_lonely': self.nodes_lonely(),
			'nodes_reflexive': self.nodes_reflexive(),
			}
		
		report['matrix'] = MatrixBinary.get_matrix_formated(self.matrix, style='str')
		report['closure'] = MatrixBinary.get_matrix_formated(self.closure, style='str')
			
		return report

	def set_closure_binary(self, matrix: 'MatrixBinary', closure: object, reflexive, deep: int=-1, **d) -> None:
		""" Set properties of this object from closure binary
		
		:param object closure: transitive closure MatrixBinary class or matrixM list
		
		>>> m = MatrixBinary(boolean=['00001', '00100', '00010', '00000', '01001'])
		>>> mbc = MatrixBinaryClosure(m.closure_reflexive())
		>>> print(mbc)
		dim=5 reflexive=True deep=4
		11111
		01110
		00110
		00010
		01111
		
		>>> m = MatrixBinary(boolean=['00001', '00100', '00010', '00000', '01001'])
		>>> mbc = MatrixBinaryClosure(m.closure_reflexive_optimized())
		>>> print(mbc)
		dim=5 reflexive=True deep=-1
		11111
		01110
		00110
		00010
		01111
		
		>>> m = MatrixBinary(boolean=['00001', '00100', '00010', '00000', '01001'])
		>>> mbc = MatrixBinaryClosure(m.closure_matrix())
		>>> print(mbc)
		dim=5 reflexive=False deep=4
		01111
		00110
		00010
		00000
		01111
		
		>>> m = MatrixBinary(boolean=['00001', '00100', '00010', '00000', '01001'])
		>>> mbc = MatrixBinaryClosure(m.closure_slides())
		>>> print(mbc)
		dim=5 reflexive=False deep=4
		01111
		00110
		00010
		00000
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
		self.closureNS = MatrixBinaryClosure.get_MS2NS(self.closureMS)
		self.unit = [2**i for i in range(self.dim - 1,  -1, -1)]

	def str_report(self) -> str:
		""" Return a string of report() content
		
			See MatrixBinaryClosure.report()
		
		>>> m = MatrixBinary(boolean=['010010', '001000', '010100', '010010', '000000', '000000'])
		>>> mbc = MatrixBinaryClosure(m.closure_slides())
		>>> print(mbc.str_report())
		matrix: ['010010', '001000', '010100', '010010', '000000', '000000']
		closure: ['011110', '011110', '011110', '011110', '000000', '000000']
		fully connected         False
		nodes ending            {4, 5}
		nodes lonely            {5}
		nodes fully reached     set()
		fully reached wow       set()
		nodes reaching all      set()
		nodes reaching all wow  set()
		nodes reflexive         {1, 2, 3}
		nodes starting          {0, 5}
		reflexive               False
		symmetric               False
		symmetry predecessor    False
		symmetry successor      True
		"""
		trans = {
		'symmetric': 'symmetric              ',
		'symmetric_pre': 'symmetry predecessor   ',
		'symmetric_suc': 'symmetry successor     ',
		'reflexive': 'reflexive              ',
		'connected_fully': 'fully connected        ',
		'nodes_reached_fully': 'nodes fully reached    ',
		'nodes_reached_fully_wow': 'fully reached wow      ',
		'nodes_reaching_all': 'nodes reaching all     ',
		'nodes_reaching_all_wow': 'nodes reaching all wow ',
		'nodes_start': 'nodes starting         ',
		'nodes_end': 'nodes ending           ',
		'nodes_lonely': 'nodes lonely           ',
		'nodes_reflexive': 'nodes reflexive        ',
		}
		
		data = self.report()
		report = f"matrix: {data.pop('matrix')}"
		report += f"\nclosure: {data.pop('closure')}"
		
		data = sorted(data.items())
		for k, v in data:
			report += f"\n{trans[k]} {v}"
		
		return report

	def str2int(self, line: str) -> int:
		""" Return the converted binary integer from boolean string,
		
		:param int line: line of boolean in integer representation
		
		:return: boolean strings
		:rtype: str

		>>> MatrixBinary.get_int2str(36, 10)
		'0000100100'
		"""
		""" Convert string to binary
		line str / line of matrix
		"""
		return int("0b" + line, 2)

	
	
