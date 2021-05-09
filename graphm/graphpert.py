'''
Created on Apr 26, 2021

@author: salem Aguemoun
'''
import graphm.graph

class GraphPert(graphm.graph.Graph):
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
	
	:var list matrix: matrix of graph.
	
		Generated from initialization to simplify the build of Pert's graph
	
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
		'ranksep' : 1,
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
	
	@staticmethod
	def _dict_add(d: dict, index: int, item: iter) -> None:
		""" add in place item in given dictionary
		""" 
		if index in d:
			d[index].add(item)
		else:
			d[index] = {item}
		
	def add_critical(self) -> None:
		""" Add critical path to viz from:
		"""
		sbu = self.viz.add_subgraph(name='critical', label='', color='white')
		#sbc = self.viz.add_subgraph(name='critical')
		
		self.set_critical()
		self.set_nodes_index()
		self.add_nodes_critical(sbu, sbu)
		self.add_edges_critical(sbu, sbu)
		
	def add_edge_viz(self, sb: 'pygraphviz.AGraph', edge, **d) -> None:
		""" add edge in pygraphviz.AGraph passed in argument
		"""
		m, n = edge
		task = self.matrix[m][n]
		if isinstance(task, str):
			d.update({
				'label': f"{task}.{self.tasks_value[task]}",
			})
		# fictional edges
		else:
			task = task.pop()
			d.update({
				'label': f"{task}.0",
				 'style': 'dashed',
			})
		sb.add_edge(m, n, **d)
				
	def add_edges(self) -> None:
		""" Add edges to viz from:
		"""
		# all edges reduce by critical ones
		#TODO: delete
		#edges = {(m, n): self.matrix[m][n] for n in range(self.dim) for m in range(self.dim) if self.matrix[m][n] and (m, n) not in self.edges_critical}
		edges = {(m, n): self.matrix[m][n] for n in range(self.dim) for m in range(self.dim) if self.matrix[m][n] and (m, n) not in self.edges_critical}
		for edge, task in edges.items():
			d = {} if isinstance(task, str) else {'color': 'dodgerblue4', 'fontcolor': 'dodgerblue4'}
			self.add_edge_viz(self.viz, edge, **d)
				
	def add_edges_critical(self, sbu: 'pygraphviz.AGraph', sbc: 'pygraphviz.AGraph') -> None:
		""" Add critical edges to viz
		"""
		edges_unique = {(self.path_unique[i-1], self.path_unique[i]) for i in range(1, len(self.path_unique))}
		for edge in self.edges_critical:
			# unique
			if edge in edges_unique:
				sb = sbu
				args = {'color': 'red', 'fontcolor': 'red', 'fontname': 'arial bold', 'penwidth': 1.5}
			else:
				sb = sbc
				args = {'color': 'firebrick', 'fontcolor': 'firebrick', 'penwidth': 1.5}
			
			self.add_edge_viz(sb, edge, **args)

	def add_node_value_down(self, node_from: str, node: int) -> None:
		"""
		.. IMPORTANT:: node here is node index
		
		"""
		# edge is not fictional
		if isinstance(self.matrix[node_from][node], str):
			value_edge = self.tasks_value[self.matrix[node_from][node]]
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
			value_edge = self.tasks_value[self.matrix[node][node_scs]]
		else:
			value_edge = 0
		value_from = self.nodes_values[node_scs][2]
		
		# node_from is without end, keep path of unique node come from without end 		
		if value_from > -1:
			if self.nodes_values[node][2] < 0:
				self.nodes_values[node][2] = value_from - value_edge
			else:
				if value_from - value_edge < self.nodes_values[node][2]:
					self.nodes_values[node][2] = value_from - value_edge

	def add_node_viz(self, sb: 'pygraphviz.AGraph', node, **d) -> None:
		""" add node in pygraphviz.AGraph passed in argument
		"""
		""" keep to format 
		def rjust(*values) -> list:
			values = [str(i) for i in values]
			len_max = max({len(i) for i in values})
			return [i.rjust(len_max, ' ') for i in values]
		
		value_down, value_back = rjust(value_down, value_back)
		"""
		index, value_down, value_back = self.nodes_values[node]
		value_down, value_back = str(value_down), str(value_back)
		sb.add_node(node, label=f"_{index}_\n{value_down} | {value_back}", **d)

	def add_nodes(self) -> None:
		""" Add nodes to viz from:
		"""
		for rank, nodes in self.ranks.items():
			sb = self.viz.add_subgraph(name=f"rank{rank}", rank="same")
			sb.add_node(f"r{rank}")
			for node in nodes:
				if node in self.nodes_critical:
					sb.add_node(node)
				else:
					self.add_node_viz(sb, node)

	def add_nodes_critical(self, sbu: 'pygraphviz.AGraph', sbc: 'pygraphviz.AGraph') -> None:
		""" Add critical nodes to viz
		"""
		for node in self.nodes_critical:
			if node in self.path_unique:
				sb = sbu
				args = {'color': 'red', 'fontcolor': 'red', 'fontname': 'arial bold', 'penwidth': 1.5}
			else:
				sb = sbc
				args = {'color': 'firebrick', 'fontcolor': 'firebrick', 'penwidth': 1.5}
			self.add_node_viz(sb, node, **args)
			
	def add_timeline(self, **d) -> None:
		""" Add nodes to viz from:
		"""
		# rank subgraph
		sb = self.viz.add_subgraph(name='timeline')
		
		for rank in self.ranks.keys():
			sb.add_node(f"r{rank}", width=0.5)
		for rank in range(1, len(self.ranks)):
			sb.add_edge(f"r{rank - 1}", f"r{rank}", label=rank)
		sb.layout(prog='dot')
			
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
			
	def matrix_reduce_nodes(self, nodes_merged: set, new_end: str) -> None:
		""" 
		new_end do to reduce matrix from node_end
		"""
		# remove ending node
		if new_end:
			nodes_merged.add(self.node_end)
			self.node_end = new_end
			# remove old ending successor for the new ending node
			self.matrix[self.nodes_i[new_end]][self.dim - 1] = ''
		nodes_merged_i = {self.nodes_i[node] for node in nodes_merged}
		
		self.matrix = [
				[self.matrix[m][n] for n in range(self.dim) if n not in nodes_merged_i]
				for m in range(self.dim) if m not in nodes_merged_i
				]
		
		self.dim = len(self.matrix)
		self.nodes = [node for node in self.nodes if node not in nodes_merged]
		self.nodes_i = {node: i for i, node in enumerate(self.nodes)}

	def get_ancestors(self, fictional: bool=False) -> dict:
		""" get ancestors from self matrix
		
		dict of set
		"""
		if fictional:
			ancestors = {n: {m for m in range(self.dim) if self.matrix[m][n] != None} for n in range(self.dim)}
		else:
			ancestors = {n: {m for m in range(self.dim) if self.matrix[m][n] != None and isinstance(self.matrix[m][n], str)} for n in range(self.dim)}
		return ancestors
	
	def get_ancestors_label(self, fictional: bool=False) -> dict:
		""" get ancestors from self matrix
		
		dict of set
		"""
		if fictional:
			ancestors = {self.nodes[n]: {self.nodes[m] for m in range(self.dim) if self.matrix[m][n] != None} for n in range(self.dim)}
		else:
			ancestors = {self.nodes[n]: {self.nodes[m] for m in range(self.dim) if self.matrix[m][n] != None and isinstance(self.matrix[m][n], str)} for n in range(self.dim)}
		return ancestors
	
	def get_successors(self, fictional: bool=False) -> dict:
		""" get successors from self matrix
		dict of set
		"""
		if fictional:
			successors = {m: {n for n in range(self.dim) if self.matrix[m][n] != None} for m in range(self.dim)}
		else:
			successors = {m: {n for n in range(self.dim) if self.matrix[m][n] != None and isinstance(self.matrix[m][n], str)} for m in range(self.dim)}
		return successors
		
	def get_successors_label(self, fictional: bool=False) -> dict:
		""" get successors from self matrix
		dict of set
		"""
		if fictional:
			ancestors = {self.nodes[m]: {self.nodes[n] for n in range(self.dim) if self.matrix[m][n] != None} for m in range(self.dim)}
		else:
			ancestors = {self.nodes[m]: {self.nodes[n] for n in range(self.dim) if self.matrix[m][n] != None and isinstance(self.matrix[m][n], str)} for m in range(self.dim)}
		return ancestors
		
	def group_nodes(self, nodes: list, ancestors: dict) -> tuple:
		"""
		
		.. IMPORTANT:: To well understand
		
			 Nodes in argument are ancestors of treated node
		"""
		
		def get_ref_max_scs(nodes: iter):
			""" Returns the name of node which have the maximum of successors
			
			stabilizes the final structure of the graph by optimizing the critical path according to the fictitious paths 
			"""
			# get nodes names of successors of all nodes 
			successors = self.get_successors_label(fictional=True)
			# get number of successors of nodes (just one for each count)
			refs_scs = {len(successors[node]): node for node in nodes}
			# get the name of node of the maximum of successors
			return refs_scs[max(refs_scs.keys())]
			
		def get_ref_max_value(nodes: iter):
			""" Returns the name of the node with the highest task value
			
			Optimize the graph by avoiding the passage of critical paths by a fictitious path
			Stabilize the graph by taking the same path
			"""
			# get nodes names of successors of all nodes 
			values = {self.tasks_value[i]: i for i in nodes}
			return values[max(values.keys())]
			
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
			ref = get_ref_max_scs(node for nodes in ancestors_conflict_nodes_unique.values() for node in nodes)
		# merge at least one node with another one in another group of ancestors in conflict
		elif len(ancestors_conflict_nodes_unique_exist) > 1:
			ref = get_ref_max_scs(node for nodes in ancestors_conflict_nodes_unique.values() for node in nodes)
		# at lest ancestors group exists and at least an independent node 
		elif ancestors_conflict_nodes_unique_exist and nodes_indy:
			# get one node in ancestors_conflict_nodes
			ref = get_ref_max_scs(node for nodes in ancestors_conflict_nodes_unique.values() for node in nodes)
		elif nodes_indy:
			# get node from independent nodes
			ref = get_ref_max_value(nodes_indy)
		else:
			# get one node in ancestors_conflict_nodes, the one have the biggest task value
			ref = get_ref_max_value({node for nodes in ancestors_conflict_nodes.values() for node in nodes})
		
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

	def set_back(self):
		""" Define value of nodes by a DFS
		
		.. IMPORTANT:: node here is the numeric value in matrix
		
		do not forget node with end for end !
		
		"""
		node_start = 0
		node_end = self.nodes_i[self.node_end]
		ancestors = self.get_ancestors(fictional=True)
		paths = [[node_end]]
		paths_back = []

		while paths:
			paths_tmp = paths
			paths = []
			for path in paths_tmp:
				node_successor = path[-1]
				nodes = ancestors[node_successor]

				for node in nodes:
					if node != node_end:
						# nodes
						self.add_node_value_back(node_successor, node)
						
						# cycle
						if node in path:
							# TODO9: replace old one
							#exit(f"There is a ascending cycle in your graph:  {' '.join(str(i) for i in path)} -> {node}")
							raise ValueError(f"There is a backing cycle in your graph: {' '.join(str(i) for i in path)} -> {node}")
					
						# paths
						if node == node_start:
							paths_back.append(path + [node])
						else:
							paths.append(path + [node])
							
		self.paths_back = {tuple(i) for i in paths_back}

	def set_critical(self):
		""" get the best critical path ;o)
		"""
		def iscritical(node_start: int, node_end: int) -> bool:
			ve = self.tasks_value[self.matrix[node_start][node_end]] if isinstance(self.matrix[node_start][node_end], str) else 0
			return self.nodes_values[node_start][1] + ve == self.nodes_values[node_end][1]
				
		self.nodes_critical = {node for node, data in self.nodes_values.items() if data[1] == data[2]}
		paths_critical = set()
		
		for path in self.paths_down:
			add = True
			for i in range(1, len(path)):
				if path[i] not in self.nodes_critical or not iscritical(path[i-1], path[i]):
					add = False
					break
			if add:
				paths_critical.add(path)
		
		# paths		
		self.paths_critical = {}
		self.edges_critical = set()
		for path in paths_critical:
			self._dict_add(self.paths_critical,len(path), path)
			self.edges_critical.update((path[i-1], path[i]) for i in range(1, len(path)))
		self.path_unique = next(iter(self.paths_critical[min(self.paths_critical.keys())]))
		
	def set_down(self):
		""" Define value of nodes by a DFS
		
		.. IMPORTANT:: node here is the numeric value in matrix
		
		"""
		node_end = self.nodes_i[self.node_end]
		nodes_visited = {0}
		paths = [[0]]
		paths_down = []
		successors = self.get_successors(fictional=True)
		# index, value_down, value_back
		self.nodes_values = {i: [i, 0, -1] for i in range(self.dim)}
		self.nodes_values[0] = [0,0,-1]
		
		while paths:
			paths_tmp = paths
			paths = []
			for path in paths_tmp:
				node_ancestor = path[-1]
				nodes = successors[node_ancestor]
					
				for node in nodes:
					# cycle
					if node in path and node != node_end:
						# TODO: replace old one
						# exit(f"There is a descending cycle in your graph: {' '.join(str(i) for i in path)} -> {node}")
						raise ValueError(f"There is a descending cycle in your graph: {' '.join(str(i) for i in path)} -> {node}")
					
					# nodes
					nodes_visited.add(node)
					self.add_node_value_down(node_ancestor, node)

					# paths
					if node != node_end:
						paths.append(path + [node])
					else:
						paths_down.append(path + [node])
						
		# close with put the final value for the back
		self.nodes_values[node_end][2] = self.nodes_values[node_end][1]
		self.paths_down = {tuple(i) for i in paths_down}

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
		# downing paths of edges
		self.paths_down = []
		# backing paths of edges
		self.paths_back = []

		# initialize
		self.set_matrix(pert)
		if not self.matrix:
			exit("The data of pert is empty ;o)")

		# generate
		self.matrix_reduce()
		self.set_down()
		self.set_back()
		self.set_ranks()
		#drawing
		self.add_critical()
		self.add_nodes()
		self.add_edges()
		self.add_timeline()
		print(self.viz)
		self.draw('files/pert_first.svg', ext='svg')
		
		print('gag')
		
	def matrix_reduce(self):
		
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
		
		ancestors2group = {n: a for n, a in ancestors.items() if len(a) > 1}
		for node, nodes_ancestor in ancestors2group.items():
			node_ref, nodes_merged, nodes_fictional = self.group_nodes(nodes_ancestor, ancestors)
			
			if nodes_fictional:
				self.matrix_add_fictionals(node_ref, nodes_fictional, node)
			if nodes_merged:
				nodes_merged_all.update(nodes_merged)
				self.matrix_merge_nodes(node_ref, nodes_merged, node)
				ancestors = self.get_ancestors_label()
		
		new_end = ancestors[self.node_end].pop() if len(ancestors[self.node_end]) == 1 else None
		self.matrix_reduce_nodes(nodes_merged_all, new_end)

		"""
		graph_matrices.append(copym(self.matrix))
		graph_nodes.append(copyn(self.nodes))
		for i in range(len(graph_matrices)):
			g = Graph(matrix=graph_matrices[i], nodes=graph_nodes[i])
			g.draw(f"files/pert-inter5-{i}.svg", ext='svg', graph_attr={'rankdir':'LR'}, edge_attr={'fontsize':12})
		"""

	def set_matrix(self, pert):
		# nodes
		self.nodes = [k for k in pert.keys()]
		self.nodes_lonely = set(self.nodes).difference({i for d in pert.values() for i in d[0].split(',')}, self.node_end)
		self.nodes.sort()
		self.nodes.remove(self.node_end)
		self.nodes.append(self.node_end)
		self.nodes.insert(0, self.node_start)
		self.nodes_i = {node: i for i, node in enumerate(self.nodes)}
		# edges
		self.tasks_value = {node: data[1] for node, data in pert.items()}
		self.tasks_value[self.node_start] = 0
		self.tasks_value[self.node_end] = 0
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
				#self.matrix[self.nodes_i[node_start]][self.nodes_i[node_end]] = node_end + str(self.tasks_value[node_end])

	def set_nodes_index(self, style: str='from_ancestor') -> None:
		""" Sets index for all nodes
		"""
		if style == 'follow':
			index = 0
			for nodes in self.ranks.values():
				for node in nodes:
					self.nodes_values[node][0] = index
					index += 1
					
		elif style == 'from_ancestor':
			successors = self.get_successors()
			indexed = {0}
			index = 1
			for rank, nodes_rank in self.ranks.items():
				if rank != 0:
					for ancestor in self.ranks[rank - 1]:
						for node in successors[ancestor]:
							if node in nodes_rank and node not in indexed:
								self.nodes_values[node][0] = index
								indexed.add(node)
								index += 1
		
	def set_ranks(self):
		""" set ranks for nodes
		"""
		def add_last(node, rank, ranks):
			""" use local parent variables: ranks, node_visited
			""" 
			if node in nodes_visited:
				ranks = {k: v.difference({node}) for k,v in ranks.items()}
			if rank in ranks:
				ranks[rank].add(node)
			else:
				ranks[rank] = {node}
			return ranks
		
		node_end = self.nodes_i[self.node_end]
		successors = self.get_successors()
		ranks = {0: {0}}
		rank = 0
		nodes_visited = {0}
		paths = [[0]]

		while paths:
			rank += 1
			paths_tmp = paths
			paths = []
			for path in paths_tmp:
				node_ancestor = path[-1]
				nodes = successors[node_ancestor]

				for node in nodes:
					# rank
					ranks = add_last(node, rank, ranks)
					nodes_visited.add(node)
					
					# paths
					if node != node_end:
						paths.append(path + [node])
		self.ranks = ranks
				


				


