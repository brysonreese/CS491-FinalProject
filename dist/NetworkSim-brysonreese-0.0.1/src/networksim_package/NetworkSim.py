'''
Project:    Random Doubly Weighted Graph Network Simulator
Authors:    Bryson Reese, Fate Jacobson, Austen Chu
Date:       December 6, 2021
Purpose:    Generate a random doubly weighted graph to simulate a network with nodal processing delay
            as well as transmission delay. User may specify the amount of iterations made, so that they
            can collect this data and use for research purposes. This project was initially thought of
            for machine learning purposes, to one day use the position data, weight data, and path data,
            as well as possibly OCR to train a model to efficiently find the shortest weighted path
            through this network, to act as a simulation to emphasize network thoroughput.
'''

'''
Updated on Apr 19, 2022 to create more modularity for purposes of unit testing for CS491 final project
'''

import networkx as nx
import matplotlib.pyplot as plt
import random
import math
import os
import sys

##generates graph pngs
def generateGraph(graph, path, iteration):
    ##generate good looking node layout for graph generation
    pos_nodes = nx.spring_layout(graph)
    nx.draw(graph, pos_nodes, with_labels=True)

    ##position the attributes of the nodes properly 
    pos_attrs = {}
    for node, coords in pos_nodes.items():
         pos_attrs[node] = (coords[0], coords[1] + 0.06)

    ##get node attributes and add them to custom node attributes
    node_attrs = nx.get_node_attributes(graph, 'weight')
    custom_node_attrs = {}
    for node, attr in node_attrs.items():
        custom_node_attrs[node] = str(attr)

    ##draw node attributes
    nx.draw_networkx_labels(graph, pos_attrs, labels=custom_node_attrs)

    ##retrieve and draw edge labels
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos_nodes, edge_labels)
    
    ##save png to iteration folder
    plt.savefig("{}/{}.png".format(path, iteration), format="PNG")

def create_sim_directory():
    ##making simulation directory
    try:
        os.mkdir("NetworkSim")
    except (FileExistsError) as e:
        print(e)
        print("Ensure there are no remnants of previous runs in the current directory!")
        sys.exit()

def create_iteration(iteration):
    ##create iteration folder and iteration .txt file
    try:
        os.mkdir("NetworkSim/{}".format(iteration))
        f = open("NetworkSim/{}/{}.txt".format(iteration, iteration), "a")
        f.write("(start_vertex, end_vertex) : [path taken] : minWeightCalculated\n")
        return f
    except (FileExistsError) as e:
        print(e)
        print("Ensure there are no remnants of previous runs in the current directory!")
        sys.exit()

def generate_network(numNodes, edgeProb, minNodeWeight, maxNodeWeight, minEdgeWeight, maxEdgeWeight):
        ##generate graph with specified params, remove any isolated ones
        ##isolation in pairs rarely happens above 0.2 edgeprob
        network = nx.fast_gnp_random_graph(numNodes, edgeProb)
        network.remove_nodes_from(list(nx.isolates(network)))

        ##assign random edge and node weights to all nodes and edges generated by network
        for node in nx.nodes(network):
            network.nodes[node]["weight"] = random.randint(minNodeWeight, maxNodeWeight)
            
        for edge in nx.edges(network):
            network.edges[edge]["weight"] = random.randint(minEdgeWeight, maxEdgeWeight)
        return network

def generate_paths(network):
    ##generate all paths possible from every node to every other node (brute force!)
    paths = []

    for node_source in nx.nodes(network):
        for node_end in nx.nodes(network):
            paths.append(list(nx.all_simple_paths(network, node_source, node_end)))

    return paths


def run_sim(numSims, numNodes, edgeProb, minNodeWeight, maxNodeWeight, minEdgeWeight, maxEdgeWeight):
    ##run sim for number of iterations specified
    for iteration in range(numSims):
        f = create_iteration(iteration)

        network = generate_network(numNodes, edgeProb, minNodeWeight, maxNodeWeight, minEdgeWeight, maxEdgeWeight)

        paths = generate_paths(network)

        ##where the MAGIC happens
        ##iterate through generated paths
        ##paths are generated as a list of lists for each set of start to end nodes
        for i in range(len(paths)):
            ##make sure it wasnt going from itself to itself
            if(len(paths[i]) > 0):
                ##examining each path now for given start and end node
                for path in paths[i]:
                    ##set start and end node values
                    currStartNode = path[0]
                    currEndNode = path[-1]
                    ##status vars that contain the info for the next two for loops
                    vertexWeightTotal = 0
                    edgeWeightTotal = 0
                    currMinWeight = math.inf
                    currMinNodePath = []
                    ##adding up all node weights and edge weights for current path
                    for node in path:
                        vertexWeightTotal += network.nodes[node]["weight"]
                    for edge in list(nx.utils.pairwise(path)):
                        edgeWeightTotal += network.edges[edge]["weight"]
                    ##add together, if less than the current min, set it as current min
                    totalWeight = vertexWeightTotal + edgeWeightTotal
                    if totalWeight < currMinWeight:
                        currMinWeight = totalWeight
                        currMinNodePath = path
                ##write to file in iteration folder
                f.write("(" + str(currStartNode) + " , " + str(currEndNode) + ") : " + str(currMinNodePath) + " : " + str(currMinWeight) + "\n")

        f.close()

        ##drop graph in iteration folder
        generateGraph(network, "NetworkSim/{}".format(iteration), iteration)

if __name__ == "__main__":
    create_sim_directory()

    ##get user input
    print("\nWelcome to the network simulator, please enter your desired simulation conditions below.")
    print("Please understand the parameters that you enter, and scale accordingly to your machine's power.")
    print("As this program currently brute forces this, the number of nodes and edge creation probability affect performance the most.")
    print("Provided next to the input spaces are recommended parameters for performance.")
    print("Press CTRL + C to kill in terminal if you get scared, buckle up!\n")
    numSims = int(input("Please enter the number of simulations you would like to run [1 - ?]: "))
    numNodes = int(input("Please enter the estimated number of nodes you would like to generate [2 - 18]: "))
    edgeProb = float(input("Please enter the edge creation probability [0.2 - 0.3]: "))
    minNodeWeight = int(input("Please enter the minimum weights for nodes [1 - ?]: "))
    maxNodeWeight = int(input("Please enter the maximum weights for nodes [1 - ?]: "))
    minEdgeWeight = int(input("Please enter the minimum edge weights [1 - ?]: "))
    maxEdgeWeight = int(input("Please enter the maximum edge weights [1 - ?]: "))

    run_sim(numSims, numNodes, edgeProb, minNodeWeight, maxNodeWeight, minEdgeWeight, maxEdgeWeight)
    