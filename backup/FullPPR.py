import collections
import pickle
import time
from functools import partial

import numpy as np
import networkx as nx

class FullPersonalizedPagerank:
    def __init__(self, graph, walk_length, num_walks):
        self.graph = graph
        self.walk_length = walk_length
        self.num_walks = num_walks
        self.ppr_vectors = collections.defaultdict(partial(collections.defaultdict, float))
        self.total = walk_length * num_walks

    def personalized_pagerank(self):
        for _ in range(self.num_walks):
            for node in self.graph.nodes():
                self.random_walk(node)

        for node in self.graph.nodes():
            sumup = sum(self.ppr_vectors[node].values())
            for visited_node in self.ppr_vectors[node].keys():
                self.ppr_vectors[node][visited_node] /= sumup

        return self.ppr_vectors

    def random_walk(self, node):
        path = [node]
        neighbors = list(self.graph.neighbors(node))

        for i in range(self.walk_length - 1):
            if len(neighbors) == 0:
                break
            next_node = np.random.choice(neighbors)
            self.ppr_vectors[node][next_node] += 1
            path.append(next_node)
            neighbors = list(self.graph.neighbors(next_node))