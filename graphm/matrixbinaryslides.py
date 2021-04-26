'''
Created on Apr 26, 2021

@author: salem Aguemoun
'''
# for doctest
if __name__ == "matrixbinaryslides" :
	from graphm import MatrixBinary

class MatrixBinarySlides(object):
	""" Manage slides of binary matrices with closure
	
	This class give a lot of tools to manipulate and analyse
	a graph with its transitive closure and sildes
	
	.. NOTE:: Closure comes from MatrixBinary.get_closure_slides()...
	
	.. CAUTION:: Instance variables
	
	:var list closureM: integers rows of transitive closure
	:var list closureMS: strings rows of transitive closure
	:var list closureN:  integers columns of transitive closure
	:var list closureNS: strings columns of transitive closure
	:var int deep: max deep for transitive closure, slides number
	:var int dim: dimension of square matrix
	:var list slidesM: integers rows of adjacency matrices
	:var list slidesMS: strings rows of adjacency matrices
	:var list slidesN:  integers columns of adjacency matrices
	:var list slidesNS: strings columns of adjacency matrices
	:var list successors: list of successors of nodes
	:var list successorsE: list of successors of nodes without nodes itself 
	:var list unity: diagonal matrix with integers

	**Graph for the majority of examples** 
	
	.. IMAGE:: files/mbs.png

	"""

	def __init__(self, slides) -> 'MatrixBinarySlides':
		""" Set properties from slides and the number of columns of matrices
		
		:param list slides: transitive closure with the intermediate adjacency matrices (matrixN)
		
		:rtype: MatrixBinarySlides
		"""
		if not slides:
			raise ValueError("The slides are empty")
		self.set_slides_binary(slides)

	def __repr__(self) -> str:
		""" Return dimension and deep of matrices
		
		:return: dimension and deep of matrices in one line
		
		>>> m = MatrixBinary(boolean=['01001', '00100', '01010', '00001', '01010'])
		>>> mbs = MatrixBinarySlides(m.get_closure_slides())
		
		>>> repr(mbs)
		'dim=5 deep=3'
		"""
		return f"dim={self.dim} deep={self.deep}"
	
	def __str__(self) -> str:
		""" Return the representation of this object and the closure
		
		:return: repr() + the closure in 2 dimensions

		>>> m =MatrixBinary(boolean=['01001', '00100', '01010', '00001', '01010'])
		>>> mbs = MatrixBinarySlides(m.get_closure_slides())
		
		>>> print(mbs)
		dim=5 deep=3
		01111
		01111
		01111
		01111
		01111
		"""
		return self.__repr__() + "\n" + "\n".join(m for m in self.closureMS)

	def add_unity(self, slides: list) -> list:
		""" Return given slides added of the unity matrix
		
		:param list slides: list of adjacency matrices
		
		:return: slides added of unity matrix
		:rtype: list
		
		"""
		return [self.unity[i] | slides[i] for i in range(self.dim) ]
		
	def get_closure(self, style="int") -> list:
		""" Return the matrix of transitive closure
		
		:param str style: style of export of closure
			* **int** return 0/1 integers
			* **str** Return string of '0'/'1'
			* **bin** return binary integers

		:return: the transitive closure in given style 
		:rtype: list
		
		>>> m = MatrixBinary(boolean=['01001', '00100', '01010', '00001', '01010'])
		>>> mbs = MatrixBinarySlides(m.get_closure_slides())
		
		>>> print(mbs.get_closure())
		[[0, 1, 1, 1, 1], [0, 1, 1, 1, 1], [0, 1, 1, 1, 1], [0, 1, 1, 1, 1], [0, 1, 1, 1, 1]]
		"""
		return self.get_matrix(-1, style)
	
	def get_connectivity(self) -> dict:
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
		>>> mbs = MatrixBinarySlides(m.get_closure_slides())
		
		>>> print(mbs.get_connectivity())
		{'graph_connected_fully': False, 'nodes_lonely': set(), 'nodes_start': {0}, 'nodes_end': set(), 'nodes_connected_not': {0}, 'nodes_connected': [{1, 2, 3, 4}]}
		"""
		graph_connected_fully = self.is_connected_fully()
		nodes_lonely = self.get_nodes_lonely()
		nodes_start = self.get_nodes_start()
		nodes_end = self.get_nodes_end()
		
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
		
		return {
			'graph_connected_fully': graph_connected_fully,
			'nodes_lonely': nodes_lonely,
			'nodes_start': nodes_start,
			'nodes_end': nodes_end,
			'nodes_connected_not': nodes_connected_not,
			'nodes_connected': nodes_connected,
			}
	
	def get_deep_node_reached(self, node_start: int, node_end: int) -> int:
		""" Return the deep of shortest path between the given starting & ending nodes
		
		:param int node_start: starting node
		:param int node_end: ending node
		
		:return: the deep of shortest path or -1 if the path does not exists
		:rtype: set
		
		.. WARNING:: deep start from 0. 0 means the distance between nodes is 1

		>>> m = MatrixBinary(boolean=['01001', '00100', '01010', '00001', '01010'])
		>>> mbs = MatrixBinarySlides(m.get_closure_slides())
		
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
		
	def get_matrix(self, index: int, style="int") -> list:
		""" Return the matrix of transitive closure in given index
		
		:param str style: style of export of closure
			* **int** return 0/1 integers
			* **str** Return string of '0'/'1'
			* **bin** return binary integers

		:return: the transitive closure in given style 
		:rtype: list
		
		>>> m = MatrixBinary(boolean=['01001', '00100', '01010', '00001', '01010'])
		>>> mbs = MatrixBinarySlides(m.get_closure_slides())
		
		>>> print(mbs.get_matrix(1))
		[[0, 1, 1, 1, 0], [0, 1, 0, 1, 0], [0, 0, 1, 0, 1], [0, 1, 0, 1, 0], [0, 0, 1, 0, 1]]
		
		>>> print(mbs.get_matrix(1, style='str'))
		['01110', '01010', '00101', '01010', '00101']
		
		>>> print(mbs.get_matrix(1, style='bin'))
		[14, 10, 5, 10, 5]
		"""
		if index >= self.dim:
			raise ValueError("Wrong dimension. more than {self.dim}")
		
		slide = self.slidesM[index] if index > -1 else self.closureM
		if style == "int":
			return [[int(i) for i in self.int2str(m)]for m in slide]
		elif style == "str":
			return [self.int2str(m) for m in slide]
		elif style == "bin":
			return slide[:]
	
	def get_nodes_ancestors(self, node:int) -> set:
		""" Return a set nodes that reach the given node
		
		:param int node: starting node
		
		:return: ancestors of given node
		:rtype: set

		>>> m = MatrixBinary(boolean=['01001', '00100', '01010', '00001', '01010'])
		>>> mbs = MatrixBinarySlides(m.get_closure_slides())
		
		>>> mbs.get_nodes_ancestors(4)
		{0, 1, 2, 3, 4}
		
		>>> mbs.get_nodes_ancestors(0)
		set()
		"""
		return {i for i in range(self.dim) if self.closureNS[node][i] == '1'}
	
	def get_nodes_end(self) -> set:
		""" Return a set of ending nodes, with no successors
		
		:return: nodes with no successors
		:rtype: set

		>>> m = MatrixBinary(boolean=['01001', '00100', '01010', '00001', '01010'])
		>>> mbs = MatrixBinarySlides(m.get_closure_slides())
		>>> mbs.get_nodes_end()
		set()
		"""
		return {i for i in range(self.dim) if self.closureM[i] == 0}
	
	def get_nodes_lonely(self) -> set:
		""" Return a set of lonely nodes, with no successors & ancestors
		
		:return: nodes with no successors & ancestors
		:rtype: set

		>>> m = MatrixBinary(boolean=['01001', '00100', '01010', '00001', '01010'])
		>>> mbs = MatrixBinarySlides(m.get_closure_slides())
		>>> mbs.get_nodes_lonely()
		set()
		"""
		return self.get_nodes_start() & self.get_nodes_end()
	
	def get_nodes_reached_fully(self) -> set:
		""" Return a set of finally reached nodes by all, even itself
		
		.. IMPORTANT:: all, EVEN ITSELF
		
		:return: finally reached nodes by all, even itself
		:rtype: set

		>>> m = MatrixBinary(boolean=['01001', '00100', '01010', '00001', '01010'])
		>>> mbs = MatrixBinarySlides(m.get_closure_slides())
		>>> mbs.get_nodes_reached_fully()
		{1, 2, 3, 4}
		"""
		full = 2**self.dim - 1
		return {i for i in range(self.dim) if (self.closureN[i] == full)}
	
	def get_nodes_reached_fully_wow(self) -> set:
		""" Return a set of finally reached nodes by all, with or without itself 
		
		.. IMPORTANT:: all, WITH OR WITHOUT ITSELF

		:return: finally reached nodes by all, with or without itself 
		:rtype: set

		>>> m = MatrixBinary(boolean=['01001', '00100', '01010', '00001', '01010'])
		>>> mbs = MatrixBinarySlides(m.get_closure_slides())
		>>> mbs.get_nodes_reached_fully_wow()
		{1, 2, 3, 4}
		"""
		full = 2**self.dim - 1
		return {i for i in range(self.dim) if (self.closureN[i] | self.unity[i]) == full}
	
	def get_nodes_reaching_all(self) -> set:
		""" Return a set of nodes finally reaching all, even itself
		
		.. IMPORTANT:: all, EVEN ITSELF
		
		:return: nodes finally reaching all, even itself
		:rtype: set

		>>> m = MatrixBinary(boolean=['01001', '00100', '01010', '00001', '01010'])
		>>> mbs = MatrixBinarySlides(m.get_closure_slides())
		>>> mbs.get_nodes_reaching_all()
		set()
		"""
		full = 2**self.dim - 1
		return {i for i in range(self.dim) if self.closureM[i] == full}
	
	def get_nodes_reaching_all_wow(self) -> set:
		""" Return a set of nodes finally reaching all, with or without itself
		
		.. IMPORTANT:: all, WITH OR WITHOUT ITSELF

		:return: nodes finally reaching all, with or without itself
		:rtype: set

		>>> m = MatrixBinary(boolean=['01001', '00100', '01010', '00001', '01010'])
		>>> mbs = MatrixBinarySlides(m.get_closure_slides())
		>>> mbs.get_nodes_reaching_all()
		set()
		"""
		""" Return a set of nodes reaching all, with or without itself """
		full = 2**self.dim - 1
		return {i for i in range(self.dim) if (self.closureM[i] | self.unity[i]) == full}
	
	def get_nodes_reflexive(self) -> set:
		"""  Return a set of finally reflexive nodes, nodes reached by themselves
		
		:return: finally reflexive nodes
		:rtype: set

		>>> m = MatrixBinary(boolean=['01001', '00100', '01010', '00001', '01010'])
		>>> mbs = MatrixBinarySlides(m.get_closure_slides())
		>>> mbs.get_nodes_reflexive()
		{1, 2, 3, 4}
		"""
		return {m for m in range(self.dim) if self.closureMS[m][m] == '1'}
	
	def get_nodes_start(self) -> set:
		""" Return a set of starting nodes, with no ancestors
		
		:return: nodes with no ancestors
		:rtype: set

		>>> m = MatrixBinary(boolean=['01001', '00100', '01010', '00001', '01010'])
		>>> mbs = MatrixBinarySlides(m.get_closure_slides())
		>>> mbs.get_nodes_start()
		{0}
		"""
		return {i for i in range(self.dim) if self.closureN[i] == 0}
	
	def get_nodes_successors(self, node:int) -> set:
		""" Return a set of nodes finally reached by the given node
		
		:param int node: ancestor of nodes returned
		
		:return: successors of given node
		:rtype: set

		>>> m = MatrixBinary(boolean=['01001', '00100', '01010', '00001', '01010'])
		>>> mbs = MatrixBinarySlides(m.get_closure_slides())
		>>> mbs.get_nodes_successors(4)
		{1, 2, 3, 4}
		"""
		return {i for i in range(self.dim) if self.closureMS[node][i] == '1'}

	def get_paths_cycle(self, node_start:int, shortest:bool=False) -> dict:
		""" Return a dictionary of paths of cycles found starting from node
		
		.. IMPORTANT:: by default returns all cycles presents in graph
			To have  only found cycles until the transitive closure are reached,
			put 'shortest' option to True
		
		:param int node_start: the starting node to search paths
		:param bool shortest=False: if true limits paths to shortest ones, default is False

		:return: paths of cycles
		:rtype: dict

			:paths_cycle: (list) all paths of cycles
			:nodes_reached: (set) all reached nodes including starting node

		>>> m = MatrixBinary(boolean=['00001', '00100', '00010', '00000', '01001'])
		>>> mbs = MatrixBinarySlides(m.get_closure_slides())
		>>> mbs.get_paths_cycle(4)
		{'paths_cycle': [], 'nodes_reached': {1, 2, 3, 4}}
		
		>>> m =MatrixBinary(boolean=['01001', '00100', '01010', '00001', '01010'])
		>>> mbs = MatrixBinarySlides(m.get_closure_slides())
		>>> mbs.get_paths_cycle(4)
		{'paths_cycle': [[4, 3], [1, 2], [4, 1, 2, 3]], 'nodes_reached': {1, 2, 3, 4}}
		"""
		nodes_reached = {node_start}
		paths_cycle = []
		paths_cycle_set = set()
		paths = [[node_start]]
		deep_final = self.deep if shortest else self.dim

		# no successors with or without itself
		if (self.closureM[node_start] == 0) or (self.closureM[node_start] ^ 2**(self.dim - node_start - 1) == 0):
			paths = []
		
		deep = 0
		while deep < deep_final and paths:
			paths_tmp = paths
			paths = []
			for path in paths_tmp:
				successors = self.successorsE[path[deep]]
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
			'paths_cycle': paths_cycle,
			'nodes_reached': nodes_reached,
			}
	
	def get_paths_cycle_all(self) -> list:
		""" Return a dictionary of all paths of cycles found starting from node
		
		.. TODO:: implement the search of solutions
		
			* exclude lonely nodes
			* exclude ending nodes
			* select node which have the most successors and get cycles
			* select one node and get cycles without searching in visited nodes
			* ... until all nodes are visited
		
		.. IMPORTANT:: **Solutions : Use get_connectivity() to select nodes for each connected !!** 
		
		:return: paths of all cycles of graph
		:rtype: dict

			:paths_cycle: (list) all paths of cycles
			:nodes_reached: (set) all reached nodes including starting node
		"""
		# find the shortest path to complete
		
		nodes_reaching_all = self.get_nodes_reaching_all_wow()
		# global solution
		if nodes_reaching_all:
			node_from = nodes_reaching_all.pop()
			return {node_from: self.get_paths_cycle(node_from)}
		
		# solution by subsets
		raise ValueError("Needs to be implemented ;o)")
		""" TODO
		nodes_ending = self.get_nodes_end()
		nodes_starting = self.get_nodes_start()
		
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
		
		nr_unique = set(self.slidesN(i) for i in range(self.dim))
		
		nodes_reached = set()
		for node in range(self.dim):
			nr_tmp = self.get_nodes_successors(node)
			if nr_tmp not in nodes_reachedg:
				nodes_reaching[node] = nr_tmp
				nodes_reached.add(nr_tmp)
		#nodes_reaching = {node: self.get_nodes_successors(node) for node in range(self.dim)}
		
		nodes_reaching = sorted(nodes_reaching.items(), key=lambda d: len(d[1]))
		reached = False
		#while not reached:
		#	nodes
		"""
	
	def get_paths_from(self, node_start:int, shortest:bool=False) -> dict:
		""" Return a dictionary of all paths starting from node
		
		.. IMPORTANT:: by default returns all paths presents in the graph
			To have  only found cycles until the transitive closure are reached,
			put 'shortest' option to True
		
		:param int node_start: the starting node to search paths
		:param bool shortest=False: if true limits paths to shortest ones, default is False

		:return: paths
		:rtype: dict

			:paths_final: (list) all paths which access to maximal deep
			:paths_ended: (list) all paths which deep less than maximal one
			:paths_cycle: (list) all paths of elementary cycles
			:nodes_reached: (set) all reached nodes including starting node

		>>> m =MatrixBinary(boolean=['01001', '00100', '01010', '00001', '01010'])
		>>> mbs = MatrixBinarySlides(m.get_closure_slides())
		>>> mbs.get_paths_from(1)
		{'paths_final': [], 'paths_ended': [], 'paths_cycle': [[1, 2], [1, 2, 3, 4], [3, 4]], 'nodes_reached': {1, 2, 3, 4}}
		
		>>> mbs.get_paths_from(4)
		{'paths_final': [], 'paths_ended': [], 'paths_cycle': [[4, 3], [1, 2], [4, 1, 2, 3]], 'nodes_reached': {1, 2, 3, 4}}
		"""
		nodes_reached = {node_start}
		paths_ended = []
		paths_cycle = []
		paths_cycle_set = set()
		paths = [[node_start]]
		deep_final = self.deep if shortest else self.dim

		# no successors with or without itself
		if (self.closureM[node_start] == 0) or (self.closureM[node_start] ^ 2**(self.dim - node_start - 1) == 0):
			paths = []
		
		deep = 0
		while deep < deep_final and paths:
			paths_tmp = paths
			paths = []
			for path in paths_tmp:
				successors = self.successorsE[path[deep]]
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
			'paths_final': paths,
			'paths_ended': paths_ended,
			'paths_cycle': paths_cycle,
			'nodes_reached': nodes_reached,
			}
	
	def get_paths_from_to(self, node_start: int, node_end: int, shortest:bool=True) -> list:
		""" Return a dictionary of all paths starting from node 'node_start' to 'node_end'
		
		.. IMPORTANT:: by default returns all paths presents in the graph
			To have  only found cycles until the transitive closure are reached,
			put 'shortest' option to True
		
		:param int node_start: the starting node
		:param int node_end: the ending node
		:param bool shortest=False: if true limits paths to shortest ones, default is False

		:return: paths
		:rtype: dict

			:count: (int) iterations count 
			:nodes_reached: (set) all reached nodes including starting node
			:paths_final: (list) all paths which access to maximal deep
			:reached: (bool) True if node_end is reached by node_start

		>>> m =MatrixBinary(boolean=['01001', '00100', '01010', '00001', '01010'])
		>>> mbs = MatrixBinarySlides(m.get_closure_slides())
		
		>>> mbs.get_paths_from(3,2)
		{'paths_final': [[3, 4, 1, 2]], 'paths_ended': [], 'paths_cycle': [[3, 4]], 'nodes_reached': {1, 2, 3, 4}}
	
		>>> mbs.get_paths_from(0,2)
		{'paths_final': [[0, 1, 2, 3], [0, 4, 1, 2]], 'paths_ended': [], 'paths_cycle': [[1, 2], [4, 3]], 'nodes_reached': {0, 1, 2, 3, 4}}
		"""
		count = 1
		reached = False
		nodes_reached = {node_start}
		paths = [[node_start]]
		paths_final = []
		deep_final = self.deep if shortest else self.dim # for security

		# no successors with or without itself
		if self.closureMS[node_start][node_end] == '0':
			paths = []
		
		deep = 0
		while (not shortest or (not reached and shortest)) and paths and deep < deep_final:
			paths_tmp = paths
			paths = []
			for path in paths_tmp:
				successors = self.successorsE[path[deep]]
				for node in successors:
					count += 1
					if node == node_end:
						paths_final.append(path + [node])
						reached = True
					else:
						if node not in path:
							nodes_reached.add(node)
							paths.append(path + [node])
				# clean paths if reached
			deep += 1
			
		return {
			'count': count,
			'nodes_reached': nodes_reached,
			'paths_final': paths_final,
			'reached': reached,
			}
	
	def get_report(self, matrix:bool=False, closure:bool=False) -> dict:
		""" Return a report of matrix properties
				
		:param bool matrix: if True Return matrix content
		:param bool closure: if True Return closure content

		:return: a report of matrix properties
		:rtype: dict
		
			:matrix: (list) optional original matrix in format 'str'
			:closure: (list) optional transitive closure in format 'str'

			:reflexive_fully: (bool) if true graph is fully reflexive
			:connected_fully: (bool) if true graph is fully connected
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

		.. IMAGE:: files/mbs.png

		>>> m =MatrixBinary(boolean=['01001', '00100', '01010', '00001', '01010'])
		>>> mbs = MatrixBinarySlides(m.get_closure_slides())
		
		>>> print(mbs)
		dim=5 deep=3
		01111
		01111
		01111
		01111
		01111

		>>> print(mbs.get_report())
		{'reflexive_fully': {1, 2, 3, 4}, 'connected_fully': False, 'nodes_reached_fully': {1, 2, 3, 4}, 'nodes_reached_fully_wow': {1, 2, 3, 4}, 'nodes_reaching_all': set(), 'nodes_reaching_all_wow': {0}, 'nodes_start': {0}, 'nodes_end': set(), 'nodes_lonely': set(), 'nodes_reflexive': False}
		"""
		d = {
			'reflexive_fully': self.is_reflexive(),
			'connected_fully': self.is_connected_fully(),
			'nodes_reached_fully': self.get_nodes_reached_fully(),
			'nodes_reached_fully_wow': self.get_nodes_reached_fully_wow(),
			'nodes_reaching_all': self.get_nodes_reaching_all(),
			'nodes_reaching_all_wow': self.get_nodes_reaching_all_wow(),
			'nodes_start': self.get_nodes_start(),
			'nodes_end': self.get_nodes_end(),
			'nodes_lonely': self.get_nodes_lonely(),
			'nodes_reflexive': self.is_reflexive(),
			'reflexive_fully': self.get_nodes_reflexive(),
			}
		
		if matrix:
			d['matrix'] = self.get_matrix(style='str')
		if closure:
			d['matrix'] = self.get_closure(style='str')
			
		return d

	def get_slide_MS2NS(self,slide: list) -> list:
		""" Return the transpose of the slide.
		swapped slidesM and slidesN
		
		Convert rows of this matrix to columns

		:return: the transpose of the slide
		:rtype: list
		
		>>> m = MatrixBinary(boolean=['00001', '00100', '00010', '00000', '01001'])
		>>> mbs = MatrixBinarySlides(m.get_closure_slides())
		>>> closure = mbs.get_closure(style='str')
		
		>>> print(closure)
		['01111', '00110', '00010', '00000', '01111']
		
		>>> print(mbs.get_slide_MS2NS(closure))
		['00000', '10001', '11001', '11101', '10001']
		"""
		return [''.join(str(slide[m][n]) for m in range(self.dim)) for n in range(self.dim)]
	
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

	def is_connected_fully(self) -> bool:
		""" Return true if the graph is fully connected
		
		:return: true if the graph is fully connected
		:rtype: bool
		
		>>> m = MatrixBinary(boolean=['01001', '00100', '01010', '00001', '01010'])
		>>> mbs = MatrixBinarySlides(m.get_closure_slides())
		
		>>> mbs. is_connected_fully()
		False
		"""
		full = 2**self.dim - 1
		for m in self.closureM:
			if m != full:
				return False
		return True
	
	def is_reflexive(self) -> bool:
		""" Return true if the graph is reflexive,
		at least one return for each way
		
		.. IMPORTANT:: return True if each edge has at least one edge back
		
		:return: true if the graph is reflexive
		:rtype: bool
		
		>>> m = MatrixBinary(boolean=['01001', '00100', '01010', '00001', '01010'])
		>>> mbs = MatrixBinarySlides(m.get_closure_slides())
		>>> mbs. is_reflexive()
		False

		>>> m = MatrixBinary(boolean=['01001', '00100', '01010', '00001', '10010'])
		>>> mbs = MatrixBinarySlides(m.get_closure_slides())
		>>> mbs. is_reflexive()
		True
		"""
		for i in range(self.dim):
			if self.closureM[i] & self.closureN[i]  != self.closureM[i]:
				return False
		return True
	
	def is_reflexive_fully(self) -> bool:
		""" Return true if the graph is fully reflexive

		.. IMPORTANT:: return True the graph is fully reflexive

		:return: true if the graph is fully reflexive
		:rtype: bool
		
		>>> m = MatrixBinary(boolean=['01001', '00100', '01010', '00001', '01010'])
		>>> mbs = MatrixBinarySlides(m.get_closure_slides())
		>>> mbs. is_reflexive_fully()
		False

		>>> m = MatrixBinary(boolean=['01001', '00100', '01010', '00001', '10010'])
		>>> mbs = MatrixBinarySlides(m.get_closure_slides())
		>>> mbs. is_reflexive_fully()
		True
		"""
		for i in range(self.dim):
			if self.closureM[i] != self.closureN[i]:
				return False
		return True
	
	def set_slides_binary(self, slides: list) -> None:
		""" Set properties of this object from given slides
		
		slides come from Matrix Binary.get closure slides() and derivatives
		
		.. NOTE:: the first items in slides is the transitive closure
		
		:param list slides: transitive closure with the intermediate adjacency matrices (matrixN)
		
		>>> m = MatrixBinary(boolean=['00001', '00100', '00010', '00000', '01001'])
		>>> mbs = MatrixBinarySlides(m.get_closure_slides())
		>>> print(mbs)
		dim=5 deep=4
		01111
		00110
		00010
		00000
		01111
		"""
		if len(slides) < 2:
			raise ValueError("Need minimum length equals to 2")
		
		self.dim = len(slides[0])
		
		# closure
		self.closureM = slides.pop(0)
		self.closureMS = [self.int2str(m) for m in self.closureM]
		self.closureNS = self.get_slide_MS2NS(self.closureMS)
		self.closureN = [self.str2int(n) for n in self.closureNS]
		
		self.deep = len(slides)
		self.unity = [2**i for i in range(self.dim - 1,  -1, -1)]
		
		self.slidesM = slides
		self.slidesMS = [[self.int2str(m) for m in self.slidesM[i]] for i in range(self.deep)]

		# converts all slides
		#self.slides_MS2NS()

		self.successors = {m: [n for n in range(self.dim) if self.slidesMS[0][m][n] == '1'] for m in range(self.dim)}
		self.successorsE = {m: [n for n in range(self.dim) if self.slidesMS[0][m][n] == '1' and m != n] for m in range(self.dim)}
		
	def slides_MS2NS(self) -> None:
		""" Transpose matrices of all slides
		Converts slidesM & slidesMS  and set slidesN and slidesNS
		
		>>> m = MatrixBinary(boolean=['00001', '00100', '00010', '00000', '01001'])
		>>> mbs = MatrixBinarySlides(m.get_closure_slides())
		
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

	def str_report(self, matrix:bool=False, closure:bool=False) -> str:
		""" Return a string of report of matrix properties
		
		- matrix: bool / if True Return matrix content
		- closure: bool / if True Return closure content
		"""
		report = ''
		if matrix:
			report += f"{self.get_matrix(style='str')}"
		if closure:
			report += f"{self.get_matrix(style='str')}"
		report += f"reflexive\t\t\t\t\t {self.is_reflexive()}" \
			+ f"\nfully reflexive\t\t\t\t {self.is_reflexive_fully()}" \
			+ f"\nfully connected\t\t\t\t {self.is_connected_fully()}" \
			+ f"\nnodes fully reached\t\t {self.get_nodes_reached_fully()}" \
			+ f"\nnodes fully reached wow\t {self.get_nodes_reached_fully_wow()}" \
			+ f"\nnodes reaching all\t\t\t {self.get_nodes_reaching_all()}" \
			+ f"\nnodes reaching all wow\t\t {self.get_nodes_reaching_all_wow()}" \
			+ f"\nnodes starting\t\t\t {self.get_nodes_start()}" \
			+ f"\nnodes ending\t\t\t\t {self.get_nodes_end()}" \
			+ f"\nnodes lonely\t\t\t\t {self.get_nodes_lonely()}" \
			+ f"\nnodes reflexive\t\t\t {self.get_nodes_reflexive()}" \
			#+ f"reflexive\t\t: {self.is_reflexive()}" \
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

	
	
