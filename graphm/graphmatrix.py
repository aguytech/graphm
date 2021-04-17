import pygraphviz

class GraphM:
	""" Manage graph with matrix:
	
		* Data with internal representation in matrix
		* Representation of graph with the export capacity in dot format
	
	:var str node_style: default style to generate nodes
	
		**str** / str, int
	
	:var dict layout: default attributes for graph layout, see :class:`pygraphviz.Agraph`
	
		:prog: (str) type of programmed layout
			
			**dot** / neato, dot, twopi, circo, fdp, nop

	:var dict graph_attr: default attributes for graph, see :class:`pygraphviz.Agraph`
	
		:directed: (bool) directed graph or not
		:label: (str) label printed in the graph
		:rankdir: (str) orientation for dot graph
		:ranksep: (str) distance between nodes
		:strict: (bool) mode for dot graph
	
	:var dict node_attr: default attributes for nodes, see :class:`pygraphviz.Agraph`
	
		:color: (str) font color of nodes
		:fontcolor: (str) font color of nodes
		:fontname: (str) font name of nodes
		:shape: (str) shape of nodes
		
	:var dict edge_attr: default attributes for edges, see :class:`pygraphviz.Agraph`
	
		:color: (str) font color of edges
		:fontcolor: (str) font color of edges
		:fontname: (str) font name of edges

	.. CAUTION:: Instance variables
	
	:var list matrix: square matrix containing integer values in 2 dimensions
	:var int dim: number of rows and columns
	:var pygraphviz.AGraph viz: manage drawing in dot format with :class:`pygraphviz.AGraph`

	:var dict layout: graph layout, see :class:`Graph.layout`

			

	**Graph for the majority of examples** 
	
	.. IMAGE:: files/graph2.png
	
	"""
	node_style = 'str'
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
	
	def __init__(self, **d) -> 'Graph':
		""" Set the graph properties from matrix or a classical graph definition
		
			* matrix
						
		 		| **boolean** get a boolean matrix
				| **binary** get a binary matrixM and dimN
		
			* classical
						
				| **edges** get list of edges and of optionally nodes
				| **nodes** optional, get list of nodes

		:param dict \*\*d: options to specify the type of matrix
		
			:boolean: (list[int]) matrix in [str, ...] or [[int,...], ...] or (str, ...) or ((int,...), ...)
			:binary: matrixM in [int, ...]
			:edges: (tuple/list) list of edges in tuple format (nodeIn, nodeOut)
			:nodes: (tuple/list) optional list of nodes

			for **nodes**
			
			:nodes: (iter(str)) names of nodes
			:node_style='str': (str) type of nodes name generation 'str' or 'int' 
			
			for **viz**
			
			:layout: (dict) default attributes for graph layout, see :class:`Graph.layout`
			:graph_attr: (dict) default attributes for graph, see :attr:`Graph.graph_attr`
			:node_attr: (dict) default attributes for nodes, see :attr:`Graph.node_attr`
			:edge_attr: (dict) default attributes for edges, see :attr:`Graph.edge_attr`
		
		:return: the graph
		:rtype: Graph

		>>> g = GraphM()
		>>> print(g)
		dim 0
		matrix 
		nodes 
		
		>>> g = GraphM(boolean=['00010', '01100', '10000', '10100', '00000'], nodes='a,b,c,d,e,f,g,h,i,j', node_style='int')
		>>> print(g)
		dim 5
		matrix [[0, 0, 0, 1, 0], [0, 1, 1, 0, 0], [1, 0, 0, 0, 0], [1, 0, 1, 0, 0], [0, 0, 0, 0, 0]]
		nodes a b c d e
		"""
		self.matrix = []
		self.dim = 0
		self.layout = GraphM.layout.copy()
		
		# viz
		self.set_viz(**d)
		
		# matrix
		if 'boolean' in d:
			self.set_matrix_boolean(**d)
		elif 'binary' in d:
			self.set_matrix_binary(**d)
		elif ('nodes' in d) or ('edges' in d):
			self.set_matrix_ne(**d)

	def __repr__(self) -> str:
		""" Return the dimension and the length of nodes if exists
		
		:return: the dimension and the length of nodes

		>>> g = GraphM()
		>>> repr(g)
		'dim=0 nodes=0'
		
		>>> g = GraphM(boolean=['00010', '01100', '10000', '10100', '00000'], nodes='aa,bbb,c,d,e,f,g,h,i,j', node_style='int')
		>>> repr(g)
		'dim=5 nodes=5'
		"""
		return f"dim={self.dim}" + f" nodes={len(self.viz.nodes()) if self.viz else 0}"
	
	def __str__(self) -> str:
		""" Return the dimension, nodes and matrix if exists
		
		:return: the dimension, matrix and the length of nodes
		
		>>> g = GraphM()
		>>> print(g)
		dim 0
		matrix 
		nodes 
		
		>>> g = GraphM(boolean=['00010', '01100', '10000', '10100', '00000'], nodes='a,b,c,d,e,f,g,h,i,j', node_style='int')
		>>> print(g)
		dim 5
		matrix [[0, 0, 0, 1, 0], [0, 1, 1, 0, 0], [1, 0, 0, 0, 0], [1, 0, 1, 0, 0], [0, 0, 0, 0, 0]]
		nodes a b c d e
		"""
		return f"dim {self.dim}" \
			+ f"\nmatrix {self.matrix if self.matrix else ''}" \
			+ f"\nnodes {self.str_nodes()}"

	def convert_edges(self, edges: iter) -> list:
		""" Convert edges to list of single elements
		
		:param list edges: edges of graph
		
		:return: edges in single elements
		:rtype: list
		"""
		# str
		if isinstance(edges, str):
			edges = [(a, b) for a, b in edges.split(',')]
		# iter(str)
		elif isinstance(edges[0], str):
				edges = [[i for i in edge.split('-')] for edge in edges]
		# dict
		elif isinstance(edges, dict):
			edges = [(str(a), str(b)) for a, b in edges.items()]
		else:
			edges = [(str(a), str(b)) for a, b in edges]
		
		return edges

	def convert_nodes(self, nodes: iter) -> list:
		""" Convert edges to list of single elements
		
		:param list edges: edges of graph
		
		:return: edges in single elements
		:rtype: list
		"""
		if isinstance(nodes, str):
			nodes = nodes.split(',')
		nodes = [str(i) for i in nodes]
		
		return nodes

	def draw(self, path: str="files/tmp.png", ext: str='png', **d) -> None:
		""" Draw matrix graph to a file with the layout and fews options for test_graphviz:
			* file: str / 
			* layout: str / circo, dot, fdp, neato, osage, patchwork, twopi
		
		:param str path=files/tmp.png: path to write the file
		:param str ext='png': format of the file
		
			options:
				**dot** / circo, dot, fdp, neato, osage, patchwork, twopi
			
			full options regadless implementaion :
				**png** / canon, cmap, cmapx, cmapx_np, dia, dot, fig, gd, gd2, gif, hpgl, imap,
				imap_np, ismap, jpe, jpeg, jpg, mif, mp, pcl, pdf, pic, plain, plain-ext,
				png, ps, ps2, svg, svgz, vml, vmlz, vrml, vtx, wbmp, xdot, xlib
		
		:param dict \*\*d: options to specify the type of matrix
		
			for **viz**
			
			:label='G': (str) label for the graph
			:shape='circle': (str) shape of the node for the graph 
			:nodeFont='Arial': (str) font name for nodes
			:nodeColor='chocolate4': (str) font color for nodes
			:edgeColor='gray30': (str)  font color for edges

			for **nodes**
			
			:nodes: (iter(str)) names of nodes
			:node_style='str': (str) type of nodes name generation 'str' or 'int' 
		
		**example 1**
		
			>>> g = GraphM(nodes=['A','B','C','D','E'], edges=('AD','DA','DC','CA','BC','BB'))
			>>> g.draw("docs/src/files/graph3.png")
			
		.. IMAGE:: files/graph3.png
		
		.list(self.viz.graph_attr.items())
		
		**example 2**
		
			>>> g = GraphM(boolean=['00010', '01100', '10000', '10100', '00000'])
			>>> g.draw("docs/src/files/graph3.png")
			
		.. IMAGE:: files/graph3.png
		
		.
			
		**example 3**
		
			>>> g = GraphM(boolean=['00010', '01100', '10000', '10100', '00000'], node_style='int')
			>>> g.draw("docs/src/files/graph4.png")
			
		.. IMAGE:: files/graph4.png
		
		.
			
		**example 4**
		
			>>> g = GraphM(boolean=['00010', '01100', '10000', '10100', '00000'], nodes=['α','β','γ','δ','ε','ζ'])
			>>> g.draw("docs/src/files/graph5.png")
			
		.. IMAGE:: files/graph5.png
		
		.
		"""
		# viz
		self.update_viz_attrs(**d)
		
		# draw
		# TODO
		#self.viz.layout(prog=self.layout['prog'])
		self.viz.layout(**self.layout)
		self.viz.draw(path, ext)

	def generate_nodes(self, **d) -> list:
		""" Return nodes names generating with the type given
		
		:param dict \*\*d: containing options
		
			:node_style: (str) type of nodes name generation
				options: str, int
				default:  Graph.node_style
		
		:return: nodes names
		:rtype: list

		>>> g = GraphM(boolean=['00010', '01100', '10000', '10100', '00000'])
		>>> g.generate_nodes()
		['A', 'B', 'C', 'D', 'E']

		>>> g.generate_nodes(node_style='int')
		['0', '1', '2', '3', '4']
		"""
		# default
		node_style = d['node_style'] if 'node_style' in d else GraphM.node_style
			
		# characters
		if node_style == "str": 
			begin = ord('A')
			letters = [chr(begin + i) for i in range(26)]
			nodes = letters[:]
			c = 0
			while len(nodes) < self.dim:
				nodes.extend(letters[c]+s for s in letters)
				c += 1
			nodes = nodes[:self.dim]

		# numeric
		elif node_style == "int":
			nodes = [str(i) for i in range(self.dim)]
		else:
			raise ValueError("Wrong option for node_style: {node_style}")

		return nodes
		
	def init_viz_attrs(self) -> None:
		""" Set default viz attributes to drawing with default class attributes for viz
		
			See :attr:`Graph.layout`, :attr:`Graph.graph_attr`, :attr:`Graph.node_attr`, :attr:`Graph.edge_attr` in :class:`Graph`

		>>> g = GraphM(boolean=['00010', '01100', '10000', '10100', '00000'])
		>>> list(g.viz.graph_attr.items())
		[('directed', 'True'), ('label', 'G'), ('rankdir', 'TB'), ('ranksep', '0.5'), ('strict', 'False')]

		>>> g.viz.graph_attr.pop('label')
		'G'
		>>> list(g.viz.graph_attr.items())
		[('directed', 'True'), ('label', ''), ('rankdir', 'TB'), ('ranksep', '0.5'), ('strict', 'False')]
		
		>>> g.init_viz_attrs()
		>>> list(g.viz.graph_attr.items())
		[('directed', 'True'), ('label', 'G'), ('rankdir', 'TB'), ('ranksep', '0.5'), ('strict', 'False')]
		"""
		for attr_name in ('graph_attr', 'node_attr', 'edge_attr'):
			attr = getattr(GraphM, attr_name)
			attr_viz = getattr(self.viz, attr_name)
			attr_viz.update(attr)

	def int2str(self, line: int) -> str:
		""" Return string value of converted binary, string length is adjusted by to dim
	
		:param int line: line of boolean in integer representation
		
		:return: string of booleans
		:rtype: str

		>>> g = GraphM(binary=[1, 3, 8, 0])
		>>> g.int2str(7)
		'0111'
		"""
		s = bin(line)[2:]
		return s.rjust(self.dim, '0')

	def set_matrix_binary(self, **d) -> None:
		""" Set boolean matrix from binary matrix and nodes if given
		
		Get a binary matrix contains a list of integers
		
		:param dict \*\*d: containing matrix and optionally nodes
		
			:binary: (list) matrixM in format [int, ...]

			for **nodes**
			
			:nodes: (iter(str)) names of nodes
			:node_style='str': (str) type of nodes name generation 'str' or 'int' 
		
		>>> g = GraphM()
		>>> g.set_matrix_binary(binary=[1, 4, 2])
		>>> print(g)
		dim 3
		matrix [[0, 0, 1], [1, 0, 0], [0, 1, 0]]
		nodes A B C
		"""
		if not d['binary']:
			raise ValueError("Wrong empty matrix")

		matrix = d['binary']
		self.dim = len(matrix)
		self.matrix = [[int(n) for n in self.int2str(m)] for m in matrix]
		
		self.set_viz_nodes(**d)
		self.set_viz_edges(self.viz.nodes())

	def set_matrix_boolean(self, **d) -> None:
		""" Set boolean matrix with int 0/1 from boolean matrix and nodes if given
		
		:param dict \*\*d: containing matrix and optionally nodes
		
			:boolean: (list) matrix: matrix in formats [str, ...] or [[int,...], ...] or (str, ...) or ((int,...), ...) 

			for **nodes**
			
			:nodes: (iter(str)) names of nodes
			:node_style='str': (str) type of nodes name generation 'str' or 'int' 
	
		>>> g = GraphM(boolean=['00010', '01100', '10000', '10100', '00000'])
		>>> print(g)
		dim 5
		matrix [[0, 0, 0, 1, 0], [0, 1, 1, 0, 0], [1, 0, 0, 0, 0], [1, 0, 1, 0, 0], [0, 0, 0, 0, 0]]
		nodes A B C D E
		
		>>> g = GraphM(boolean=[['0','0','0','1'], ['0','0','1','0'], ['1','0','0','0'], ['1','0','1','0']])
		>>> print(g)
		dim 4
		matrix [[0, 0, 0, 1], [0, 0, 1, 0], [1, 0, 0, 0], [1, 0, 1, 0]]
		nodes A B C D
		
		>>> g = GraphM(boolean=[[0,0,0,1], [0,0,1,0], [0,0,0,1], [1,0,1,1]])
		>>> print(g)
		dim 4
		matrix [[0, 0, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1], [1, 0, 1, 1]]
		nodes A B C D
		"""
		matrix = d['boolean']
		if not matrix:
			raise ValueError("Wrong empty matrix")

		self.dim = len(matrix)
		if len(matrix[0]) != self.dim:
			raise ValueError("Matrix have to be square")
		
		self.matrix = [[int(matrix[m][n]) for n in range(self.dim)] for m in range(self.dim)]
		
		self.set_viz_nodes(**d)
		self.set_viz_edges(self.viz.nodes())

	def set_matrix_ne(self, **d) -> None:
		""" Set boolean matrix from nodes or edges
		
		.. NOTE:: if edges are given without nodes, the nodes are generate from edges automatically
		
		:param dict \*\*d: containing matrix and optionally nodes
		
			:edges: (iter) edges in format 'in,out' or [in, out] or (in, out)
			:nodes: (iter) names of nodes in iterable of strings
			:node_style='str': (str) type of nodes name generation 'str' or 'int' 

		>>> g = GraphM(nodes=['A','B','C','D','E'], edges=('AD','DA','DC','CA','BC','BB'))
		>>> print(g)
		dim 5
		matrix [[0, 0, 0, 1, 0], [0, 1, 1, 0, 0], [1, 0, 0, 0, 0], [1, 0, 1, 0, 0], [0, 0, 0, 0, 0]]
		nodes A B C D E
		
		>>> g = GraphM(edges=('AD','DA','DC','CA','BC','BB'))
		>>> print(g)
		dim 4
		matrix [[0, 0, 0, 1], [0, 1, 1, 0], [1, 0, 0, 0], [1, 0, 1, 0]]
		nodes A B C D
				
		>>> g = GraphM(nodes=['A','B','C','D','E'])
		>>> print(g)
		dim 5
		matrix [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
		nodes A B C D E
		"""
		nodes = d['nodes'] if 'nodes' in d else []
		edges = d['edges'] if 'edges' in d else []

		edges = self.convert_edges(edges)

		nodes_edges = {node for edge in edges for node in edge} if edges else set()
		if nodes:
			if nodes_edges - set(nodes):
				raise ValueError("nodes presents in edges and not in nodes given")
		else:
			nodes = list(nodes_edges)
			nodes.sort()
		
		# dim
		self.dim = len(nodes)
		# nodes
		self.set_viz_nodes(nodes=nodes, cut=False)
		
		# matrix
		self.matrix = [[0 for _ in range(self.dim)] for _ in range(self.dim)]
		nodes_rev = {node: i for i,node in enumerate(nodes)}
		for edgeIn, edgeOut in edges:
			self.matrix[nodes_rev[edgeIn]][nodes_rev[edgeOut]] = 1

		# edges
		self.set_viz_edges(nodes)

	def set_viz(self,**d) -> None:
		""" Set instance of :class:`pygraphviz.AGraph` with viz properties
		
		:param dict \*\*d: options to specify arguments to :class:`pygraphviz.AGraph`
		
			:layout: (dict) default attributes for graph layout, see :class:`Graph.layout`
			:graph_attr: (dict) default attributes for graph, see :attr:`Graph.graph_attr`
			:node_attr: (dict) default attributes for nodes, see :attr:`Graph.node_attr`
			:edge_attr: (dict) default attributes for edges, see :attr:`Graph.edge_attr`
		"""
		# TODO
		# graph_attr = Graph.graph_attr.copy()
		# if 'graph_attr' in d:
		# 	graph_attr.update(d['graph_attr'])
		# 	d.pop('graph_attr')
		
		self.viz = pygraphviz.AGraph()
		
		self.init_viz_attrs()
		self.update_viz_attrs(**d)

	def set_viz_edges(self, nodes: list=[]) -> None:
		""" Add edges to viz from arguments edges & nodes
		
		:param list nodes: nodes of graph

		>>> g = GraphM(boolean=['00010', '01100', '10000', '10100', '00000'])
		>>> g.viz.edges()
		[('A', 'D'), ('B', 'B'), ('B', 'C'), ('C', 'A'), ('D', 'C')]

		>>> g.set_viz_edges('a,b,c,d,e,f,g,h,j')
		>>> g.viz.edges()
		[('a', 'd'), ('d', 'c'), ('b', 'b'), ('b', 'c'), ('c', 'a')]
		"""
		# remove existing nodes
		self.viz.remove_edges_from(self.viz.edges())
		
		nodes = self.convert_nodes(nodes)
		
		for m in range(self.dim):
			for n in  range(self.dim):
				if self.matrix[m][n]:
					self.viz.add_edge(nodes[m], nodes[n])

	def set_viz_nodes(self, cut :bool=True, **d) -> None:
		""" Add nodes to viz from:
			#. dictionary if given in argument
			#. generated by self.generate_nodes()
		
			:param bool cut=False: if True reduce the number of nodes to the dimension of the graph
			:param dict \*\*d: options to specify arguments to :class:`pygraphviz.AGraph`
		
				:nodes: (iter(str)) names of nodes
				:node_style='str': (str) type of nodes name generation 'str' or 'int' 

		>>> g = GraphM(boolean=['00010', '01100', '10000', '10100', '00000'])
		>>> g.viz.nodes()
		['A', 'B', 'C', 'D', 'E']

		>>> g.set_viz_nodes(nodes='UU,V,X,Y,Z,T')
		>>> g.viz.nodes()
		['UU', 'V', 'X', 'Y', 'Z']
		"""
		# remove existing nodes
		self.viz.remove_nodes_from(self.viz.nodes())
		
		if 'nodes' in d:
			if not hasattr(self, 'dim'):
				raise ValueError("The graph has no dimension")
			
			nodes = self.convert_nodes(d['nodes'])
			
			if len(nodes) < self.dim:
				raise ValueError(f"The number of names: {nodes} is less than the number of nodes: {self.dim}")
			
			# cut nodes to graph dimension
			if cut:
				nodes = nodes[:self.dim]
		else:
			nodes = self.generate_nodes(**d)

		# add to viz
		for node in nodes:
			self.viz.add_node(node)

	def str(self) -> str:
		""" Return the dimension, matrix and the length of nodes if exists
		
		:return: the dimension, matrix and the length of nodes

		>>> g = GraphM()
		>>> print(g.str())
		dim 0
		nodes 
		matrix
		
		>>> g = GraphM(boolean=['00010', '01100', '10000', '10100', '00000'], nodes='a,b,c,d,e,f,g,h,i', node_style='int')
		>>> print(g.str())
		dim 5
		nodes a b c d e
		matrix
		00010 
		01100 
		10000 
		10100 
		00000
		"""
		return f"dim {self.dim}" \
			+ f"\nnodes {self.str_nodes()}" \
			+ "\nmatrix" + (f"\n{self.str_matrix()}" if self.str_matrix() else "")

	def str_matrix(self):
		""" Return a representation of matrix in 2 dimensions
		
		:return: a representation of matrix in 2 dimensions
		:rtype: str
		
		>>> g = GraphM(boolean=['00010', '01100', '10000', '10100', '00000'], nodes=['u','v','w','x','y','z'])
		>>> print(g.str_matrix())
		00010 
		01100 
		10000 
		10100 
		00000
		"""
		return ' \n'.join(''.join(str(i) for i in line) for line in self.matrix) if self.matrix else ""

	def str_nodes(self):
		""" Return a representation of nodes to string
		
		:return: a representation of nodes
		:rtype: str
		
		>>> g = GraphM(boolean=['00010', '01100', '10000', '10100', '00000'], nodes=['α','β','γ','δ','ε','ζ'])
		>>> g.str_nodes()
		'α β γ δ ε'
		"""
		return ' '.join(self.viz.nodes()) if self.viz else ""

	def update_viz_attrs(self, **d) -> None:
		""" Add viz attributes to drawing
		
		:param dict \*\*d: options to specify arguments to :class:`pygraphviz.AGraph`
		
			See :attr:`Graph.layout`, :attr:`Graph.graph_attr`, :attr:`Graph.node_attr`, :attr:`Graph.edge_attr` in :class:`Graph`

		>>> g = GraphM(boolean=['00010', '01100', '10000', '10100', '00000'])
		>>> list(g.viz.graph_attr.items())
		[('directed', 'True'), ('label', 'G'), ('rankdir', 'TB'), ('ranksep', '0.5'), ('strict', 'False')]

		>>> g.update_viz_attrs(graph_attr={'label':'new', 'margin':0.2})
		>>> list(g.viz.graph_attr.items())
		[('directed', 'True'), ('label', 'new'), ('margin', '0.2'), ('rankdir', 'TB'), ('ranksep', '0.5'), ('strict', 'False')]
		"""
		if 'layout' in d:
			self.layout.update(d['layout'])
		
		for attr_name in ('graph_attr', 'node_attr', 'edge_attr'):
			if attr_name in d:
				attr_viz = getattr(self.viz, attr_name)
				attr_viz.update(d[attr_name])

