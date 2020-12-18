import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
from base64 import b64encode

def make_longtable_graph(num_people):
    """
        Makes a long table for num_people. If odd, there is someone sitting on the end
        Returns:
         Graph representing a long table with edges for people who can talk
         Positions for node display
    """
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

    S = nx.Graph()
    S.add_nodes_from(range(1,num_people))
    S.add_edges_from(table_adjacency)
    return S, seat_positions

def make_seating(agreement_graph, chaotic = True):

    num_people = len(agreement_graph.nodes)
    if not chaotic:
        agreement_graph = nx.complement(agreement_graph)
    # Make the agreement graph from people and edges (agreements)
    # Make the table graph with adjacency for neighboring seats
    # Also generate the positions of seats for plotting
    table, seat_positions = make_longtable_graph(num_people)
    # For every person, list their cliques
    clique_dict = {}
    #clique_list = list(nx.find_cliques(agreement_graph))
    # List every clique for every person
    clique_list = (list(nx.enumerate_all_cliques(agreement_graph)))
    for person in agreement_graph.nodes():
        clique_dict[person] = []
        for clique in [c for c in clique_list if str(person) in c and len(c) > 1]:
            clique_dict[person].append(clique)
    # print(clique_dict)
    mapping = {} # Dictionary of seat number to person sitting in it
    # For every seat
    for seat in table.nodes():
        # Give people scores
        scores = {}
        # For every neighbor
        for person in [p for p in agreement_graph.nodes() if p not in mapping.values()]:
            for neighbor in nx.neighbors(table,seat):
                for clique in clique_dict[person]:
                    # "Punish" candidates who are in cliques with neighbors
                    if mapping.get(neighbor,None) in clique:
                        scores[person] = scores.get(person, 0) - 1
                    scores[person] = scores.get(person, 0)
        # Seat unseated person with best score here
        print("{}: {}\n".format(seat,sorted(scores.items(),key=lambda x: x[1],reverse=True)))
        for person in sorted(scores.items(),key=lambda x: x[1],reverse=True):
            if person[0] not in mapping.values():
                mapping[seat] = person[0]
                break

    print(mapping)
    # Apply the calculated seating arrangement
    T = nx.relabel_nodes(table,mapping)
    pos = {mapping[k]: v for k,v in seat_positions.items()}
    # Plot the seating arrangement
    fig = Figure()
    output = io.BytesIO()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_xlim(-0.1, num_people/2 + 1)
    axis.set_ylim(-0.1,0.6)
    nx.draw_networkx(T,pos=pos,with_labels=True,ax=axis)

    # Return an image to the flask application
    FigureCanvas(fig).print_png(output)
    return b64encode(output.getvalue()).decode("utf-8")

if __name__ == "__main__":
    # people = ["Sarah","Michael","Kristtiya","Katie","Turkey","Sam","Elmo","JackBlack","Muffin"]
    # edges = [("Turkey","Sam"),("Sarah","Turkey"),("Sam","Sarah"),("Michael","Kristtiya"),("Elmo","JackBlack")]
    people = ["Rudolph","Santa","Snowman","Mrs. Claus","Penguin"]
    edges = [("Rudolph","Santa"),("Santa","Snowman"),("Rudolph","Snowman"),("Santa","Mrs. Claus"),("Santa","Penguin"),
            ("Snowman","Mrs. Claus"),("Mrs. Claus","Penguin"),("Penguin","Rudolph")]
    G = nx.Graph()
    G.add_nodes_from(people)
    G.add_edges_from(edges)
    make_seating(G)
    plt.show()
