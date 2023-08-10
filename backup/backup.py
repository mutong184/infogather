## 创建倒排索引 ， 不一定
import collections
import itertools
import math
import os
import csv
from collections import Counter

import numpy as np


def inversedindex(path):
    ## 将文档的单列属性 对应一个文档编号  {文档编号： 文档 和单属性的组合} 下面所有的文档doc 变量 都表示文档编号
    docNo = collections.defaultdict(lambda: '')
    ## 文档的倒排索引 {term ： [doc.....]}
    inversed_index = {}
    ## 文档中term 对应的tf-idf 索引 {doc:{term : tf}}
    sore_tf_idf = collections.defaultdict(dict)
    ## 获取所有的列,用于计算idf
    total_colums = 0
    doc_number = 0
    for filename in os.listdir(path):
        if filename.endswith(".csv"):
            # 打开CSV文件
            try:
                with open(os.path.join(path, filename), "r", encoding="utf-8") as csvfile:
                    # 读取CSV文件内容
                    csvreader = csv.reader(csvfile)
                    headers = next(csvreader)
                    columns = {header: [] for header in headers}
                    for row in csvreader:
                        for i, value in enumerate(row):
                            columns[headers[i]].append(value)
                # 将每一列数据 加入到索引当中
                for header, data in columns.items():
                    docName = f"{filename[:-4]}#{header}".replace("\n", "")
                    docNo[doc_number] = docName
                    doc = doc_number
                    doc_number = doc_number + 1
                    counter = Counter(data)
                    data_length = len(data)
                    ## 是文档doc 的词频统计 {term ：tf}
                    frequence_data = {key: value / data_length for key, value in counter.items()}
                    terms = set(data)
                    total_colums = total_colums + 1
                    ## 创建inverted index {term ： [doc....]}
                    for term in terms:
                        if term in inversed_index.keys():
                            inversed_index[term].append(doc)
                        else:
                            inversed_index[term] = [doc]
                        ## 创建 文档中对应的term 的tf -idf 索引， 因为需要计算idf值，所以这里暂时放的是tf 的值，之后再遍历这个索引，乘以idf
                        sore_tf_idf[doc][term] = frequence_data[term]
            except UnicodeDecodeError as e:
                print(f"Failed to read file {filename}: {e}")
    return  inversed_index, sore_tf_idf, total_colums,docNo

def computer_df_idf(df_cut,sore_tf_idf,total_colums,inversed_index):
    ## df_cut 是对于 df 出现过高的term 进行删除，因为不具有辨识度
    N = total_colums
    for term ,docs in inversed_index.items():
        contain_term_docs = len(docs)
        df = contain_term_docs / N
        if df >= float(df_cut):
            continue
        idf = math.log10(1 / df)
        for doc in docs:
            sore_tf_idf[doc][term] = sore_tf_idf[doc][term] * idf
## 定义一个生成器函数处理大列表的组合
def combinations_generator(lst, r):
    for combination in itertools.combinations(lst, r):
        yield combination

## 定义tf -idf 相似度矩阵，这里我们使用余弦相似度
def get_similar_matrix(inversed_index,sore_tf_idf):
    similar_matrix = collections.defaultdict(dict)
    for term, docs in inversed_index.items():
        combinations = combinations_generator(docs,2)
        for combination in combinations:
            doc1 = combination[0]
            doc2 = combination[1]
            doc1_arry = np.array(list(sore_tf_idf[doc1].values()))
            doc2_arry = np.array(list(sore_tf_idf[doc2].values()))
            doc1_length = math.sqrt(np.sum(doc1_arry))
            doc2_length = math.sqrt(np.sum(doc2_arry))
            sore = (sore_tf_idf[doc1][term]*sore_tf_idf[doc2][term]) / (doc1_length * doc2_length)
            if doc2 in similar_matrix[doc1].keys():
                similar_matrix[doc1][doc2] += sore
            else:
                similar_matrix[doc1][doc2] = sore
    return similar_matrix
path = "D:\dataset\csv_benchmark"
inversed_index, sore_tf_idf, total_colums,docNo = inversedindex(path)
##df_cut,sore_tf_idf,total_colums,inversed_index
computer_df_idf(0.999, sore_tf_idf, total_colums,inversed_index)
matix = get_similar_matrix(inversed_index,sore_tf_idf)
file_docNo = os.path.join(path,"docNoIndex.csv")
file_inversed_index = os.path.join(path,"invertedindex.csv")
file_similiar_matrix = os.path.join(path,"similiar_matrix.csv")
with open(file_docNo, "w", newline="") as f:
    writer = csv.writer(f)
    for key, value in docNo.items():
        writer.writerow([key, value])

print(matix)
print(docNo)
print(inversed_index)











