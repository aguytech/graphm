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
		'directed' : True,
		'rankdir' : 'LR',
		'ranksep' : "0.5",
		'strict' : False,
		'margin' : 0.02,
		'fontsize' : 14,
		'fontname' : 'Arial',
		'label' : 'Pert',
		}
	node_attr = {
		'fixedsize' : True,
		'width' : 0.7,
		'margin': 0.01,
		'shape' : 'circle',
		'color' : 'black',
		'fontsize' : 11,
		'fontname' : 'Arial',
		'fontcolor' : 'black',
		}
	edge_attr = {
		'color' : 'gray30',
		'fontsize' : 10,
		'fontname' : 'Arial',
		'fontcolor' : 'gray25',
		}
	
	def add_edges(self, **d) -> None:
		""" Add edges to viz from:
		"""
		style_fictional = {'color': 'dodgerblue4', 'style': 'dashed'}
		
		# add to viz
		for m in range(self.dim):
			for n in range(self.dim):
				if self.matrix[m][n]:
					edge = self.matrix[m][n]
					# regular edges
					if isinstance(edge, str): 
						self.viz.add_edge(m, n, label=f"{edge}.{self.edges_value[edge]}")
					# fictional edges
					else:
						edge = edge.pop()
						self.viz.add_edge(m, n, label=f"{edge}.0", **style_fictional)
				
	def add_nodes(self, **d) -> None:
		""" Add nodes to viz from:
		"""
		def rjust(*values) -> list:
			values = [str(i) for i in values]
			len_max = max({len(i) for i in values})
			return [i.rjust(len_max, ' ') for i in values]
		
		for rank, nodes in self.ranks.items():
			sb = self.viz.add_subgraph(name=f"rank{rank}", rank="same")
			
			sb.add_node(f"r{rank}")
			for node in nodes:
				index, value_down, value_back = self.nodes_values[node]
				value_down, value_back = str(value_down), str(value_back)
				#value_down, value_back = rjust(value_down, value_back)
				# add to viz
				sb.add_node(node, label=f"_{index}_\n{value_down} | {value_back}")

	def add_node_index(self, node: int, index: int) -> None:
		self.nodes_values[node][0] = index
		
	def add_node_value_down(self, node_from: str, node: int) -> None:
		"""
		.. IMPORTANT:: node here is node index
		
		"""
		# edge is not fictional
		if isinstance(self.matrix[node_from][node], str):
			value_edge = self.edges_value[self.matrix[node_from][node]]
		else:
			value_edge = 0
		value_from = self.nodes_values[node_from][1]
		
		if value_from + value_edge > self.nodes_values[node][1]:
			self.nodes_values[node][1] = value_from + value_edge
	
	def add_node_value_back(self, node_scs: str, node: int) -> None:
		"""
		.. IMPORTANT:: node here is node index
		
		"""
		if isinstance(self.matrix[node][node_scs], str):
			value_edge = self.edges_value[self.matrix[node][node_scs]]
		else:
			value_edge = 0
		value_from = self.nodes_values[node_scs][2]
		
		# TODO: remove this
		k_node_from = self.nodes[node_scs]
		k_node = self.nodes[node]

		# node_from is without end, keep path of unique node come from without end 		
		if value_from > -1:
			if self.nodes_values[node][2] < 0:
				self.nodes_values[node][2] = value_from - value_edge
			else:
				if value_from - value_edge < self.nodes_values[node][2]:
					self.nodes_values[node][2] = value_from - value_edge

	def add_path_critical(self, node: int, node_scs: int) -> None:
		# paths
		if self.nodes_values[node][1] == self.nodes_values[node][2] and node_scs in self.paths_critical:
			if node in self.paths_critical:
				self.paths_critical[node].add(node_scs)
			else:
				self.paths_critical[node] = {node_scs}
		
	def add_timeline(self, **d) -> None:
		""" Add nodes to viz from:
		"""
		# rank subgraph
		sb_tl = self.viz.add_subgraph(name='timeline')
		sb_tl.node_attr.update(fixedsize=True, width=0.5, fontcolor='blue')
		sb_tl.edge_attr.update(fontcolor='red')
		
		for i in self.ranks.keys():
			sb_tl.add_node(f"r{i}", width=0.5)
		for i in range(1, len(self.ranks)):
			sb_tl.add_edge(f"r{i - 1}", f"r{i}", label=i)
		sb_tl.layout(prog='dot')
			
	def matrix_add_fictionals(self, node_ref: str, nodes_fictional: set, node_old: str) -> None:
		for node in nodes_fictional:
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
			
	def get_ancestors_label(self, fictional: bool=False) -> dict:
		""" get ancestors from self matrix
		
		dict of set
		"""
		if fictional:
			ancestors = {self.nodes[n]: {self.nodes[m] for m in range(self.dim) if self.matrix[m][n] != None} for n in range(self.dim)}
		else:
			ancestors = {self.nodes[n]: {self.nodes[m] for m in range(self.dim) if self.matrix[m][n] != None and isinstance(self.matrix[m][n], str)} for n in range(self.dim)}
		return ancestors
	
	def get_successors_label(self, fictional: bool=False) -> dict:
		""" get successors from self matrix
		dict of set
		"""
		if fictional:
			ancestors = {self.nodes[m]: {self.nodes[n] for n in range(self.dim) if self.matrix[m][n] != None} for m in range(self.dim)}
		else:
			ancestors = {self.nodes[m]: {self.nodes[n] for n in range(self.dim) if self.matrix[m][n] != None and isinstance(self.matrix[m][n], str)} for m in range(self.dim)}
		return ancestors
		
	def get_ancestors(self, fictional: bool=False) -> dict:
		""" get ancestors from self matrix
		
		dict of set
		"""
		if fictional:
			ancestors = {n: {m for m in range(self.dim) if self.matrix[m][n] != None} for n in range(self.dim)}
		else:
			ancestors = {n: {m for m in range(self.dim) if self.matrix[m][n] != None and isinstance(self.matrix[m][n], str)} for n in range(self.dim)}
		return ancestors
	
	def get_successors(self, fictional: bool=False) -> dict:
		""" get successors from self matrix
		dict of set
		"""
		if fictional:
			ancestors = {m: {n for n in range(self.dim) if self.matrix[m][n] != None} for m in range(self.dim)}
		else:
			ancestors = {m: {n for n in range(self.dim) if self.matrix[m][n] != None and isinstance(self.matrix[m][n], str)} for m in range(self.dim)}
		return ancestors
		
	def group_nodes(self, nodes: list, ancestors: dict) -> tuple:
		"""
		
		.. IMPORTANT:: To well understand
		
			 Nodes in argument are ancestors of treated node
		"""
		ref = None
		merged = set()
		fictional = set()

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
		if len(ancestors_conflict_nodes_unique_exist) > 1 and len(ancestors_conflict_nodes_unique_exist) == len(ancestors_conflict_nodes):
			# get one node in ancestors_conflict_nodes_unique
			ref = {node for nodes in ancestors_conflict_nodes_unique.values() for node in nodes}.pop()
		# merge at least one node with another one in another group of ancestors in conflict
		elif len(ancestors_conflict_nodes_unique_exist) > 1:
			ref = {node for nodes in ancestors_conflict_nodes_unique.values() for node in nodes}.pop()
		# at lest ancestors group exists and at least an independent node 
		elif ancestors_conflict_nodes_unique_exist and nodes_indy:
			# get one node in ancestors_conflict_nodes
			ref = {node for nodes in ancestors_conflict_nodes_unique.values() for node in nodes}.pop()
		elif nodes_indy:
			# get node from independent nodes
			ref = next(iter(nodes_indy))
		else:
			# get one node in ancestors_conflict_nodes, no merging at all, just take a reference for fictional nodes
			ref = {node for nodes in ancestors_conflict_nodes.values() for node in nodes}.pop()
		
		# TODO: Merge one non-unique node in a group with an unique node for this group from another group
		if ancestors_conflict_nodes:
			acnu = {ancestor: node[:] for ancestor, node in ancestors_conflict_nodes_unique.items()}
			for act, nodes_act in ancestors_conflict_nodes.items():
				#local_ancestors_conflict_nodes = {node for ancestor, nodes in acn.items() for node in nodes if ancestor != k and node in ancestors_nodes_unique[k]}
				# for fictional nodes
				if ref in nodes_act:
					nodes_act.remove(ref)
				else:
					# merge
					if acnu[act] and (len(ancestors_conflict_nodes_unique_exist) > 1 or nodes_indy):
						poped = acnu[act].pop()
						nodes_act.remove(poped)
						merged.add(poped)
				# fictional
				fictional.update(nodes_act)

		if nodes_indy:
			# not existing an independent nodes in groups of ancestors in conflict
			if ref in nodes_indy:
				nodes_indy.remove(ref)
			# if existing a group of ancestor in conflict merge all independent nodes
			# if not, the predecessor rule removes one independent node (the reference node)
			merged.update(nodes_indy)

		return (ref, merged, fictional)

	def reset_nodes(self, **d) -> None:
		""" remove all nodes in viz
		"""
		# remove existing nodes
		self.viz.remove_nodes_from(self.viz.nodes())

	def reset_edges(self, **d) -> None:
		""" remove all edges in viz
		"""
		# remove existing nodes
		self.viz.remove_edges_from(self.viz.edges())
		
	def set_back(self):
		""" Define value of nodes by a DFS
		
		.. IMPORTANT:: node here is the numeric value in matrix
		
		do not forget node with end for end !
		
		"""
		node_start = 0
		ancestors = self.get_ancestors(fictional=True)
		paths = [[self.nodes_i[self.node_end]]]
		# critical paths of edges
		self.paths_critical = {self.dim - 1: {}}

		while paths:
			paths_tmp = paths
			paths = []
			for path in paths_tmp:
				node_successor = path[-1]
				nodes = ancestors[node_successor]

				for node in nodes:
					# cycle
					if node in path:
						exit(f"There is a ascending cycle in your graph: {' '.join(path)} -> {node}")
					
					# nodes
					self.add_node_value_back(node_successor, node)

					# paths
					self.add_path_critical(node, node_successor)
					if node == node_start:
						self.paths_back.append(path + [node])
					else:
						paths.append(path + [node])

	def set_down(self):
		""" Define value of nodes by a DFS
		
		.. IMPORTANT:: node here is the numeric value in matrix
		
		"""
		node_end = self.dim - 1
		index_nodes = 0
		index_ranks = 0
		nodes_visited = {0}
		ranks = {0: {0}}
		successors = self.get_successors(fictional=True)
		paths = [[0]]
		# index, value_down, value_back
		self.nodes_values = {i: [None, 0, -1] for i in range(self.dim)}
		self.nodes_values[0] = [0,0,-1]
		
		while paths:
			index_ranks += 1
			ranks[index_ranks] = set()
			paths_tmp = paths
			paths = []
			for path in paths_tmp:
				node_ancestor = path[-1]
				nodes = successors[node_ancestor]
					
				for node in nodes:
					# cycle
					if node in path:
						exit(f"There is a descending cycle in your graph: {' '.join(path)} -> {node}")
					
					# rank
					if node not in nodes_visited:
						index_nodes += 1
						self.add_node_index(node, index_nodes)
						ranks[index_ranks].add(node)
						nodes_visited.add(node)
					
					# nodes
					self.add_node_value_down(node_ancestor, node)

					# paths
					if node != node_end:
						paths.append(path + [node])
					else:
						self.paths_down.append(path + [node])
						
		# set ranks
		self.set_ranks(ranks)
		
		# close with put the final value for the back
		self.nodes_values[node_end][2] = self.nodes_values[node_end][1]

	def set_ranks(self, ranks):
		node_end = {self.dim - 1}
		# reduce ranks of empty sets and remove ending node
		self.ranks = {k: v.difference(node_end) for k, v in ranks.items() if v }
		# add ending node at last rank
		self.ranks[len(self.ranks) - 1].update(node_end)
		
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
		if self.node_end not in pert.keys():
			exit(f"The ending character '{self.node_end}' is missing")
		
		# comes from the arguments given otherwise from the graph 
		self.node_start = d['node_start'] if 'node_start' in d else GraphPert.node_start
		self.node_end = d['node_end'] if 'node_end' in d else GraphPert.node_end
		self.sep = d['sep'] if 'sep' in d else GraphPert.sep
		self.color_critical = d['color_critical'] if 'color_critical' in d else GraphPert.color_critical
		# simple initialization
		self.nodes_values = {}
		self.set_matrices(pert)
		# downing paths of edges
		self.paths_down = []
		# backing paths of edges
		self.paths_back = []

		if not self.matrix:
			exit("The data of pert is empty ;o)")

		# initialize
		ancestors = self.get_ancestors_label()
		nodes_merged_all = set()
		
		"""
		graph_matrices = []
		graph_nodes = []
		def copym(m): return [[i for i in l] for l in m]
		def copyn(n): return [i for i in n]
		graph_matrices.append(copym(self.matrix))
		graph_nodes.append(copyn(self.nodes))
		"""
		
		ancestors2group = {n: a for n, a in ancestors.items() if len(a) > 1 and n != self.node_end}
		for node, nodes_ancestor in ancestors2group.items():
			node_ref, nodes_merged, nodes_fictional = self.group_nodes(nodes_ancestor, ancestors)
			
			if nodes_fictional:
				self.matrix_add_fictionals(node_ref, nodes_fictional, node)
			if nodes_merged:
				nodes_merged_all.update(nodes_merged)
				self.matrix_merge_nodes(node_ref, nodes_merged, node)
				ancestors = self.get_ancestors_label()
		
		self.matrix_reduce_nodes(nodes_merged_all)

		"""
		graph_matrices.append(copym(self.matrix))
		graph_nodes.append(copyn(self.nodes))
		for i in range(len(graph_matrices)):
			g = Graph(matrix=graph_matrices[i], nodes=graph_nodes[i])
			g.draw(f"files/pert-inter5-{i}.svg", ext='svg', graph_attr={'rankdir':'LR'}, edge_attr={'fontsize':12})
		"""

		self.set_down()
		self.set_back()
		self.add_timeline()
		self.add_nodes()
		self.add_edges()
		
		self.draw('files/pert_first.svg', ext='svg')
		print('gag')
		
	def set_matrices(self, pert):
		# nodes
		self.nodes = [k for k in pert.keys()]
		self.nodes_lonely = set(self.nodes).difference({i for d in pert.values() for i in d[0].split(',')}, self.node_end)
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
				# with value
				#self.matrix[self.nodes_i[node_start]][self.nodes_i[node_end]] = node_end + str(self.edges_value[node_end])

	def set_nodes(self, **d) -> None:
		""" Set nodes to viz from:
		"""
		self.reset_nodes()
		self.add_nodes()

	def set_edges(self, **d) -> None:
		""" Add edges to viz from:
		"""
		self.reset_edges()
		self.add_edges()
				


