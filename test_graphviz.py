import pygraphviz as pgv

#G = pgv.AGraph()
G = pgv.AGraph(strict=False, directed=True, rankdir="TD", ranksep="0.5")
G.graph_attr["label"] = "My first graphm"
G.node_attr["shape"] = "circle"
G.edge_attr["color"] = "red"

G.add_node("a")  # adds node 'a'
G.add_edge("a", "b", taillabel = "first")  # adds edge 'b'-'c' (and also nodes 'b', 'c')
G.add_edge("a", "b", "second", color="green")  # adds edge 'b'-'c' (and also nodes 'b', 'c')
G.add_edge("b", "c")  # adds edge 'b'-'c' (and also nodes 'b', 'c')
G.add_edge("a", "d")  # adds edge 'b'-'c' (and also nodes 'b', 'c')
G.add_edge("d", "e")  # adds edge 'b'-'c' (and also nodes 'b', 'c')


G.layout()  # default to neato
G.layout(prog="dot")  # use dot

s = G.string()
print(s)

G.draw("graphviz.png")
