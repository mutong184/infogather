import pickle
import time

import networkx as nx
import numpy as np

from infogether.page_ranks import IncrementalPersonalizedPageRank3




def pprMtrix2(similiar_matrix,main_node,docnum):
    graph = nx.Graph()
    graph.add_nodes_from([i for i in range(docnum)])
    for tup in similiar_matrix:
        # Get edges
        edg1, edg2, edg3 = tup
        graph.add_edge(edg1, edg2,weight=1)

    start_time = time.time()
    page_ranks_2 = nx.pagerank(graph, alpha=0.7, personalization={main_node: 1},
                               max_iter=1000, weight='weight')
    end_time = time.time()
    print("Power Iteration Pageranks time: ", end_time -start_time)

    start_time = time.time()
    pr = IncrementalPersonalizedPageRank3(graph, main_node, 300, 0.3)
    pr.initial_random_walks()
    page_ranks3 = pr.compute_personalized_page_ranks()
    end_time = time.time()
    print("Mokar tero Pageranks time: ", end_time - start_time)

    re = []
    for i in range(14810):
        if i not in page_ranks3.keys():
            re.append(0.0)
        else:
            re.append(page_ranks3[i])
    page_ranks_array = np.array(re)
    #page_ranks_array = np.array(list(page_ranks_2_2.values()))
    page_ranks_2_array = np.array(list(page_ranks_2.values()))


    # 计算差异并进行归一化
    difference = np.linalg.norm(page_ranks_array - page_ranks_2_array) / np.linalg.norm(page_ranks_2_array)

    # 打印结果
    return difference



if __name__ == '__main__':


    """ 
    filesimiliar = ""
    if not filesimiliar:
        filesimiliar = "D:\ljj\data\similiarmatrix.pickle"

    start_time = time.time()
    with open(filesimiliar, 'rb') as f:
        similiar_matrix = pickle.load(f)
    docnum = 14810
    result = []
    for i in range(1):
        print(pprMtrix2(similiar_matrix,i,docnum))

    """
    # Load graph
    filesimiliar = ""
    if not filesimiliar:
        filesimiliar = "D:\ljj\data\similiarmatrix.pickle"

    start_time = time.time()
    with open(filesimiliar, 'rb') as f:
        similiar_matrix = pickle.load(f)
    docnum = 14810
    
    graph = nx.Graph()
    graph.add_nodes_from([i for i in range(docnum)])
    for tup in similiar_matrix:
        edg1, edg2, edg3 = tup
        graph.add_edge(edg1, edg2, weight=1)
    num_walks = 300
    reset_pro = 0.3
    stime = time.time()
    pr = IncrementalPersonalizedPageRank3(graph, num_walks, reset_pro,docnum)
    pr.initial_random_walks()
    page_ranks3 = pr.compute_personalized_page_ranks()
    etime = time.time()
    print(etime - stime)
    pprmatrixfile = "D:\ljj\data\pprmatrix_n%s_r%s.pickle" % (num_walks, reset_pro)
    with open(pprmatrixfile, 'wb') as file:
        pickle.dump(page_ranks3, file)
    print("ppr matrix 构建完成")






