import collections
import itertools
import math
import os.path
import pickle
import sys
import time
import traceback

import numpy as np

import CreatIndex
from myLogger import MyLogger

# 获取当前文件的目录路径
current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

log_dir = os.path.join(current_dir, "log")

os.makedirs(log_dir, exist_ok=True)
# 拼接相对路径和日志文件名
log_file_path = os.path.join(log_dir, "foursimiliar.log")
logger = MyLogger(log_file_path)

def fuc_columnWithdict(indefilepath):
    # computer column witdth {doc : columnwith}
    indexfile = os.path.join(indefilepath,"KIV.pkl")
    columnWithdict = collections.defaultdict(dict)
    with open(indexfile, "rb") as file:
        KIV = pickle.load(file)
    stime = time.time()
    for doc, terms in KIV.items():
        docTermslen = 0
        for term in terms:
            docTermslen += len(str(term))
        columnWithdict[doc] = docTermslen / len(terms)

    columnWithfile = os.path.join(indefilepath, "columnWithdict.pkl")
    with open(columnWithfile, "wb") as file:
        pickle.dump(columnWithdict, file)
    etime = time.time()
    print("columnWith similiar compute success %s" % (etime - stime))

def fuc_columnNamedict(indefilepath):
    stime = time.time()
    # compute columnName columnName[doc1][doc2] = value
    indexfile = os.path.join(indefilepath, "KIA.pkl")
    with open(indexfile, "rb") as file:
        KIA = pickle.load(file)
    columnNamedict = collections.defaultdict(dict)
    for columnname, docset in KIA.items():
        for docs in itertools.combinations(docset, 2):
            doc1, doc2 = docs
            if doc2 not in columnNamedict[doc1]:
                columnNamedict[doc1][doc2] = 1.0
            else:
                columnNamedict[doc1][doc2] += 1.0

    columnNamefile = os.path.join(indefilepath, "columnNamedict.pkl")
    with open(columnNamefile, "wb") as file:
        pickle.dump(columnNamedict, file)

    etime = time.time()
    print("columnName similiar sucess time:%s" % (etime - stime))
    stime = time.time()

def fuc_columnValuedict(indefilepath,totaldocnum):
    stime = time.time()
    indexfile = os.path.join(indefilepath, "inversed_index.pkl")
    with open(indexfile, "rb") as file:
        inversed_index = pickle.load(file)

    indexfile = os.path.join(indefilepath, "KIV.pkl")
    with open(indexfile, "rb") as file:
        KIV = pickle.load(file)

    # compute columsValue  columnValue【doc1】【doc2】 = value
    columnValuedict = collections.defaultdict(dict)
    # idf
    idfsore = collections.defaultdict(float)
    for term, docset in inversed_index.items():
        # comput for idf
        df = len(docset) / totaldocnum
        if df > 0.99:
            print("term:%s df 超过0.99" % term)
        else:
            idf = math.log10(1 / df)
            idfsore[term] = idf

        for docs in itertools.combinations(docset, 2):
            doc1, doc2 = docs
            if doc2 not in columnValuedict[doc1]:
                columnValuedict[doc1][doc2] = 1.0 / min(len(KIV[doc1]),len(KIV[doc2]))
            else:
                columnValuedict[doc1][doc2] += 1.0 / min(len(KIV[doc1]),len(KIV[doc2]))

    columnValuefile = os.path.join(indefilepath,"columnValuedict.pkl")
    idfsorefile = os.path.join(indefilepath, "idfsore.pkl")
    with open(columnValuefile, "wb") as file:
        pickle.dump(columnValuedict, file)
    # store the idf - term
    with open(idfsorefile, "wb") as file:
        pickle.dump(idfsore, file)



def fuc_table_tabledict(indefilepath):
    indexfile = os.path.join(indefilepath, "inversed_index.pkl")
    with open(indexfile, "rb") as file:
        inversed_index = pickle.load(file)

    idfsorefile = os.path.join(indefilepath, "idfsore.pkl")
    with open(idfsorefile, "rb") as file:
        idfsore = pickle.load(file)

    stime = time.time()
    # compute columsValue  table_table【doc1】【doc2】 = value
    table_tabledict = collections.defaultdict(dict)
    for term, docset in inversed_index.items():
        for docs in itertools.combinations(docset, 2):
            doc1, doc2 = docs
            if doc2 not in table_tabledict[doc1]:
                table_tabledict[doc1][doc2] = idfsore[term] ** 2
            else:
                table_tabledict[doc1][doc2] += idfsore[term] ** 2

    table_tablefile = os.path.join(indefilepath, "table_tabledict.pkl")
    with open(table_tablefile, "wb") as file:
        pickle.dump(table_tabledict, file)

    etime = time.time()
    print("table_table similiar sucess time:%s" % (etime - stime))

def gettotalSimiliar(indefilepath):
    indexfile = os.path.join(indefilepath, "inversed_index.pkl")
    with open(indexfile, "rb") as file:
        inversed_index = pickle.load(file)

    indexfile = os.path.join(indefilepath, "columnWithdict.pkl")
    with open(indexfile, "rb") as file:
        columnWithdict = pickle.load(file)

    indexfile = os.path.join(indefilepath, "columnNamedict.pkl")
    with open(indexfile, "rb") as file:
        columnNamedict = pickle.load(file)

    indexfile = os.path.join(indefilepath, "table_tabledict.pkl")
    with open(indexfile, "rb") as file:
        table_tabledict = pickle.load(file)

    indexfile = os.path.join(indefilepath, "columnValuedict.pkl")
    with open(indexfile, "rb") as file:
        columnValuedict = pickle.load(file)

    similiarfile = os.path.join(indefilepath, "similiar.txt")
    with open(similiarfile, "a", encoding="utf-8") as f:
        for term, docset in inversed_index.items():
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

                table_table =16.086539239253728
                columnValue =0.16666666666666669
                columnName =1.0
                columnWith =1.0


                similiar = table_table * 3.1153867 + columnValue * -41.712273 + columnName * -16.411203  + columnWith * 46.372387 -17.42106
                lable = 1 / (1 + np.exp(-similiar))
                if lable == 1.0:
                    tup = (doc1,doc2,lable)
                    f.write(str(tup))


def foursimiliar(indexfilepath,totalnum):
    try:
        fuc_columnValuedict(indexfilepath,totalnum)
        fuc_table_tabledict(indexfilepath)
        fuc_columnNamedict(indexfilepath)
        fuc_columnWithdict(indexfilepath)
    except Exception  as e:
        # 获取异常的详细堆栈信息
        stack_trace = traceback.format_exc()
        # 将堆栈信息写入日志文件
        print(stack_trace)

#foursimiliar("D:\ljj\data\my_index.pkl","D:\ljj\data")

#foursimiliar("/home/lijiajun/data/my_index.pkl","/home/lijiajun/data")
print("comupute four  similiar bigin ")
foursimiliar("D:\ljj\data",14810)
#foursimiliar("/home/lijiajun/data/", index.doc_number)
print("comupute four  similiar end ")


gettotalSimiliar("D:\ljj\data")