from graphm import Graph


class GraphPert(Graph):
	""" Manage graph with matrix.
	
	Representation of graph with the export capacity in dot format
	
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
	
	:var pygraphviz.AGraph viz: manage drawing in dot format with :class:`pygraphviz.AGraph`

	:var dict layout: graph layout, see :class:`GraphPert.layout`

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
	
	def __init__(self, **d) -> 'GraphPert':
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
			:node_style: (str) type of nodes name generation 'str' or 'int' 
						
				default: :class:`GraphPert.node_style`

			for **viz**
			
			:layout: (dict) default attributes for graph layout, see :class:`GraphPert.layout`
			:graph_attr: (dict) default attributes for graph, see :attr:`GraphPert.graph_attr`
			:node_attr: (dict) default attributes for nodes, see :attr:`GraphPert.node_attr`
			:edge_attr: (dict) default attributes for edges, see :attr:`GraphPert.edge_attr`
		
		:return: the graph
		:rtype: GraphPert

		>>> g = GraphPert()
		>>> print(g)
		nodes=0 edges=0
		nodes 
		edges 
		
		>>> g = GraphPert(boolean=['00010', '01100', '10000', '10100', '00000'], nodes='a,b,c,d,e,f,g,h,i,j', node_style='int')
		>>> print(g)
		nodes=5 edges=6
		nodes a b c d e
		edges a-d b-b b-c c-a d-a d-c
		"""
		self.layout = GraphPert.layout.copy()
		
		# viz
		self.set_viz(**d)
		
		# matrix
		if 'boolean' in d:
			self.set_matrix_boolean(**d)
		elif 'binary' in d:
			self.set_matrix_binary(**d)
		elif ('nodes' in d) or ('edges' in d):
			self.set_nodes_edges(**d)



