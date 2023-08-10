import numpy as np
import networkx as nx


class PersonalizedPageRank:
    def __init__(self, graph, seed_node, jump_prob=0.15, num_walks=10000, max_steps=100):
        self.graph = graph
        self.seed_node = seed_node
        self.jump_prob = jump_prob
        self.num_walks = num_walks
        self.max_steps = max_steps

    def random_walk(self):
        current_node = self.seed_node
        for _ in range(self.max_steps):
            if np.random.uniform() < self.jump_prob:
                return self.seed_node
            neighbors = list(self.graph.neighbors(current_node))
            if neighbors:
                current_node = np.random.choice(neighbors)
            else:
                return self.seed_node
        return current_node

    def compute_page_rank(self):
        num_nodes = self.graph()
        visit_times = np.zeros(num_nodes)

        for _ in range(self.num_walks):
            node = self.random_walk()
            visit_times[node] += 1

        page_rank = visit_times / np.sum(visit_times)
        return page_rank


# 创建一个有向图
graph = nx.DiGraph()

# 添加边
graph.add_edge(0, 1)
graph.add_edge(0, 2)
graph.add_edge(1, 2)
graph.add_edge(1, 3)
graph.add_edge(2, 0)
graph.add_edge(2, 1)
graph.add_edge(2, 3)

seed_node = 0
ppr = PersonalizedPageRank(graph, seed_node)

page_rank = ppr.compute_page_rank()
print(page_rank)
