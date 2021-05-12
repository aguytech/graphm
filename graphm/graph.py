'''
Created on Apr 26, 2021

@author: salem Aguemoun
'''
import pygraphviz
import graphm.matrixbinary
import graphm.matrixboolean
MatrixBinary = graphm.matrixbinary.MatrixBinary
MatrixBoolean = graphm.matrixboolean.MatrixBoolean

class Graph(object):
	""" Manage graph with matrix.
	
	Data is directly stored in :class:`pygraphviz.Agraph`

	Drawing is supported by writing file in 'dot' format 
	(others available layouts are :class:`GraphM.layout`)
	
	:var str node_style: default style to generate nodes
	
		**str** / str, int
	
	:var dict layout: default attributes for graph layout, see :class:`pygraphviz.Agraph`
	
		:prog: (str) type of programmed layout
			
			**dot** / neato, dot, twopi, circo, fdp, nop

	:var str sep: default separator for elements in string like optionally for node, edges
	
		**,**
	
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
	
	:var pygraphviz.AGraph viz: manage drawing in dot format with :class:`pygraphviz.AGraph`

	:var dict layout: graph layout, see :class:`Graph.layout`

	**Graph for the majority of examples** 
	
	.. IMAGE:: files/graph_draw2.svg
	
	"""
	node_style = 'str'
	layout = {
		'prog' : 'dot',
		}
	sep = ','
	graph_attr = {
		'label' : 'G',
		'directed' : True,
		'rankdir' : "TB",
		'ranksep' : 0.5,
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
						
		 		| **matrix** get a matrix (None is default value)
		 		| **boolean** get a boolean matrix
				| **binary** get a binary matrixM and dimN
		
			* classical
						
				| **edges** get list of edges and of optionally nodes
				| **nodes** optional, get list of nodes

		:param dict \*\*d: options to specify the type of matrix
		
			:matrix: (list[int]) matrix in [str, ...] or [[int,...], ...] or (str, ...) or ((int,...), ...)
			:boolean: (list[int]) matrix in [str, ...] or [[int,...], ...] or (str, ...) or ((int,...), ...) or class MatrixBoolean
			:binary: matrixM in [int, ...] or class MatrixBinary
			:edges: (tuple/list) list of edges in tuple format (nodeIn, nodeOut)
			:nodes: (tuple/list) optional list of nodes
			:sep: (str) separator for elements in string like optionally for node, edges,  see :class:`Graph.sep`

			for **nodes**
			
			:nodes: (iter(str)) names of nodes
			:node_style: (str) node name generation style: 'str' or 'int' 
				
				default: :class:`Graph.node_style`
			
			for **viz**
			
			:layout: (dict) default attributes for graph layout, see :class:`Graph.layout`
			:graph_attr: (dict) default attributes for graph, see :attr:`Graph.graph_attr`
			:node_attr: (dict) default attributes for nodes, see :attr:`Graph.node_attr`
			:edge_attr: (dict) default attributes for edges, see :attr:`Graph.edge_attr`
		
		:return: the graph
		:rtype: Graph

		>>> g = Graph()
		>>> print(g)
		nodes=0 edges=0
		nodes 
		edges 
		
		>>> g = Graph(boolean=['00010', '01100', '10000', '10100', '00000'], nodes='a,b,c,d,e,f,g,h,i,j', node_style='int')
		>>> print(g)
		nodes=5 edges=6
		nodes a b c d e
		edges a-d b-b b-c c-a d-a d-c
		"""
		# TODO: remove
		#self.layout = Graph.layout.copy()
		#self.sep = d['sep'] if 'sep' in d else Graph.sep
		
		# viz
		self.set_viz(**d)

		# call the good method to initialize object
		initialized = False
		for attr in ('matrix', 'boolean', 'binary', 'pert'):
			if attr in d:
				self._call_init(f"set_from_{attr}", **d)
				initialized = True
				break
		if not initialized and ('nodes' in d or 'edges' in d):
			self._call_init('set_from_nodes_edges', **d)

	def __repr__(self) -> str:
		""" Return the number of nodes and of edges
		
		:return: the dimension and the length of nodes

		>>> g = Graph()
		>>> repr(g)
		'nodes=0 edges=0'
		
		>>> g = Graph(boolean=['00010', '01100', '10000', '10100', '00000'], nodes='aa,bbb,c,d,e,f,g,h,i,j', node_style='int')
		>>> repr(g)
		'nodes=5 edges=6'
		"""
		return f"nodes={self.viz.number_of_nodes()} edges={self.viz.number_of_edges()}"
	
	def __str__(self) -> str:
		""" Return the representation of nodes, edges and list of nodes and edges
		
		:return: the numbers of nodes & edges in a first line and list of nodes & edges in a second line
		
		>>> g = Graph()
		>>> print(g)
		nodes=0 edges=0
		nodes 
		edges 
		
		>>> g = Graph(boolean=['00010', '01100', '10000', '10100', '00000'], nodes='a,b,c,d,e,f,g,h,i,j', node_style='int')
		>>> print(g)
		nodes=5 edges=6
		nodes a b c d e
		edges a-d b-b b-c c-a d-a d-c
		"""
		return repr(self) \
			+ "\n" + f"nodes {self.str_nodes()}" \
			+ "\n" + f"edges {self.str_edges()}"

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
		
	def add_nodes(self, cut :bool=False, **d) -> list:
		""" Add nodes to viz from:
			#. given in argument
			#. generated by self.generate_nodes()
		
			:param bool cut=False: if True reduce the number of nodes to the dimension of the graph
			:param dict \*\*d: options to specify arguments to :class:`pygraphviz.AGraph`
		
				:nodes: (iter(str)) names of nodes
				:dim: (int) number of nodes (needed if nodes are empty)
				:node_style: (str) node name generation style: 'str' or 'int' 
						
					default: :class:`Graph.node_style`
		
		:return: nodes generated after settings
		:rtype: list

		>>> g = Graph(boolean=['00010', '01100', '10000', '10100', '00000'])
		>>> g.viz.nodes()
		['A', 'B', 'C', 'D', 'E']

		>>> g.set_nodes(nodes='UU,V,X,Y,Z,T')
		>>> g.viz.nodes()
		['UU', 'V', 'X', 'Y', 'Z', 'T']
		"""
		if 'nodes' in d:
			nodes = self.convert_nodes(d['nodes'])
			
			# for matrix, need to have enough nodes
			if cut:
				if not 'dim' in d:
					raise ValueError("Missing index 'dim' in dictionary of arguments")
				dim = d['dim']
				if len(nodes) < dim:
					raise ValueError(f"The number of names: {len(nodes)} is less than the number of nodes: {dim}")
			
			# cut nodes to graph dimension
			if cut:
				nodes = nodes[:dim]
		else:
			nodes = self.generate_nodes(**d)

		# add to viz
		self.viz.add_nodes_from(nodes)
		
		return nodes

	def convert_edges(self, edges: iter) -> list:
		""" Convert edges to list of single elements
		
		:param list edges: edges of graph
		
		:return: edges in single elements
		:rtype: list
		"""
		if not edges:
			return []
		
		# str
		if isinstance(edges, str):
			edges = [[i for i in line.split('-')] for line in edges.split(',')]
		# iter(str)
		elif isinstance(edges[0], str):
				edges = [[i for i in edge.split('-')] for edge in edges]
		# dict
		elif isinstance(edges, dict):
			edges = [(str(d[0]), str(d[1]), str(d[:2])) for d in edges.items()]
		else:
			if len(edges[0]) == 3:
				edges = [(str(u), str(v), str(l)) for u,v, l in edges]
			else:
				edges = [(str(d[0]), str(d[1]), str(d[2:] if d[2:] else '')) for d in edges]
		
		return edges

	def convert_nodes(self, nodes: iter) -> list:
		""" Convert nodes to list of single elements
		
		:param list nodes: nodes of graph
		
		:return: nodes in single elements
		:rtype: list
		"""
		if not nodes:
			return []
		
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
			
			full options according to its implementation:
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
			:node_style: (str) node name generation style: 'str' or 'int' 
			
				default: :class:`Graph.node_style`
		
		**example 1**
		
			>>> g = Graph(nodes=['a','bb','c','d','e'], edges=('a-d','d-a','d-c','c-a','bb-c','bb-bb'))
			>>> g.draw("docs/src/files/graph_draw.svg", ext="svg")
			
		.. IMAGE:: files/graph_draw.svg
		
		.list(self.viz.graph_attr.items())
		
		**example 2**
		
			>>> g = Graph(boolean=['00010', '01100', '10000', '10100', '00000'])
			>>> g.draw("docs/src/files/graph_draw2.svg", ext="svg")
			
		.. IMAGE:: files/graph_draw2.svg
		
		.
			
		**example 3**
		
			>>> g = Graph(boolean=['00010', '01100', '10000', '10100', '00000'], node_style='int')
			>>> g.draw("docs/src/files/graph_draw3.svg", ext="svg")
			
		.. IMAGE:: files/graph_draw3.svg
		
		.
			
		**example 4**
		
			>>> g = Graph(boolean=['00010', '01100', '10000', '10100', '00000'], nodes=['α','β','γ','δ','ε','ζ'])
			>>> g.draw("docs/src/files/graph_draw4.svg", ext="svg")
			
		.. IMAGE:: files/graph_draw4.svg
		
		.
		"""
		# viz
		self.update_attrs(**d)
		
		# draw
		self.viz.layout(**self.layout)
		self.viz.draw(path, ext)

	def generate_nodes(self, dim: int, **d) -> list:
		""" Return nodes names generating with the type given

		:param int dim: dimension of square matrix
		:param dict \*\*d: containing options
		
			:dim: (int) number of nodes
			:node_style: (str) node name generation style: 'str' or 'int' 
						
				default: :class:`Graph.node_style`
		
		:return: nodes names
		:rtype: list

		>>> g = Graph(boolean=['00010', '01100', '10000', '10100', '00000'])
		>>> g.generate_nodes(5)
		['A', 'B', 'C', 'D', 'E']

		>>> g.generate_nodes(5, node_style='int')
		['0', '1', '2', '3', '4']
		"""
		if dim < 1:
			raise ValueError(f"Wrong dimension: {dim}, must be more than 1")
		
		# default
		node_style = d['node_style'] if 'node_style' in d else Graph.node_style
			
		# characters
		if node_style == "str": 
			begin = ord('A')
			letters = [chr(begin + i) for i in range(26)]
			nodes = letters[:]
			c = 0
			while len(nodes) < dim:
				nodes.extend(letters[c]+s for s in letters)
				c += 1
			nodes = nodes[:dim]

		# numeric
		elif node_style == "int":
			nodes = [str(i) for i in range(dim)]
		else:
			raise ValueError("Wrong option for node_style: {node_style}")

		return nodes
		
	def init_attrs(self) -> None:
		""" Set default viz attributes to drawing with default class attributes for viz
		
			See :attr:`Graph.layout`, :attr:`Graph.graph_attr`, :attr:`Graph.node_attr`, :attr:`Graph.edge_attr` in :class:`Graph`

		>>> g = Graph(boolean=['00010', '01100', '10000', '10100', '00000'])
		>>> list(g.viz.graph_attr.items())
		[('directed', 'True'), ('label', 'G'), ('rankdir', 'TB'), ('ranksep', '0.5'), ('strict', 'False')]

		>>> g.viz.graph_attr.pop('label')
		'G'
		>>> list(g.viz.graph_attr.items())
		[('directed', 'True'), ('label', ''), ('rankdir', 'TB'), ('ranksep', '0.5'), ('strict', 'False')]
		
		>>> g.init_attrs()
		>>> list(g.viz.graph_attr.items())
		[('directed', 'True'), ('label', 'G'), ('rankdir', 'TB'), ('ranksep', '0.5'), ('strict', 'False')]
		"""
		for attr_name in ('graph_attr', 'node_attr', 'edge_attr'):
			attr = getattr(self, attr_name)
			attr_viz = getattr(self.viz, attr_name)
			attr_viz.update(attr)

	def reset_edges(self, **d) -> None:
		""" remove all edges in viz
		"""
		# remove existing nodes
		self.viz.remove_edges_from(self.viz.edges())
		
	def reset_nodes(self, **d) -> None:
		""" remove all nodes in viz
		"""
		# remove existing nodes
		self.viz.remove_nodes_from(self.viz.nodes())

	def set_edges(self, **d) -> None:
		""" Add edges to viz from:
		"""
		self.reset_edges(**d)
		self.add_edges(**d)

	def set_nodes(self, **d) -> None:
		""" Set nodes to viz from:
		"""
		self.reset_nodes(**d)
		self.add_nodes(**d)

	def set_from_binary(self, binary: iter, **d) -> None:
		""" Set viz graph from binary matrix and nodes if given
		
		Get a binary matrixN containing rows of integers
		
		:param iter binary: binary square matrix containing matrixM in format [int, ...]
		:param dict \*\*d: containing optionally nodes, node_style
		
			:nodes: (iter(str)) names of nodes
			:dim: (int) number of nodes (needed if nodes are empty)
			:node_style: (str) node name generation style: 'str' or 'int' 
						
				default: :class:`Graph.node_style`
		
		>>> g = Graph()
		>>> g.set_from_binary(binary=[1, 4, 2])
		>>> print(g)
		nodes=3 edges=3
		nodes A B C
		edges A-C B-A C-B
		"""
		if isinstance(binary, MatrixBinary):
			matrix = binary.matrixM
		else:
			matrix = binary

		if not matrix:
			raise ValueError("Wrong empty matrix")

		dim = len(matrix)
		self.set_nodes(dim=dim, cut=True, **d)
		nodes = self.viz.nodes()

		matrixS = [MatrixBinary.get_int2str(line, dim) for line in matrix]
		edges = [(nodes[m], nodes[n]) for m in range(dim) for n in range(dim) if matrixS[m][n] == '1']
		
		self.set_edges(edges=edges)

	def set_from_boolean(self, boolean: iter, **d) -> None:
		""" Set viz graph from boolean matrix and nodes if given.
		
		Get a boolean matrix containing 2 dimensions of rows and columns.
		Support several formats.
			
		:param iter boolean: boolean square matrix in formats [str, ...] or [[int,...], ...] or (str, ...) or ((int,...), ...) 
		:param dict \*\*d: containing matrix and optionally nodes, node_style
		
			:nodes: (iter(str)) names of nodes
			:dim: (int) number of nodes (needed if nodes are empty)
			:node_style: (str) node name generation style: 'str' or 'int' 
						
				default: :class:`Graph.node_style`
		
		>>> g = Graph(boolean=['00010', '01100', '10000', '10100', '00000'])
		>>> print(g)
		nodes=5 edges=6
		nodes A B C D E
		edges A-D B-B B-C C-A D-A D-C
		
		>>> g = Graph(boolean=[['0','0','0','1'], ['0','0','1','0'], ['1','0','0','0'], ['1','0','1','0']])
		>>> print(g)
		nodes=4 edges=5
		nodes A B C D
		edges A-D B-C C-A D-A D-C
		
		>>> g = Graph(boolean=[[0,0,0,1], [0,0,1,0], [0,0,0,1], [1,0,1,1]])
		>>> print(g)
		nodes=4 edges=6
		nodes A B C D
		edges A-D B-C C-D D-A D-C D-D
		"""
		if isinstance(boolean, MatrixBoolean):
			matrix = boolean.matrix
		else:
			matrix = boolean
			
		if not matrix:
			raise ValueError("Wrong empty matrix")
		
		dim = len(matrix)
		self.set_nodes(dim=dim, cut=True, **d)
		nodes = self.viz.nodes()

		matrixS = [[str(matrix[m][n]) for n in range(dim)] for m in range(dim)]
		edges = [(nodes[m], nodes[n]) for m in range(dim) for n in range(dim) if matrixS[m][n] != '0']
		
		self.set_edges(edges=edges)

	def set_from_matrix(self, matrix: iter, **d) -> None:
		""" Set viz graph from a common matrix and nodes if given.
		
		Get a common matrix containing 2 dimensions of rows and columns.
		(default value is None)
		Support several formats.
			
		:param iter matrix: square matrix in formats [[int,...], ...] or ((int,...), ...) 
		:param dict \*\*d: containing matrix and optionally nodes, node_style
		
			:nodes: (iter(str)) names of nodes
			:dim: (int) number of nodes (needed if nodes are empty)
			:node_style: (str) node name generation style: 'str' or 'int' 
						
				default: :class:`Graph.node_style`
		
		>>> g = Graph(matrix=((None,None,None,2), (None,None,5,None), (None,None,None,10), (7,None,2,3)))
		>>> print(g)
		nodes=4 edges=6
		nodes A B C D
		edges A-D B-C C-D D-A D-C D-D
		
		>>> g = Graph(matrix=[[None,None,None,2], [None,None,5,None], [None,None,None,10], [7,None,2,3]], node_style='int')
		>>> print(g)
		nodes=4 edges=6
		nodes 0 1 2 3
		edges 0-3 1-2 2-3 3-0 3-2 3-3
		"""
		if not matrix:
			raise ValueError("Wrong empty matrix")
		
		dim = len(matrix)
		self.set_nodes(dim=dim, cut=True, **d)
		nodes = self.viz.nodes()

		edges = [(nodes[m], nodes[n], matrix[m][n]) for m in range(dim) for n in range(dim) if matrix[m][n] != None]
		
		self.set_edges(edges=edges)

	def set_from_nodes_edges(self, **d) -> None:
		""" Set the graph from both nodes and edges passed as arguments 
		
		.. NOTE::
		
			if edges are given without nodes, the nodes are generated automatically from edges
			
			if the number of nodes given is greater than those present in the edges, they are added to the graph
		
		:param dict \*\*d: containing matrix and optionally nodes
		
			:edges: (iter) edges in format 'in,out' or [in, out] or (in, out)
			:nodes: (iter) names of nodes in iterable of strings
			:node_style: (str) node name generation style: 'str' or 'int' 
						
				default: :class:`Graph.node_style`

		>>> g = Graph(nodes=['A','B','C','D','E'], edges=('A-D','D-A','D-C','C-A','B-C','B-B'))
		>>> print(g)
		nodes=5 edges=6
		nodes A B C D E
		edges A-D B-B B-C C-A D-A D-C
		
		>>> g = Graph(nodes=['A','B','C','X','Y'], edges=('A-D,D-A,D-C,C-A,B-C,B-B,E-F,E-G,B-I'))
		>>> print(g)
		nodes=10 edges=9
		nodes A B C D E F G I X Y
		edges A-D B-B B-C B-I C-A D-A D-C E-F E-G
				
		>>> g = Graph(edges=('A-D,D-A,D-C,C-A,B-C,B-B'))
		>>> print(g)
		nodes=4 edges=6
		nodes A B C D
		edges A-D B-B B-C C-A D-A D-C
				
		>>> g = Graph(nodes=['A','B','C','D','E'])
		>>> print(g)
		nodes=5 edges=0
		nodes A B C D E
		edges 
		"""
		nodes = d.pop('nodes') if 'nodes' in d else []
		edges = d['edges'] if 'edges' in d else []

		edges = self.convert_edges(edges)

		nodes_edges = {node for edge in edges for node in edge} if edges else set()
		if nodes:
			nodes = self.convert_nodes(nodes)
			nodes = list(nodes_edges | set(nodes))
			nodes.sort()
		else:
			nodes = list(nodes_edges)
			nodes.sort()
		
		# dim
		dim = len(nodes)
		# nodes
		self.set_nodes(dim=dim, nodes=nodes, **d)
		# edges
		self.set_edges(edges=edges)

	def set_viz(self,**d) -> None:
		""" Set instance of :class:`pygraphviz.AGraph` with viz properties
		
		:param dict \*\*d: options to specify arguments to :class:`pygraphviz.AGraph`
		
			:layout: (dict) default attributes for graph layout, see :class:`Graph.layout`
			:graph_attr: (dict) default attributes for graph, see :attr:`Graph.graph_attr`
			:node_attr: (dict) default attributes for nodes, see :attr:`Graph.node_attr`
			:edge_attr: (dict) default attributes for edges, see :attr:`Graph.edge_attr`
		"""
		# Need to give graph_attr in __init__, for at least 'strict'
		# TODO: remove
		#graph_attr = Graph.graph_attr.copy()
		#if 'graph_attr' in d:
		#	graph_attr.update(d['graph_attr'])
		if 'graph_attr' in d:
			self.graph_attr.update(d['graph_attr'])
		
		self.viz = pygraphviz.AGraph(**self.graph_attr)
		
		# TODO: remove
		self.init_attrs()
		self.update_attrs(**d)

	def add_edges(self, edges: iter) -> None:
		""" Add edges to viz
		
			:param iter edges: edges of graph

		>>> g = Graph(boolean=['00010', '01100', '10000', '10100', '00000'])
		>>> g.viz.nodes()
		['A', 'B', 'C', 'D', 'E']

		>>> g.set_nodes(nodes='UU,V,X,Y,Z,T')
		>>> g.viz.nodes()
		['UU', 'V', 'X', 'Y', 'Z', 'T']
		
		>>> g.viz.nodes()
		['UU', 'V', 'X', 'Y', 'Z', 'T']
		"""
		# add to viz
		edges = self.convert_edges(edges)
		for u, v, l in edges:
			self.viz.add_edge(u, v, label=l)

	def str_nodes(self):
		""" Return a representation of nodes to string
		
		:return: a representation of nodes
		:rtype: str
		
		>>> g = Graph(boolean=['00010', '01100', '10000', '10100', '00000'], nodes=['α','β','γ','δ','ε','ζ'])
		>>> g.str_nodes()
		'α β γ δ ε'
		"""
		return  ' '.join(self.viz.nodes()) if self.viz.nodes else ''

	# TODO
	def str_edges(self):
		""" Return a representation of nodes to string
		
		:return: a representation of nodes
		:rtype: str
		
		>>> g = Graph(boolean=['00010', '01100', '10000', '10100', '00000'], nodes=['α','β','γ','δ','ε','ζ'])
		>>> g.str_nodes()
		'α β γ δ ε'
		"""
		return ' '.join(i+'-'+j for i,j in self.viz.edges()) if self.viz.edges else ''

	def update_attrs(self, **d) -> None:
		""" Add viz attributes to drawing
		
		:param dict \*\*d: options to specify arguments to :class:`pygraphviz.AGraph`
		
			See :attr:`Graph.layout`, :attr:`Graph.graph_attr`, :attr:`Graph.node_attr`, :attr:`Graph.edge_attr` in :class:`Graph`

		>>> g = Graph(boolean=['00010', '01100', '10000', '10100', '00000'])
		>>> list(g.viz.graph_attr.items())
		[('directed', 'True'), ('label', 'G'), ('rankdir', 'TB'), ('ranksep', '0.5'), ('strict', 'False')]

		>>> g.update_attrs(graph_attr={'label':'new', 'margin':0.2})
		>>> list(g.viz.graph_attr.items())
		[('directed', 'True'), ('label', 'new'), ('margin', '0.2'), ('rankdir', 'TB'), ('ranksep', '0.5'), ('strict', 'False')]
		"""
		if 'layout' in d:
			self.layout.update(d['layout'])
		
		for attr_name in ('graph_attr', 'node_attr', 'edge_attr'):
			if attr_name in d:
				attr_viz = getattr(self.viz, attr_name)
				attr_viz.update(d[attr_name])


