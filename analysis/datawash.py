import csv
import sys
import os.path
import json

# 清洗数据，去除重复记录。
def washdata():
    """清洗数据，去除重复记录。
    """
    CUR_PATH = sys.path[0]
    if CUR_PATH == '':
        CUR_PATH = os.getcwd()
    DATAPATH = os.path.join(os.path.dirname(CUR_PATH), 'datafile')  # 此脚本文件上一级路径中的datafile文件夹
    DATA_TABLEHEADER = ['user_url_token', 'user_data_json', 'user_following_list']
    
    # 数据文件夹不存在，就退出
    if not os.path.exists(DATAPATH):
        return None
    
    # 从存储数据文件的文件夹中找出所有csv文件，得到一个包含所有csv绝对路径文件名的list。
    csvfilelist = list()
    for filename in os.listdir(DATAPATH):
        filename = os.path.join(DATAPATH, filename)
        if os.path.splitext(filename)[1] == '.csv':
            with open(filename, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                if reader.fieldnames == DATA_TABLEHEADER:
                    csvfilelist.append(os.path.join(DATAPATH, filename))
    csvfilelist.sort()
    
    WASHED_FILE = os.path.join(CUR_PATH, 'data','washeddata.csv')
    WASHED_TABLEHEADER = ['user_url_token', 'user_data_json']
    # 整理后的文件存在，就退出
    if os.path.exists(WASHED_FILE):
        return None
    
    # 用dict去重
    datadict = dict()
    for filename in csvfilelist:
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                datadict[row[WASHED_TABLEHEADER[0]]] = row[WASHED_TABLEHEADER[1]]
    datalist = list()
    for k,v in datadict.items():
        datalist.append({'user_url_token':k, 'user_data_json':v})
    
    # 写入文件
    with open(WASHED_FILE, 'w', newline='', encoding='utf-8') as csvfile:
        # Create table header.
        headerrow = dict()
        for x in ['user_url_token', 'user_data_json']:
            headerrow[x] = x
        # Write in.
        writer = csv.DictWriter(csvfile, ['user_url_token', 'user_data_json'])
        writer.writerow(headerrow)
        for userinfo in datalist:    
            writer.writerow(userinfo)
    return None
    
washdata()

# 生成器，用于遍历所有用户的数据
def datajsons():
    """生成器，用于遍历所有用户的json数据
    """
    CUR_PATH = sys.path[0]
    if CUR_PATH == '':
        CUR_PATH = os.getcwd()
    FILEPATH = os.path.join(CUR_PATH, 'data','washeddata.csv')
    TABLEHEADER = ['user_url_token', 'user_data_json']
    
    # 数据文件夹不存在，就退出
    if not os.path.exists(FILEPATH):
        return None

    with open(FILEPATH, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            user_data_json = json.loads(row[TABLEHEADER[1]])
            yield user_data_json
    return None