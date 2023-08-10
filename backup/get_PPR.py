import numpy as np
import networkx as nx

def random_walk(graph, node, walk_length):
    path = [node]
    for _ in range(walk_length - 1):
        neighbors = list(graph.neighbors(path[-1]))
        if len(neighbors) == 0:
            break
        weights = [graph[path[-1]][n]['weight'] for n in neighbors]
        probabilities = np.array(weights) / sum(weights)
        next_node = np.random.choice(neighbors, p=probabilities)
        path.append(next_node)
    return path

def personalized_pagerank(graph, start_node, walk_length, num_walks):
    num_nodes = graph.number_of_nodes()
    ppr_vectors = np.zeros((num_nodes, num_nodes))

    for _ in range(num_walks):
        for node in graph.nodes():
            path = random_walk(graph, node, walk_length)
            for i, visited_node in enumerate(path):
                ppr_vectors[node, visited_node] += graph[visited_node][path[i-1]]['weight']

    ppr_vectors = ppr_vectors / (walk_length * num_walks)

    return ppr_vectors[start_node]

# 构建图
graph = nx.Graph()
# 添加边和节点
# ...

start_node = 0
walk_length = 10
num_walks = 100
ppr_vector = personalized_pagerank(graph, start_node, walk_length, num_walks)
