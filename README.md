# infogather
Paper：InfoGather- Entity Augmentation and Attribute Discovery By Holistic Matching with Web Tables   code for join and union

online:
python join_creatofflineIndex_webtable_opendata.py 


#offline:
location：13022 /home/lijiajun/infogather/
script: join_creatofflineIndex_webtable_opendata.py 
run commond: python join_creatofflineIndex_webtable_opendata.py
parameters：
datalist: list, dataset list 
indexstorepath: string, the path of storing index
columnValue_rate: float, the columnValue importance of the column
columnName_rate :  float, the columnName importance of the column
columnWith_rate : float, the columnWith importance of the column
dataset_large_or_small: sting , large or small
num_walks: int, the superparameter of ppr
reset_pro: float,the superparameter of ppr


#online:
location：13022  /home/lijiajun/infogather
script: join_queryonline_opendata.py/join_queryonline_webtable.py
run commond: python join_creatofflineIndex_webtable_opendata.py
parameters：
queryfilepath:string the querytablefilepath
columnname: the query column

#get topk:
topk: join_creat_topkfile.py/join_creat_topkfile.py
location：13022  /home/lijiajun/infogather
script: python join_creat_topkfile.py
run commond: python join_creatofflineIndex_webtable_opendata.py
parameters：
filepath: string,the index of final_res_dic.pkl filepath
storepath: string, the result of topk file store path


