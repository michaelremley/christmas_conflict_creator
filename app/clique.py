import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

def make_seating(people, edges, chaotic = True):

    #people = ["Sarah","Michael","Kristtiya","Katie","Turkey","Sam","Elmo","JackBlack","Muffin"]
    #edges = [("Turkey","Sam"),("Sarah","Turkey"),("Sam","Sarah"),("Michael","Kristtiya"),("Elmo","JackBlack")]
    num_people = len(people)
    G = nx.Graph()
    # Get nodes
    G.add_nodes_from(people)
    # Get edges, people who agree to not eat meat
    G.add_edges_from(edges)

    S = nx.Graph()
    S.add_nodes_from(range(1,num_people))
    if (num_people % 2): # Odd number of people
        table_adjacency = [(a,a+1) for a in range(1,num_people-1)] # Connect into cycle
        table_adjacency.extend([(a,num_people-a) for a in range(1,int((num_people-1)/2))]) # Connect across the table
        table_adjacency = list(set(table_adjacency)) # Removes duplicated connections
        table_adjacency.extend([(1,num_people),(num_people,num_people-1)])
        seat_positions = {k: np.asarray([k,0.5]) for k in range(1,1+int((num_people-1)/2))} # Seat the upper row
        seat_positions.update({k: np.asarray([num_people-k,0]) for k in range(int((num_people-1)/2)+1,num_people)}) # Seat the lower row
        seat_positions.update({num_people: np.asarray([-0.25,0.25])}) # Seat odd person at end of table
    else:
        table_adjacency = [(a,a+1) for a in range(1,num_people)] # Connect into cycle
        table_adjacency.extend([(a,num_people-a+1) for a in range(1,int(num_people/2))]) # Connect across the table
        table_adjacency = list(set(table_adjacency)) # Removes duplicated connections

        seat_positions = {k: np.asarray([k,0.5]) for k in range(1,int((num_people)/2)+1)} # Seat the upper row
        seat_positions.update({k: np.asarray([num_people+1-k,0]) for k in range(int(num_people/2)+1,num_people+1)}) # Seat the lower row

    S.add_edges_from(table_adjacency)

    # For every person, list their cliques
    clique_dict = {}
    clique_list = list(nx.find_cliques(G))

    for person in G.nodes():
        for clique in clique_list:
            if str(person) in clique:
                clique_dict[person] = clique

    mapping = {} # Dictionary of seat number to person sitting in it
    # For every seat
    for seat in S.nodes():
        # Give people scores
        scores = {}
        # For every neighbor
        for person in G.nodes():
            for neighbor in nx.neighbors(S,seat):
                # if nx.is_isolate(G,person):
                #     scores[person] = scores.get(person, 0) + 2
                # Give points to people not in cliques with the neighbors
                if mapping.get(neighbor,None) not in nx.neighbors(G,person):
                    scores[person] = scores.get(person, 0) + 1
                scores[person] = scores.get(person, 0)
        # Seat unseated person with best score here
        for person in sorted(scores.items(),key=lambda x: x[1],reverse=chaotic):
            if person[0] not in mapping.values():
                mapping[seat] = person[0]
                break
        # Remove the person from the unseated pool
    T = nx.relabel_nodes(S,mapping)
    pos = {mapping[k]: v for k,v in seat_positions.items()}
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    nx.draw_networkx(T,pos=pos,with_labels=True,ax=axis)
    plt.xlim([-2, num_people/2 + 1])
    #plt.show()
    return fig
    fig = clq.make_seating(G.nodes,G.edges)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
