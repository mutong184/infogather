import networkx as nx

# 创建二分图
G = nx.Graph()

# 添加左侧节点（代理）
G.add_nodes_from(['Agent1', 'Agent2', 'Agent3'])

# 添加右侧节点（接收者）
G.add_nodes_from(['Receiver1', 'Receiver2', 'Receiver3'])

# 添加边和权重
G.add_edge('Agent1', 'Receiver1', weight=3)
G.add_edge('Agent1', 'Receiver3', weight=2)
G.add_edge('Agent2', 'Receiver2', weight=2)
G.add_edge('Agent2', 'Receiver4', weight=1)
G.add_edge('Agent3', 'Receiver1', weight=1)
G.add_edge('Agent3', 'Receiver3', weight=4)
G.add_edge('Agent3', 'Receiver4', weight=2)

# 使用最大权匹配算法
matching = nx.max_weight_matching(G, weight='weight', maxcardinality=True)

print("最大权匹配结果：")
for agent, receiver in matching:
    weight = G[agent][receiver]['weight']
    print(f"节点 {agent} 和节点 {receiver} 匹配，权重为 {weight}")
