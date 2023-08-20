import os
import pickle
import sys
import time
import CreatIndex
from myLogger import MyLogger

# 获取当前文件的目录路径
current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
# 拼接相对路径和日志文件名
log_file_path = os.path.join(current_dir, "main.log")
logger = MyLogger(log_file_path)



if __name__ == '__main__':
    filepath = "/data_ssd/opendata"
    #filepath = "D:\dataset\csv_benchmark"
    start_time = time.time()
    index = CreatIndex.CreatDataIndex(filepath)
    index.computeIndex()
    print("index length :%s" % index.doc_number)
    end_time = time.time()
    print("Index creation time: %s" % (end_time - start_time))
    with open("/home/lijiajun/data/my_index.pkl", "wb") as file:
        pickle.dump(index, file)
    """ 
    with open("D:\ljj\data\my_index.pkl", 'rb') as f:
        similiar_matrix = pickle.load(f)
    """



def query_table_colums(querytable, querycolumn, index, ppr_vector, k):
    filepath = "D:\dataset\csv_benchmark"
    queryfile = os.path.join(filepath, querytable)
    q = QuaryOnline(queryfile, querycolumn, index, ppr_vector)
    q.getRelationtablesSore()
    result = q.getTransformatTableInfo(index.docNo)
    return result[querycolumn][:k]


def pprMtrix(graph, num_walks, reset_pro, docnum):
    pprmatrixfile = "D:\ljj\data\pprmatrix_n%s_r%s.pickle" % (num_walks, reset_pro)
    if os.path.exists(pprmatrixfile):
        with open(pprmatrixfile, 'rb') as file:
            ppr_vector = pickle.load(file)
        print("no need to compute ppr")
        return ppr_vector
    start_time = time.time()
    pr = IncrementalPersonalizedPageRank3(graph, num_walks, reset_pro, docnum)
    pr.initial_random_walks()
    page_ranks3 = pr.compute_personalized_page_ranks()
    end_time = time.time()
    consumption_time = end_time - start_time
    print("Graph PPR calculation completed, computation time: %s" % consumption_time)
    pprmatrixfile = "D:\ljj\data\pprmatrix_n%s_r%s.pickle" % (num_walks, reset_pro)
    with open(pprmatrixfile, 'wb') as file:
        pickle.dump(page_ranks3, file)
    print("ppr matrix 构建完成")
    with open(pprmatrixfile, 'rb') as file:
        ppr_vector = pickle.load(file)
    return ppr_vector


def indicator(ki, index, ppr_vector):
    groundtrue = "D:\dataset\indicate\csv_groundtruth\\att_groundtruth.csv"
    groundtruedict = util.process_csv(groundtrue)
    precison = [0.0] * ki
    recall = [0.0] * ki
    k = ki
    i = 0
    timec = 0
    for key, value in groundtruedict.items():
        if key == 'query_table#query_col_name':
            continue
        querytablename = key.split("#")[0]
        column = key.split("#")[1]
        try:
            start_time = time.time()
            setresult = query_table_colums(querytablename, column, index, ppr_vector, k)
            end_time = time.time()
            cusumertime = end_time - start_time
            timec += cusumertime
        except Exception as e:
            print("table %s colums %s exception %s" % (querytablename, column, e))
            continue
        i += 1
        tmp_pre = []
        tmp_recall = []
        for cycle in range(1, k + 1):
            intersection = set(setresult[:cycle]) & value
            if intersection:
                l = len(intersection)
                tmp_pre.append(l / cycle)
                tmp_recall.append(l / len(value))
            # print("tablename:%s,precicion:%s ,recall:%s" % (key, l / k, l / len(value)))
            else:
                tmp_pre.append(0.0)
                tmp_recall.append(0.0)
                print(" zero tablename:%s" % (key))
        precison = [a + b for a, b in zip(tmp_pre, precison)]
        recall = [a + b for a, b in zip(tmp_recall, recall)]
    print("i:%s" % i)
    print("30k precicion:%s ,recall:%s,querytime:%s" % (
    sum(precison[:30]) / 30 / i, sum(recall[:30]) / 30 / i, timec / i))
    print("60k precicion:%s ,recall:%s,querytime:%s" % (
    sum(precison[:60]) / 60 / i, sum(recall[:60]) / 60 / i, timec / i))
    print("%s precicion:%s ,recall:%s,querytime:%s" % (k, sum(precison) / k / i, sum(recall) / k / i, timec / i))


def index_judger(file,index1,index2):
    result1 = set()
    result2 = set()
    colums = index1.docColumns[file]
    for colum in colums:
        result1.add(index1.docNo[colum])
    colums2 = index2.docColumns[file]
    for colum in colums2:
        result2.add(index2.docNo[colum])
    if result1 != result2:
        print("%s index error index 1 result:%s index2 result:%s " %(file,result1,result2))
        return 1
    else:
        return 0

























