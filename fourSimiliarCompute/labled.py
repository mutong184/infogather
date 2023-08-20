import collections
import itertools
import pickle
import time

from myLogger import MyLogger


logger = MyLogger('D:\ljj\log\getallable.log')
if __name__ == '__main__':

    docnum = 14810
    doclist = [i for i in range(docnum)]
    with open("D:\ljj\data\similiarmatrix.pickle", 'rb') as f:
        similiar_matrix = pickle.load(f)

    # get labed 1
    labeldic = collections.defaultdict(int)
    for tup in similiar_matrix:
        # Get edges
        edg1, edg2, edg3 = tup
        labeldic[(edg1,edg2)] = 1

    # compute table_tabledict  table_table【doc1】【doc2】 = value
    with open("D:\ljj\data\\table_tabledict.pkl", "rb") as file:
        table_tabledict = pickle.load(file)

    # compute columsValue  columnValue【doc1】【doc2】 = value
    with open("D:\ljj\data\columnValuedict.pkl", "rb") as file:
        columnValuedict = pickle.load(file)

    # compute columnName columnName[doc1][doc2] = value

    with open("D:\ljj\data\columnNamedict.pkl", "rb") as file:
        columnNamedict = pickle.load(file)

    # computer column witdth {doc : columnwith}

    with open("D:\ljj\data\columnWithdict.pkl", "rb") as file:
        columnWithdict = pickle.load(file)

    stime = time.time()
    with open("D:\ljj\data\lable.txt","w",encoding='utf-8') as f:
        #f.write("table-table columnValue columnName columnWith lable \n")

        for doc1,doc2 in itertools.combinations(doclist, 2):
            table_table = 0.0
            columnValue = 0.0
            columnName = 0.0
            columnWith = 0.0
            lable = 0
            if (doc1,doc2) in labeldic:
                lable = 1
            if doc1 in table_tabledict and doc2 in table_tabledict[doc1]:
                table_table = table_tabledict[doc1][doc2]
            if doc1 in columnValuedict and doc2 in columnValuedict[doc1]:
                columnValue = columnValuedict[doc1][doc2]
            if doc1 in columnNamedict and doc2 in columnNamedict[doc1]:
                columnName = columnNamedict[doc1][doc2]
            columnWith = columnWithdict[doc1] / columnWithdict[doc2]
            f.write("%s#%s#%s#%s#%s\n"%(table_table,columnValue,columnName,columnWith,lable))
    etime = time.time()
    comsumer = stime - etime
    print("labed comsumer time %s"%(comsumer))
    print("lable weigth compute success")


























