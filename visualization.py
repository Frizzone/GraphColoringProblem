__PLOT = True
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import imageio
import os

def plot(solution, edges, node_count, it=None):
    G = nx.Graph()
    color_count = max(solution)
    
    edges_list = []
    nodes_list = []
    color_list = []
    colors = []
    
    for i in range(color_count+1): colors.append(np.random.rand(3,))
    
    for n in range(node_count): 
        nodes_list.append(n)
        G.add_node(n)
        color_list.append(colors[solution[n]])
    
    for edge in edges:
        edges_list.append((edge[0], edge[1]))
        G.add_edge(edge[0], edge[1])
    
    nx.draw(G, nodelist=nodes_list, edgelist=edges_list, with_labels=True,
                        node_color=color_list, width=1, edge_color='b', node_size=60,
                        font_color='w', font_size=6, font_family='sans-serif')
    
    plt.show()