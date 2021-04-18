from graphm import Graph


class GraphPert(Graph):
	""" Manage Pert graph.
	
	Data is directly stored in :class:`pygraphviz.Agraph`

	Drawing is supported by writing file in 'dot' format 
	(others layout are availables :class:`GraphM.layout`)
	
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
		self.set_edges(edges)



