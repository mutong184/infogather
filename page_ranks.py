"""
The code in this file computes the PageRanks using the Monte Carlo algorithm.
"""
import collections
from functools import partial
from itertools import islice

import networkx as nx
import random
from numpy import cumsum, array


class IncrementalPersonalizedPageRank3(object):


    def __init__(self, graph,number_of_random_walks, reset_probability,docnum):
        self.graph = graph
        self.number_of_random_walks = number_of_random_walks
        self.reset_probability = reset_probability
        self.docnum = docnum

        self.ppr_vectors = collections.defaultdict(partial(collections.defaultdict, float))

    def initial_random_walks(self):
        #for node in islice(self.graph.nodes(), 5):
        for node in range(self.docnum):
            print("construct %s pprvector" %node)
            for _ in range(self.number_of_random_walks):
                self.regular_random_walk(node)
        return

    def regular_random_walk(self, node):
        random_walk = node
        self.ppr_vectors[node][node] += 1
        c = random.uniform(0, 1)
        while c > self.reset_probability:
            if len(list(self.graph.neighbors(random_walk))) > 0:
                current_node = random_walk
                current_neighbors = list(self.graph.neighbors(current_node))
                current_edge_weights = array(
                    [self.graph[current_node][neighbor]['weight'] for neighbor in current_neighbors])
                cumulated_edge_weights = cumsum(current_edge_weights)
                if cumulated_edge_weights[-1] == 0:
                    break
                random_id = list(
                    cumulated_edge_weights < (random.uniform(0, 1) * cumulated_edge_weights[-1])).index(
                    False)
                next_node = current_neighbors[random_id]
                random_walk = next_node
                self.ppr_vectors[node][next_node] += 1
                c = random.uniform(0, 1)
            else:
                break
        return

    def compute_personalized_page_ranks(self):
        #for node in islice(self.graph.nodes(), 5):
        for node in range(self.docnum):
            sumup = sum(self.ppr_vectors[node].values())
            for visited_node in self.ppr_vectors[node].keys():
                try:
                    self.ppr_vectors[node][visited_node] /= sumup
                except ZeroDivisionError:
                    print("List of visit times is empty...")
        return self.ppr_vectors


