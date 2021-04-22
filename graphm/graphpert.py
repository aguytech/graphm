import functools
from graphm import Graph


class GraphPert(Graph):
	""" Manage Pert graph.
	
	Data is directly stored in :class:`pygraphviz.Agraph`

	Drawing is supported by writing file in 'dot' format 
	(others available layouts are :class:`GraphM.layout`)
	
	:var str node_start: default character for starting node
	
		**>**
	
	:var str node_end: default character for ending node
	
		**<**
	
	:var str color_critical: default color for drawing critical path of the Pert graph
	
		**red** / for others colors see `<https://graphviz.org/doc/info/colors.html>`_
	
	:var dict layout: default attributes for graph layout, see :class:`pygraphviz.Agraph`
	
		:prog: (str) type of programmed layout
			
			**dot** / neato, dot, twopi, circo, fdp, nop

	:var dict graph_attr: default attributes for graph, see :class:`pygraphviz.Agraph`
	
		:colorscheme: (str) default "" / color scheme to interpret colors
		
			| X11, SVG, Brewer. see `<https://graphviz.org/doc/info/colors.html>`_
			
		:directed: (bool) directed graph or not
		:label: (str) label printed in the graph
		:rankdir: (str) orientation for dot graph
		:ranksep: (str) distance between nodes
		:strict: (bool) mode for dot graph
	
	:var dict node_attr: default attributgetattr(self, attr)es for nodes, see :class:`pygraphviz.Agraph`
	
		:color: (str) font color of nodes
		:fontcolor: (str) font color of nodes
		:fontname: (str) font name of nodes
		:shape: (str) shape of nodes
		
	:var dict edge_attr: default attributes for edges, see :class:`pygraphviz.Agraph`
	
		:color: (str) font color of edges
		:fontcolor: (str) font color of edges
		:fontname: (str) font name of edges
		
	.. NOTE:: For inherited class variables see :class:`graphm.graph.Graph`
		
	.. CAUTION:: Instance variables
	
	:var pygraphviz.AGraph viz: manage drawing in dot format with :class:`pygraphviz.AGraph`

	:var dict layout: graph layout, see :class:`GraphPert.layout`

	**Graph for the majority of examples** 
	
	.. IMAGE:: files/graph_draw2.png
	
	"""
	node_start = '>'
	node_end = '<'
	sep = ','
	color_critical = 'red'
	layout = {
		'prog' : 'dot',
		}
	graph_attr = {
		'label' : 'G',
		'directed' : True,
		'rankdir' : "TB",
		'ranksep' : "0.5",
		'strict' : False,
		}
	node_attr = {
		'color' : 'chocolate4',
		'fontcolor' : 'chocolate4',
		'fontname' : 'Arial',
		'shape' : 'circle',
		}
	edge_attr = {
		'color' : 'gray30',
		'fontcolor' : 'gray30',
		'fontname' : 'Arial',
		}
	
	def add_node_value(self, node_from: str, node: int, way: str, index: int=-1) -> None:
		# index, value_down, value_back
		
		value_from = self.edges_value[node_from]
		value = self.edges_value[node]
		
		# down
		if way == 'down':
			if index < 0:
				raise ValueError("Need an index to add the value in downing way")
			self.nodes_values[node][0] = index
			if isinstance(self.matrix[self.nodes_i[node_from]][self.nodes_i[node]], str):
				if value_from + value > self.nodes_values[node][1]:
					self.nodes_values[node][1] = value_from + value
		# back		
		elif way == 'back':
			if isinstance(self.matrix[self.nodes_i[node_from]][self.nodes_i[node]], str):
				if value_from - value < self.nodes_values[node][2]:
					self.nodes_values[node][2] = value_from - value
		# wrong
		else:
			raise ValueError("worng given way, 'down' or 'back'")

	def matrix_add_fictives(self, node_ref: str, nodes_fictive: set, node_old: str) -> None:
		for node in nodes_fictive:
			"""
			if not self.matrix[self.nodes_i[node]][self.nodes_i[node_ref]]:
				self.matrix[self.nodes_i[node]][self.nodes_i[node_ref]] = {node}
			else:
				self.matrix[self.nodes_i[node]][self.nodes_i[node_ref]].update(node)
			"""
			self.matrix[self.nodes_i[node]][self.nodes_i[node_ref]] = [node]
			# remove old one
			self.matrix[self.nodes_i[node]][self.nodes_i[node_old]] = None

	def matrix_merge_nodes(self, node_ref: str, nodes_merged: list, node_end: str) -> None:
		for node in nodes_merged:
			# remove edge to 
			self.matrix[self.nodes_i[node]][self.nodes_i[node_end]] = None

			# rows
			for n in range(self.dim):
				if self.matrix[self.nodes_i[node]][n] != None:
					self.matrix[self.nodes_i[node_ref]][n] = self.matrix[self.nodes_i[node]][n]
					self.matrix[self.nodes_i[node]][n] = None
			# columns
			for m in range(self.dim):
				if self.matrix[m][self.nodes_i[node]] != None:
					self.matrix[m][self.nodes_i[node_ref]] = self.matrix[m][self.nodes_i[node]]
					self.matrix[m][self.nodes_i[node]] = None
			
	def matrix_reduce_nodes(self, nodes_merged: set) -> None:
		nodes_merged_i = [self.nodes_i[node] for node in nodes_merged]
		
		self.matrix = [
				[self.matrix[m][n] for n in range(self.dim) if n not in nodes_merged_i]
				for m in range(self.dim) if m not in nodes_merged_i
				]
		
		self.dim = len(self.matrix)
		self.nodes = [node for node in self.nodes if node not in nodes_merged]
		self.nodes_i = {node: i for i, node in enumerate(self.nodes)}
			
	def get_ancestors(self, fictive: bool=False) -> dict:
		""" get ancestors from self matrix
		
		dict of set
		"""
		if fictive:
			ancestors = {self.nodes[n]: {self.nodes[m] for m in range(self.dim) if self.matrix[m][n] != None} for n in range(self.dim)}
		else:
			ancestors = {self.nodes[n]: {self.nodes[m] for m in range(self.dim) if self.matrix[m][n] != None and isinstance(self.matrix[m][n], str)} for n in range(self.dim)}
		return ancestors
	
	def get_successors(self, fictive: bool=False) -> dict:
		""" get successors from self matrix
		dict of set
		"""
		if fictive:
			ancestors = {self.nodes[m]: {self.nodes[n] for n in range(self.dim) if self.matrix[m][n] != None} for m in range(self.dim)}
		else:
			ancestors = {self.nodes[m]: {self.nodes[n] for n in range(self.dim) if self.matrix[m][n] != None and isinstance(self.matrix[m][n], str)} for m in range(self.dim)}
		return ancestors
		
	def set_paths(self, nodes: list) -> list:
		""" get edges from nodes with matrix
		"""
		self.paths_edges.add(tuple(self.matrix[self.nodes_i[nodes[i-1]]][self.nodes_i[nodes[i]]] for i in range(1, len(nodes) - 1)))
		
	def group_nodes(self, nodes: list, ancestors: dict) -> tuple:
		"""
		
		.. IMPORTANT:: To well understand
		
			 Nodes in argument are ancestors of treated node
		"""
		ref = None
		merged = set()
		fictive = set()

		# set of all nodes in conflict
		#nodes_all = set(nodes)
		# counted nodes from ancestors
		ancestors_all = [ancestor for node in nodes for ancestor in ancestors[node]]
		# count grouped ancestors by nodes
		ancestors_count = {ancestor: ancestors_all.count(ancestor) for ancestor in set(ancestors_all)}
		# ancestors in conflict and its dependent nodes
		ancestors_conflict_nodes = {ancestor: {node for node in nodes if ancestor in ancestors[node]} for ancestor, count in ancestors_count.items() if count > 1}

		# counted grouped ancestors
		nodes_ancestors = [node for node in nodes for ancestor in ancestors[node]]
		# count grouped nodes by nodes
		nodes_ancestors_count = {node: nodes_ancestors.count(node) for node in set(nodes_ancestors)}
		# nodes for ancestors in conflict if each node don't appears in an other groups of ancestors in conflict
		ancestors_conflict_nodes_unique = {ancestor: [node for node in nodes if nodes_ancestors_count[node] == 1] for ancestor, nodes in ancestors_conflict_nodes.items()}
		# counts nodes in groups of ancestors in conflict if group of ancestors in conflict have at least one unique node (ancestors_conflict_nodes_unique)
		ancestors_conflict_nodes_unique_exist = {ancestor: len(nodes) for ancestor, nodes in ancestors_conflict_nodes_unique.items() if len(nodes) > 0}

		# nodes with independent ancestors
		#ancestors_nodes_indy = {ancestor: {node for node in nodes if ancestor in ancestors[node]} for ancestor, count in ancestors_count.items() if count == 1}
		nodes_indy = {node for node in nodes if node not in {n for l in ancestors_conflict_nodes.values() for n in l}}
		
		# ref
		# merge one node at least for each groups of ancestors in conflict
		if len(ancestors_conflict_nodes_unique_exist) == len(ancestors_conflict_nodes) and len(ancestors_conflict_nodes_unique_exist) > 1:
			# get one node in ancestors_conflict_nodes_unique
			ref = {node for nodes in ancestors_conflict_nodes_unique.values() for node in nodes}.pop()
		# merge at least one node with another one in another group of ancestors in conflict
		elif len(ancestors_conflict_nodes_unique_exist) > 1:
			ref = {node for nodes in ancestors_conflict_nodes_unique.values() for node in nodes}.pop()
		# ancestors groups exists
		elif ancestors_conflict_nodes:
			# get one node in ancestors_conflict_nodes
			ref = {node for nodes in ancestors_conflict_nodes.values() for node in nodes}.pop()
		else:
			ref = next(iter(nodes_indy))
		
		#acn = ancestors_conflict_nodes.copy()
		for k, nodes in ancestors_conflict_nodes.items():
			#local_ancestors_conflict_nodes = {node for ancestor, nodes in acn.items() for node in nodes if ancestor != k and node in ancestors_nodes_unique[k]}
			# for fictive nodes
			if ref in nodes:
				nodes.remove(ref)
			# for merging
			if ref in ancestors_conflict_nodes_unique[k]:
				ancestors_conflict_nodes_unique[k].remove(ref)
			# merge
			if  ancestors_conflict_nodes_unique[k] and len(ancestors_conflict_nodes_unique_exist) > 1:
				merged.update(ancestors_conflict_nodes_unique[k])
				nodes.difference_update(ancestors_conflict_nodes_unique[k])
			# fictive
			fictive.update(nodes)
			"""
			if ancestors_conflict_nodes_unique[k]:
				ref = ancestors_conflict_nodes_unique[k].pop()
				nodes.remove(ref)
				if len(ancestors_conflict_nodes_unique) > 1:
			# fictive
			fictive.update(nodes)
			"""

		if nodes_indy:
			if ref in nodes:
				nodes.remove(ref)
			# independent nodes are lonely (No groups of ancestors in conflict)
			if ancestors_conflict_nodes:
				merged.update(nodes_indy)
				nodes.difference_update(nodes_indy)
			else:
				poped = nodes.pop()
				merged.update(poped)

		return (ref, merged, fictive)

	def set_back(self):
		""" Define value of nodes by a DFS
		
		.. IMPORTANT:: node here is the numeric value in matrix
		
		don ot forget node with end for end !
		
		"""
		ancestors = self.get_ancestors(fictive=True)
		paths = [[self.node_end]]
		while paths:
			paths_tmp = paths
			paths = []
			for path in paths_tmp:
				node_successor = path[-1]
				nodes_ancestors = ancestors[node_successor]

				for node in nodes_ancestors:
					# cycle
					if node in path:
						exit(f"There is a ascending cycle in your graph: {' '.join(path)} -> {node}")
					
					# nodes
					self.add_node_value(node_successor, node, 'back')

					# paths
					if node != self.node_end:
						paths.append(path + [node])

	def set_down(self):
		""" Define value of nodes by a DFS
		"""
		index_nodes = 0
		index_ranks = 0
		nodes_ranked = {self.node_start}
		self.ranks = {0: {self.node_start}}
		successors = self.get_successors(fictive=True)
		paths = [[self.node_start]]
		# index, value_down, value_back
		self.nodes_values = {node: [None, 0, 0] for node in self.nodes}
		self.nodes_values[self.node_start] = [0,0,0]
		
		while paths:
			index_ranks += 1
			self.ranks[index_ranks] = set()
			paths_tmp = paths
			paths = []
			for path in paths_tmp:
				node_ancestor = path[-1]
				nodes_successors = successors[node_ancestor]
					
				for node in nodes_successors:
					# cycle
					if node in path:
						exit(f"There is a descending cycle in your graph: {' '.join(path)} -> {node}")
					
					# rank
					if node not in nodes_ranked:
						self.ranks[index_ranks].add(node)
						nodes_ranked.add(node)
						index_nodes += 1
					
					# nodes
					self.add_node_value(node_ancestor, node, 'down', index_nodes)

					# paths
					if node != self.node_end:
						paths.append(path + [node])
					else:
						self.paths.append(path + [node])

	def set_from_pert(self, pert: dict, **d) -> None:
		""" Set the graph from pert, values and optionally edge names 
		
		:param dict pert: pert definition containing for each task. her ancestors, value
		
			:index: (str) edge
			:value: tuple with edge ancestors, values of edge
				Contains tuple (: iter, value: int, label: str)
			 
				 #. ancestors (iter) in formats str  or [str,...] or (str, ...)
				 #. value (int)
			 
		:param dict \*\*d: containing options:
		
			:node_start: (str) character for starting node
			
				default: :class:`GraphPert.node_start`
			
			:node_end: (str) character for ending node
			
				default: :class:`GraphPert.node_end`
			
			:color_critical: (iter) color for drawing critical path of the Pert graph
						
				default: :class:`GraphPert.color_critical`

		"""
		if not pert:
			exit("The pert is empty ;o)")
		
		# comes from the arguments given otherwise from the graph 
		self.node_start = d['node_start'] if 'node_start' in d else GraphPert.node_start
		self.node_end = d['node_end'] if 'node_end' in d else GraphPert.node_end
		self.sep = d['sep'] if 'sep' in d else GraphPert.sep
		self.color_critical = d['color_critical'] if 'color_critical' in d else GraphPert.color_critical
		# simple initialization
		self.nodes_values = {}
		self.set_matrices(pert)
		# paths of edges
		self.paths = []

		if not self.matrix:
			exit("The data of pert is empty ;o)")

		# initialize
		ancestors = self.get_ancestors()
		nodes_merged_all = set()
		
		"""
		"""
		graph_matrices = []
		graph_nodes = []
		def copym(m): return [[i for i in l] for l in m]
		def copyn(n): return [i for i in n]
		
		ancestors2group = {n: a for n, a in ancestors.items() if len(a) > 1 and n != self.node_end}
		for node, nodes_ancestor in ancestors2group.items():
			"""
			"""
			graph_matrices.append(copym(self.matrix))
			graph_nodes.append(copyn(self.nodes))
			
			#nodes = ancestors[node]
			node_ref, nodes_merged, nodes_fictive = self.group_nodes(nodes_ancestor, ancestors)
			
			if nodes_fictive:
				self.matrix_add_fictives(node_ref, nodes_fictive, node)
			if nodes_merged:
				nodes_merged_all.update(nodes_merged)
				self.matrix_merge_nodes(node_ref, nodes_merged, node)
				ancestors = self.get_ancestors()
		"""
		"""
		graph_matrices.append(copym(self.matrix))
		graph_nodes.append(copyn(self.nodes))
		
		self.matrix_reduce_nodes(nodes_merged_all)

		"""
		"""
		graph_matrices.append(copym(self.matrix))
		graph_nodes.append(copyn(self.nodes))
		for i in range(len(graph_matrices)):
			g = Graph(matrix=graph_matrices[i], nodes=graph_nodes[i])
			g.draw(f"files/pert-inter5-{i}.svg", ext='svg', graph_attr={'rankdir':'LR'}, edge_attr={'fontsize':12})

		self.set_down()
		
		self.set_back()
		
	def set_matrices(self, pert):
		# nodes
		self.nodes = [k for k in pert.keys()]
		self.nodes.sort()
		self.nodes.remove(self.node_end)
		self.nodes.append(self.node_end)
		self.nodes.insert(0, self.node_start)
		self.nodes_i = {node: i for i, node in enumerate(self.nodes)}
		# edges
		self.edges_value = {node: data[1] for node, data in pert.items()}
		self.edges_value[self.node_start] = 0
		self.edges_value[self.node_end] = 0
		# dim
		self.dim = len(self.nodes)
		# matrix
		self.matrix = [[None for _ in range(self.dim)] for _ in range(self.dim)]
		for node_end, data in pert.items():
			nodes_start, _ = data
			if not nodes_start:
				nodes_start = self.node_start
			nodes_start = self.convert_nodes(nodes_start)
			for node_start in nodes_start:
				self.matrix[self.nodes_i[node_start]][self.nodes_i[node_end]] = node_end



