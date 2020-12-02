import networkx as nx
G = nx.Graph()
# Get nodes
G.add_nodes_from(["Brian",2,3,4,5,6,7,8,9,10,11,12])
# Ged edges
G.add_edges_from([("Brian",6),("Brian",3),(6,3),(2,3),(10,11),(11,12),(10,12)])

cliques = nx.find_cliques(G)
for c in cliques:
    print(c)
