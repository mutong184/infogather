import math
import time
import random
import itertools
def process_date():
    # 原始文件路径
    file_path = "D:\ljj\data\lable.txt"

    # 创建保存分割文件的文件夹
    new_file_path = "D:\ljj\data\data0.txt"
    stime = time.time()

    count = 147487
    # 迭代读取和写入文件
    with open(file_path, 'r', encoding='utf-8') as src_file, open(new_file_path, 'w', encoding='utf-8') as dst_file:
        # 创建一个可以迭代的对象，只返回随机行索引对应的行内容
        selected_lines = itertools.islice(src_file, 0, None, 10)
        for line in selected_lines:
            line2 = line.strip()
            if line2.endswith("0") and count > 0:
                dst_file.write(line)
                count -= 1
    etime = time.time()
    print(etime - stime)
    print(count)

    # 创建保存分割文件的文件夹
    new_file_path = "D:\ljj\data\data1.txt"

    count = 147487
    # 迭代读取和写入文件
    with open(file_path, 'r', encoding='utf-8') as src_file, open(new_file_path, 'w', encoding='utf-8') as dst_file:
        # 创建一个可以迭代的对象，只返回随机行索引对应的行内容
        selected_lines = itertools.islice(src_file, 0, None, 10)
        for line in selected_lines:
            line2 = line.strip()
            if line2.endswith("1") and count > 0:
                dst_file.write(line)
                count -= 1
    etime = time.time()
    print(etime - stime)
    print(count)
    print("提取完成！")

def split_train_test(lable1file,lable0file,trainrate):
    num_lines = sum(1 for _ in open(lable1file))
    trainsize = math.floor(num_lines * trainrate)
    testsize = math.floor(num_lines*(1- trainrate))
    # contruct train date
    with open(lable1file, 'r') as f:
        lable1_lines = f.readlines()
        # 随机选择指定数量的行
    selected_lable1_lines = random.sample(lable1_lines, trainsize)

    with open(lable0file, 'r') as f:
        lable0_lines = f.readlines()
        # 随机选择指定数量的行
    selected_lable0_lines = random.sample(lable0_lines, trainsize)

    traindatafile = "D:\ljj\data\\traindata.txt"
    # 将选中的行写入目标文件
    with open(traindatafile, 'w') as f:
        f.writelines(selected_lable1_lines)
        f.writelines(selected_lable0_lines)

    # contruct test date

    test_lable1_lines = random.sample(lable1_lines, testsize)
    test_lable0_lines = random.sample(lable0_lines, testsize)
    testdatafile = "D:\ljj\data\\testdata.txt"
    # 将选中的行写入目标文件
    with open(testdatafile, 'w') as f:
        f.writelines(test_lable1_lines)
        f.writelines(test_lable0_lines)

process_date()
split_train_test("D:\ljj\data\data1.txt","D:\ljj\data\data0.txt",0.8)





