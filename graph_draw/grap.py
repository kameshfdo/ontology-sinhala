import rdflib
from rdflib.plugins.sparql import prepareQuery
import matplotlib.pyplot as plt
import networkx as nx

# Load the ontology file into rdflib
g = rdflib.Graph()
g.parse("new-ontology-v1.owl", format="xml")

# Create a NetworkX graph from the ontology
G = nx.Graph()

# Iterate over triples in the graph and add nodes and edges to NetworkX graph
for s, p, o in g:
    G.add_node(s, label=str(s))
    G.add_node(o, label=str(o))
    G.add_edge(s, o, label=str(p))

# Draw the graph using Matplotlib and NetworkX
plt.figure(figsize=(12, 12))
nx.draw(G, with_labels=True, node_size=3000, node_color="yellow", font_size=10, font_weight="bold")
plt.title("Ontology Graph")
plt.show()
