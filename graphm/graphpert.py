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
	
	def get_successors(self) -> dict:
		""" get successors from self matrix
		"""
		return {self.nodes[m]: [self.nodes[n] for n in range(self.dim) if self.matrix[m][n] != None] for m in range(self.dim)}
		
	def get_ancestors(self) -> dict:
		""" get ancestors from self matrix
		"""
		return {self.nodes[n]: [self.nodes[m] for m in range(self.dim) if self.matrix[m][n] != None] for n in range(self.dim)}
	
	def merge_nodes(self, node_ref: str, nodes_merged: list) -> None:
		def merge(matrix):
			for node in nodes_merged:
				# rows
				for n in range(self.dim):
					if matrix[self.nodes_i[node]][n] != None:
						matrix[self.nodes_i[node_ref]][n] = matrix[self.nodes_i[node]][n]
						matrix[self.nodes_i[node]][n] = None
				# columns
				for m in range(self.dim):
					if matrix[m][self.nodes_i[node]] != None:
						matrix[m][self.nodes_i[node_ref]] = matrix[m][self.nodes_i[node]]
						matrix[m][self.nodes_i[node]] = None
		
		merge(self.matrix)
		merge(self.matrix_fictive)
			
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
		self.node_start = d['node_start'] if 'node_start' in d else GraphPert.node_start
		self.node_end = d['node_end'] if 'node_end' in d else GraphPert.node_end
		self.color_critical = d['color_critical'] if 'color_critical' in d else GraphPert.color_critical
		self.set_matrices(pert)
		
		# initialize
		ancestors = self.get_ancestors()
		nodes_values = {i: [0, 0] for i in self.nodes}
		edges_label = {}
		edges_value = {}
		
		iter_nodes = iter(self.nodes)
		next(iter_nodes)
		for node in iter_nodes:
			nodes = ancestors[node]
			node_ref, nodes_merged, nodes_fictive = self.group_nodes(ancestors[node], ancestors)
			
			if nodes_fictive:
				self.set_nodes_fictive(node_ref, nodes_fictive)
			
			if nodes_merged:
				self.merge_nodes(node_ref, nodes_merged)
				ancestors = self.get_ancestors()
			
		self.set_down(edges_value, edges_label, nodes_values)

	"""
	ancs = self.convert_nodes(data[0])
	if not ancs:
		ancs = ['>']
	elif len(ancs) == 1:
		anc = ancs[0]
	else:
		ancs_list = [i for j in ancs.split(',') for i in ancestors[j].split(',')]
		tmp = {i: ancs_list.count(i) for i in set(ancs_list)}
		tmp = [(j, i) for j in ancs.split(',') for i in ancestors[j].split(',')]
	for anc in ancs:
		successors[anc].append(edge)
		edges_value[(anc, edge)] = value
	"""
	
	def group_nodes(self, nodes: list, ancestors: dict) -> tuple:
		"""
		
		.. IMPORTANT:: To well understand
		
			 Nodes in argument are ancestors of treated node
		"""
		merged = set()
		fictive = set()
		if not nodes:
			ref = '>'
		elif len(nodes) == 1:
			ref = nodes[0]
		else:
			
			print('gag')
			# all ancestors from all nodes
			ancestors_nodes_all = [ancestor for node in nodes for ancestor in ancestors[node]]
			# counted grouped ancestors
			ancestors_nodes_count = {ancestor: ancestors_nodes_all.count(ancestor) for ancestor in set(ancestors_nodes_all)}
			# conflicted ancestors and its dependent nodes
			ancestors_conflict_nodes = {ancestor: [node for node in nodes if ancestor in ancestors[node]] for ancestor, count in ancestors_nodes_count.items() if count > 1}
			# conflicted ancestors and its nodes
			ancestors_indy_nodes = {ancestor: [node for node in nodes if ancestor in ancestors[node]] for ancestor, count in ancestors_nodes_count.items() if count == 1}
			# all nodes from ancestors_conflict_nodes
			nodes_conflict = [node for nodes in ancestors_conflict_nodes.values() for node in nodes]
			# all nodes from ancestors_unique_nodes, a set coz successors of unique are node
			nodes_conflict_unique = {node for nodes in ancestors_conflict_nodes.values() for node in nodes}
			# all nodes from ancestors_unique_nodes, a set coz successors of unique are node
			nodes_indy = {node for nodes in ancestors_indy_nodes.values() for node in nodes}
			# conflicted ancestors and its dependent unique nodes (nodes with only one ancestor)
			ancestors_conflict_nodes_unique =  {ancestor: [node for node in nodes if nodes_conflict.count(node) == 1] for ancestor, nodes  in ancestors_conflict_nodes.items()}
			
			"""

			# all nodes and its ancestors
			nodes_ancestors = {node: [ancestor for ancestor in ancestors[node]] for node in nodes}
			nodes_ancestors_count = {node: max(ancestors_nodes_count[c] for c in ancestors) for node, ancestors in nodes_ancestors.items()}
			# Count number of children for the ancestor of node => give the number of brothers by node
			nodes_brothers_count = {node: sum(ancestors_nodes_count[a] for a in ancestors) for node, ancestors in nodes_ancestors.items()}
			# nodes with no common ancestors, wich have no brothers
			nodes_ancestors_unique = [node for node, count in nodes_brothers_count.items() if count == 1]
			# nodes with common ancestors, wich have brothers
			nodes_ancestors_conflict = [node for node, count in nodes_brothers_count.items() if count > 1]
			
			# list of all chidren of the conflicted ancestors
			nodes_ancestors_conflict_nodes = [i for l in ancestors_conflict_nodes.values() for i in l]

			# count each nodes for conflicted ancestors
			#nodes_conflict_count = {ancestor: {node: nodes_conflict.count(node) for node in nodes} for ancestor, nodes  in ancestors_conflict_nodes.items()}
			"""
			
			# remove conflicting nodes from independent nodes if nodes appears in the 2 groups
			nodes_indy = nodes_indy - nodes_conflict_unique
				
			#if len(nodes_ancestors_conflict_nodes) == len(set(nodes_ancestors_conflict_nodes)):
			# test if in each nodes in each group are different
			if nodes_indy:
				# indy
				ref = nodes_indy.pop()
				merged |= nodes_indy
				
				# conflicting
				# TODO to improve following rules, look for each group wich on can be merge with node in other group, group by group
				# merge only node with unique ancestor 
				for k, nodes in ancestors_conflict_nodes.items():
					if ancestors_conflict_nodes_unique[k]:
						poped = nodes.pop()
						nodes.remove(poped)
						merged.add(poped)
					# fictive
					fictive |= set(nodes)
			else:
				# TODO to improve following rules, look for each group wich on can be merge with node in other group, group by group
				# merge only node with unique ancestor 
				for k, nodes in ancestors_conflict_nodes_unique.items():
					ref = nodes.pop()
					ancestors_conflict_nodes[k].remove(ref)
					# pop only when others groups exists
					if len(ancestors_conflict_nodes_unique) > 1:
						merged.add(poped)
					# fictive
					fictive |= set(ancestors_conflict_nodes[k])

		return (ref, merged, fictive)

		"""
		{(anc if anc else '>'): edge for edge, data in pert.items() for anc in data[0]}
		
		for edge, data in pert.items():
			edges_anc, value = data[:2]
			edges_anc = self.convert_nodes(edges_anc)
			
			if not edges_anc:
				self.viz.add_edge('>', edge, f"{edge}-{value}")
			else:
				edges.extend((i, edge) for i in data)
		"""
		
		"""
		edges = []
		for edge, data in ancestors.items():
			edges_anc, value = data[:2]
			edges_anc = self.convert_nodes(edges_anc)
			
			if not edges_anc:
				self.viz.add_edge('>', edge, f"{edge}-{value}")
			else:
				edges.extend((i, edge) for i in data)
		"""
	def set_down(self, successors: dict, edges_value: dict, edges_label: dict, nodes_values: dict) -> None:
		""" Define value of nodes by a DFS
		"""
		edges_new = {}
		index = 1
		paths = [[self.node_start]]
		
		# no successors with or without itself
		if not successors:
			paths = []
		
		while paths:
			paths_tmp = paths
			paths = []
			for path in paths_tmp:
				node_act = path[-1]
				path_successors = successors[node_act]
				for node in path_successors:
					# edges
					edges_new[(node_act, index)] = edges_values[(node_act, node)]
					# nodes
					self.set_node_value(nodes_values, node, index, edges_value[(node_act, node)])
					if node != self.node_end:
						paths.append(path + [node])
					index += 1
	
	def set_node_value(self, nodes_values: dict, node: str, index: int, value: int) -> None:
		# down
		if index == 0:
			if value > nodes_values[node][index]:
				nodes_values[node][index] = value
		else:
			if value < nodes_values[node][index]:
				nodes_values[node][index] = value

	def set_nodes_fictive(self, node_ref, nodes_fictive: set) -> None:
		for node in nodes_fictive:
			self.matrix_fictive[self.nodes_i[node]][self.nodes_i[node_ref]] = 1

	def set_matrices(self, pert):
		# nodes
		self.nodes = [k for k in pert.keys()]
		self.nodes.sort()
		self.nodes.remove(self.node_end)
		self.nodes.append(self.node_end)
		self.nodes.insert(0, self.node_start)
		self.nodes_i = {node: i for i, node in enumerate(self.nodes)}
		
		self.dim = len(self.nodes)
		self.matrix = [[None for _ in range(self.dim)] for _ in range(self.dim)]
		self.matrix_fictive = [[None for _ in range(self.dim)] for _ in range(self.dim)]
		
		for node_end, data in pert.items():
			nodes_start, value = data
			if not nodes_start:
				nodes_start = self.node_start
			nodes_start = self.convert_nodes(nodes_start)
			for node_start in nodes_start:
				self.matrix[self.nodes_i[node_start]][self.nodes_i[node_end]] = value




