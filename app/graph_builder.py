import networkx as nx
import pandas as pd

def import_csv(filename):
    """ import csv file into a Pandas dataframe """
    return pd.read_csv(filename)

def preprocessing(filename):
    """ make Pandas dataframe easier to work with by:
        - deleting timestamp column
        - making the names column into the row labels
    """
    data = import_csv(filename)
    del data['Timestamp'] #delete timestamp column
    data = data.set_index('Name') # set names column to row labels
    data.index.names = [None]
    return data

def initialize_graph(data):
    """ build a graph with the name/identifiers as nodes """
    num_rows = data.shape[0]
    G = nx.Graph()
    row_names = []
    for (name, b) in data.iterrows():
        row_names.append(name)
        G.add_node(name)
    return G, row_names

def build_graph(data):
    """ iterates through all question answers and adds an edge when people agree
    """
    G, row_names = initialize_graph(data)
    for question, answers in data.iteritems():
        # print(answers)
        for curr_name in row_names:
            for compare_name in row_names:
                if answers[curr_name] == answers[compare_name] and curr_name != compare_name:
                    G.add_edge(curr_name, compare_name)
    return G


if __name__ == "__main__":
    data = preprocessing("Survey.csv")
    G = build_graph(data)
    print(G.edges)
