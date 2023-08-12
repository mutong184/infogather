import collections
import csv
import os
import re
import logging

from util import calculate_unionsection


class CreatDataIndex:
    def __init__(self, datefile):
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
        self.path = datefile
        # counter
        self.doc_number = 0


    def computeIndex(self):
        for filename in os.listdir(self.path):
            try:
                with open(os.path.join(self.path, filename), "r", encoding="utf-8") as csvfile:
                    # read csv
                    csvreader = csv.reader(csvfile)
                    headers = next(csvreader)
                    columns = {header: set() for header in headers}
                    for row in csvreader:
                        for i, value in enumerate(row):
                            columns[headers[i]].add(value)

                    for header, data in columns.items():
                        if not header:
                            continue
                        docName = f"{filename}#{header}".replace("\n", "")
                        self.docNo[self.doc_number] = docName

                        # add this column to index
                        self.docColumns[filename].add(self.doc_number)

                        doc = self.doc_number

                        # create KIA index
                        header_tmp = ""
                        header_tmp = self.convertAttribute(header)
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

                        # counter add
                        self.doc_number = self.doc_number + 1
            except UnicodeDecodeError as e:
                print(f"Failed to read file {filename}: {e}")

    def getKIV(self, terms_set):
        list_set = []
        union = {}
        for term in terms_set:
            docs_set = self.inversed_index[term]
            list_set.append(docs_set)
        if list_set:
            union = calculate_unionsection(list_set)
        return union

    # convert attribute
    def convertAttribute(self, name):
        name = name.lower().replace("\n", "")
        # appear \ ()  means multi-attribute name, get the first
        name = re.sub(r'\(.*?\)', "", name)
        name = re.sub(r"\\.*", "", name)
        name = re.sub(r"\s+", "", name)
        return name
