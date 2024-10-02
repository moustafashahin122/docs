import networkx as nx
from networkx.algorithms.cycles import simple_cycles

# Parse the graph from the .dot file
G = nx.drawing.nx_pydot.read_dot("module.gv")

# Convert the graph into a directed graph
DG = nx.DiGraph(G)

# Find cycles in the graph
cycles = list(simple_cycles(DG))

# Print the cycles

for cycle in cycles:
    print(" -> ".join(cycle))