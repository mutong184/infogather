import os
import sys
import time

import CreatIndex
from fourSimiliarCompute.foursimiliarget import gettotalSimiliar
from myLogger import MyLogger

# 获取当前文件的目录路径
current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

log_dir = os.path.join(current_dir, "log")

os.makedirs(log_dir, exist_ok=True)
# 拼接相对路径和日志文件名
log_file_path = os.path.join(log_dir, "main.log")
logger = MyLogger(log_file_path)

if __name__ == '__main__':
    #filepath = "/data_ssd/opendata"
    #filepath = "/data_ssd/webtable/large/split_1"
    #filepath = "/data_ssd/webtable/large/"
    filepath = "D:\dataset\csv_benchmark"
    #indexstorpath = "/home/lijiajun/data/opendata/"
    #indexstorpath = "/home/lijiajun/data/split_1.pkl"
    #indexstorpath = "/home/lijiajun/data/large.pkl"
    indexstorpath = "D:\ljj\data"
    start_time = time.time()
    index = CreatIndex.CreatDataIndex(filepath)
    index.computeIndex()
    #index.storeIndex(indexstorpath)
    print("index length :%s" % index.doc_number)
    end_time = time.time()
    print("Index creation time: %s" % (end_time - start_time))


    print("comupute four  similiar bigin ")
    #foursimiliar("D:\ljj\data",14810)
    #foursimiliar("/home/lijiajun/data/", index.doc_number)
    print("comupute four  similiar end ")
    """
    gettotalSimiliar("D:\ljj\data")




    with open(indexstorpath, "wb") as file:
        pickle.dump(index, file)
  
    with open(indexstorpath, 'rb') as f:
        similiar_matrix = pickle.load(f)
    """


























