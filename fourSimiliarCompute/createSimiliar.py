import collections
import itertools
import os
import pickle
import sys
import time

import numpy as np

from myLogger import MyLogger

# 获取当前文件的目录路径
current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

log_dir = os.path.join(current_dir, "../log")

os.makedirs(log_dir, exist_ok=True)
# 拼接相对路径和日志文件名
log_file_path = os.path.join(log_dir, "creatsimiliar.log")
logger = MyLogger(log_file_path)



def creatSimiliar(index):
    # compute table_tabledict  table_table【doc1】【doc2】 = value
    with open("D:\ljj\data\\table_table.pkl", "rb") as file:
        table_tabledict = pickle.load(file)

    # compute columsValue  columnValue【doc1】【doc2】 = value
    with open("D:\ljj\data\columnValue.pkl", "rb") as file:
        columnValuedict = pickle.load(file)

    # compute columnName columnName[doc1][doc2] = value

    with open("D:\ljj\data\columnName.pkl", "rb") as file:
        columnNamedict = pickle.load(file)

    # computer column witdth {doc : columnwith}

    with open("D:\ljj\data\columnWith.pkl", "rb") as file:
        columnWithdict = pickle.load(file)



    similiarlist = []
    for term, docset in index.inversed_index.items():
        for docs in itertools.combinations(docset, 2):
            doc1, doc2 = docs
            # 四种相识度
            columnWith = columnWithdict[doc1] / columnWithdict[doc2]
            if doc2 not in columnNamedict[doc1]:
                columnName = 0
            else:
                columnName = columnNamedict[doc1][doc2]
            if doc2 not in table_tabledict[doc1]:
                table_table = 0
            else:
                table_table = table_tabledict[doc1][doc2]
            if doc2 not in columnValuedict[doc1]:
                columnValue = 0
            else:
                columnValue = columnValuedict[doc1][doc2]

            # compute total similiar
            similiar = table_table * 1.6855031 + columnValue * 2.923197 + columnName * 7.5190783 + columnWith * 2.802716 + 8.004719
            lable = np.round(1 / (1 + np.exp(-similiar)))
            similiarlist.append((doc1,doc2,lable))




"""

print("similiar_matrix len %s"%(len(similiar_matrix)))
    acurry = 0
    wrong = 0
    for tup in similiarlist:
        if tup in similiar_matrix:
            acurry += 1
        else:
            wrong += 1
    print("accury : %s wrong:%s"%(acurry / (acurry + wrong),wrong / (acurry + wrong)))
with open("D:\ljj\data\similiarmatrix.pickle", 'rb') as f:
        similiar_matrix = pickle.load(f)
with open("D:\ljj\data\my_index.pkl", "rb") as file:
    index = pickle.load(file)
creatSimiliar(index)
"""





























