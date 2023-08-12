"""
The code in this file computes the PageRanks using the Monte Carlo algorithm.
"""

import networkx as nx
import random
from numpy import cumsum, array


class IncrementalPersonalizedPageRank2(object):


    def __init__(self, graph, node, number_of_random_walks, reset_probability):

        self.graph = graph
        self.node = node
        self.number_of_random_walks = number_of_random_walks
        self.reset_probability = reset_probability

        self.random_walks = list()
        self.added_edges = list()
        self.removed_edges = list()

    def initial_random_walks(self):
        while len(self.random_walks) < self.number_of_random_walks:
            self.regular_random_walk(self.node)
        return

    def regular_random_walk(self, node):
        random_walk = [node]
        c = random.uniform(0, 1)
        while c > self.reset_probability:
            if len(list(self.graph.neighbors(random_walk[-1]))) > 0:
                current_node = random_walk[-1]
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
                random_walk.append(next_node)
                c = random.uniform(0, 1)
            else:
                break
        self.random_walks.append(random_walk)
        return

    def compute_personalized_page_ranks(self):
        zeros = [0 for _ in range(len(list(self.graph.nodes())))]
        page_ranks = dict(zip(list(self.graph.nodes()), zeros))
        visit_times = dict(zip(list(self.graph.nodes()), zeros))
        nodes_in_random_walks = []
        for random_walk in self.random_walks:
            nodes_in_random_walks.extend(random_walk)
        for node in self.graph.nodes():
            visit_times[node] = nodes_in_random_walks.count(node)
        for node in self.graph.nodes():
            try:
                page_ranks[node] = float(visit_times[node]) / sum(visit_times.values())
            except ZeroDivisionError:
                print("List of visit times is empty...")
        print("pageranke len is %s"%sum(visit_times.values()))
        return page_ranks


