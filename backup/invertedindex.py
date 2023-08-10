## 创建倒排索引 ， 不一定
import collections
import itertools
import math
import os
import csv
from collections import Counter
import time
from functools import reduce

import pandas as pd
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
"""



def inversedindex(path):
    docNo = {}
    inversed_index = {}
    sore_tf_idf = {}
    total_columns = 0
    doc_number = 0
    for filename in os.listdir(path):
        if filename.endswith(".csv"):
            try:
                df = pd.read_csv(os.path.join(path, filename))
                headers = df.columns

                for header in headers:
                    docName = f"{filename[:-4]}#{header}".replace("\n", "")
                    docNo[doc_number] = docName
                    doc = doc_number
                    doc_number += 1
                    data = df[header].tolist()
                    counter = dict(pd.Series(data).value_counts(normalize=True))
                    terms = set(data)
                    total_columns += 1
                    for term in terms:
                        inversed_index.setdefault(term, []).append(doc)
                        sore_tf_idf.setdefault(doc, {})[term] = counter.get(term, 0)

            except UnicodeDecodeError as e:
                print(f"Failed to read file {filename}: {e}")

    return inversed_index, sore_tf_idf, total_columns, docNo
"""

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
    doc_lengths = {}  # 缓存文档的长度
    for term, docs in inversed_index.items():
        for combination in itertools.combinations(docs, 2):
            doc1,doc2 = combination
            # 计算文档长度
            if doc1 not in doc_lengths:
                doc1_arry = np.array(list(sore_tf_idf[doc1].values()))
                doc_lengths[doc1] = math.sqrt(np.sum(doc1_arry))
            if doc2 not in doc_lengths:
                doc2_arry = np.array(list(sore_tf_idf[doc2].values()))
                doc_lengths[doc2] = math.sqrt(np.sum(doc2_arry))

            doc1_length = doc_lengths[doc1]
            doc2_length = doc_lengths[doc2]

            # 计算相似度
            term_score = sore_tf_idf[doc1][term] * sore_tf_idf[doc2][term]
            sore = term_score / (doc1_length * doc2_length)

            # 更新相似度矩阵
            if doc2 in similar_matrix[doc1]:
                similar_matrix[doc1][doc2] += sore
            else:
                similar_matrix[doc1][doc2] = sore

        return similar_matrix

def computer_pair_docs_label4(doc1 ,doc2):
    ## dict.keys() 得到的类型为dict_keys类型不能直接转换成list，或者是np.array
    term_doc1 = np_term_bydoc[doc1]
    term_doc2 = np_term_bydoc[doc2]
    ## np.nunon1d 方法是基于c语言的，执行效率更高
    doc1_doc2_term_union = np.union1d(term_doc1,term_doc2)
    min_docset = np.array([])
    min_docset_len = 5000
    for index in doc1_doc2_term_union:
        set_len = np_docs_byterm[index].shape[0]
        if set_len < min_docset_len:
            min_docset = np_docs_byterm[index]
            min_docset_len = set_len

    min_docset = min_docset[(min_docset != doc1) & (min_docset != doc2)]
    for docnum in min_docset:

        if all(term in np_term_bydoc[docnum] for term in doc1_doc2_term_union):
            return True
        """
        if (doc1_doc2_union <= dict_set[docnum]):
            return True
        """
    return False


def computer_pair_docs_label(doc1 ,doc2):
## 首先获取两个文档中 distinct term 的交集
    ## dict.keys() 得到的类型为dict_keys类型不能直接转换成list，或者是np.array
    term_doc1 = set(sore_tf_idf[doc1].keys())
    term_doc2 = set(sore_tf_idf[doc2].keys())
    ## np.nunon1d 方法是基于c语言的，执行效率更高
    doc1_doc2_union = term_doc1.union(term_doc2)
    #iterr_set = map(lambda x:inversed_index[x],doc1_doc2_union)
    reslut_set = reduce(lambda x,y:set(x) & set(y),(inversed_index[i] for i in doc1_doc2_union))
    ## 这里需要将 文档doc1 和文档doc2 排除
    length = len(reslut_set)
    if doc1 in reslut_set:
        length = length -1
    if doc2 in reslut_set:
        length = length -1
    return length > 0

def computer_pair_docs_label2(doc1 ,doc2):
## 首先获取两个文档中 distinct term 的交集
    ## dict.keys() 得到的类型为dict_keys类型不能直接转换成list，或者是np.array
    term_doc1 = set(sore_tf_idf[doc1].keys())
    term_doc2 = set(sore_tf_idf[doc2].keys())
    ## np.nunon1d 方法是基于c语言的，执行效率更高
    doc1_doc2_union2 = term_doc1.union(term_doc2)
    result_set2 = reduce(lambda x, y: set(x) & set(y), (inversed_index[ele] for ele in doc1_doc2_union2))
    ## 这里需要将 文档doc1 和文档doc2 排除
    length = len(result_set2)
    if doc1 in result_set2:
        length = length -1
    if doc2 in result_set2:
        length = length -1
    return length > 0

path1 = "D:\dataset\csv_benchmark"
path = "D:\data_ljj"
startime = time.time()
inversed_index, sore_tf_idf, total_colums,docNo = inversedindex(path)
##df_cut,sore_tf_idf,total_colums,inversed_index
computer_df_idf(0.999, sore_tf_idf, total_colums,inversed_index)
endtime = time.time()
time_consum = endtime - startime
print("计算索引的时间为：%s"%time_consum)
print(total_colums)


#matix = get_similar_matrix(inversed_index,sore_tf_idf)
matrix = collections.defaultdict(int)
matix_len = np.array([i for i in range(total_colums)])
startime = time.time()
##  创建对应的np 类型的数据
np_term_bydoc =  collections.defaultdict(lambda: np.array([]))
for key in sore_tf_idf:
    np_term_bydoc[key] = np.array(list(sore_tf_idf[key].keys()))
np_docs_byterm = collections.defaultdict(lambda : np.array([]))
for key in inversed_index:
    np_docs_byterm[key] = np.array(inversed_index[key])
startime = time.time()
for combation in itertools.combinations(matix_len,2):
    doc1,doc2 = combation
    value = computer_pair_docs_label4(doc1,doc2)
    matrix[combation] = value
endtime = time.time()
time_consum = endtime - startime
print("计算full labled的时间为：%s"%time_consum)











