import pickle
import sys
import pandas as pd
import collections
import os
import util
from myLogger import MyLogger
# 获取当前文件的目录路径
current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

log_dir = os.path.join(current_dir, "log")

os.makedirs(log_dir, exist_ok=True)
# 拼接相对路径和日志文件名
log_file_path = os.path.join(log_dir, "creatindex.log")
logger = MyLogger(log_file_path)

class CreatDataIndex:
    def __init__(self, datafile):
        # index KIA {attribute name: doc list}
        self.KIA = collections.defaultdict(set)
        # index of KIV {doc : terms list}
        self.KIV = collections.defaultdict(set)
        # doc - document_attribute_name {doc:doc_attribute_name}
        self.docNo = collections.defaultdict(str)
        # docname- docColumn list
        self.docColumns = collections.defaultdict(set)
        # {term:[doc.....]}
        self.inversed_index = collections.defaultdict(set)
        # datafile
        self.datafile = datafile
        # counter
        self.doc_number = 0

    def computeIndex(self):
        with os.scandir(self.datafile) as filenames:
            for filename in filenames:
                if filename.is_file() and filename.name.endswith(".csv"):
                    try:
                        df = pd.read_csv(filename.path)
                    except Exception as e:
                        print("%s occur Error :%s"%(filename.name,e))
                        continue
                    headers = df.columns.tolist()
                    columns = {header: set(df[header].unique()) for header in headers}

                    for header, data in columns.items():
                        header = header.strip()
                        if not header:
                            continue
                        docName = f"{filename.name}#{header}".replace("\n", "")
                        self.docNo[self.doc_number] = docName
                        self.docColumns[filename.name].add(self.doc_number)

                        doc = self.doc_number

                        # create KIA index
                        header_tmp = util.convertArrtibute(header)
                        if header_tmp:
                            self.KIA[header_tmp].add(doc)
                        else:
                            print("文件名转化失败，失败的属性名为：%s" % header)

                        # create inverted index
                        terms = data
                        for term in terms:
                            self.inversed_index[term].add(doc)

                        # create KIV index
                        self.KIV[self.doc_number] = terms

                        self.doc_number += 1
                elif filename.is_dir():
                    self.datafile = filename.path
                    self.computeIndex()
    def storeIndex(self,storepath):
        KIAfile = os.path.join(storepath, "KIA.pkl")
        with open(KIAfile, "wb") as file:
            pickle.dump(self.KIA, file)

        KIVfile = os.path.join(storepath, "KIV.pkl")
        with open(KIVfile, "wb") as file:
            pickle.dump(self.KIV, file)

        docNofile = os.path.join(storepath, "docNo.pkl")
        with open(docNofile, "wb") as file:
            pickle.dump(self.docNo, file)

        inversed_indexfile = os.path.join(storepath, "inversed_index.pkl")
        with open(inversed_indexfile, "wb") as file:
            pickle.dump(self.inversed_index, file)

        docColumnsfile = os.path.join(storepath, "docColumns .pkl")
        with open(docColumnsfile, "wb") as file:
            pickle.dump(self.docColumns, file)

        print("all index store success")











