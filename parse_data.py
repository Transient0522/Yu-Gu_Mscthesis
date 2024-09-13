import csv

# 处理SEIR模型相关数据，从三个CSV文件中读取数据，并将数据存储在一个字典结构中

# 从名为IMD2019_MSOA.csv的文件中读取数据，提取MSOA代码和IMD数据，并将其存储在字典seir_data中
def parse_imd(seir_data, file_name):
    # seir_data是一个字典，用于存储解析后的数据，它的键是MSOA的代码，值是一个包含IMD、population和COVID-19等信息的字典
    # file_name是要读取的CSV文件的文件名
    with open(file_name, 'r') as f: # 使用open函数以只读模式('r')打开CSV文件
        csv_reader = csv.reader(f) # 创建一个CSV读取器对象csv_reader，它将逐行读取CSV文件中的数据
        # csv.reader()用于读取CSV文件，将文件内容解析为一个可迭代对象，每次迭代返回文件中的一行数据，格式为一个包含各列数据的列表
        csv_it = iter(csv_reader) # 将CSV读取器转换为一个迭代器csv_it，用于逐行遍历文件
        # iter()是python内置函数，用于返回一个迭代器对象。迭代器是一个对象，它可以逐一返回其中的元素
        next(csv_it) # 跳过表头行，因为表头行不包含所需的数值数据
        msoa_cnt = 0 # 初始化计数器msoa_cnt为0，用于统计成功加载的MSOA数据条数
        for line in csv_it: # 使用for循环遍历CSV文件的每一行，line是一个列表，其中每个元素代表CSV文件中该行的一个字段
            # line[0]: msoa code
            # line[7]: imd score
            seir_data[line[0]] = { # line[0]是MSOA的代码，将其作为键存储在字典seir_data中
                'imd': float(line[7]), # line[7]是IMD值
                'population': None, # 初始化population字段为None，表示人口数据暂时未知
                'covid': [], # 初始化covid字段为空列表[]，为未来存储COVID-19数据做准备
                'covid_case':[],  # 现有病例
                'covid_covered': [],  # 治愈病例
            }
            msoa_cnt += 1 # 每次成功添加一个MSOA记录后，msoa_cnt自增1，用于统计已处理的MSOA数据条数
        print("load imd data: {}".format(msoa_cnt)) # 打印输出一条信息，显示成功加载的MSOA数据条数

# 从名为N.csv的文件中读取MSOA的人口数据，通过匹配MSOA代码，在字典seir_data中更新相应的MSOA人口数
def parse_N(seir_data, file_name):
    with open(file_name, 'r') as f:
        csv_reader = csv.reader(f)
        csv_it = iter(csv_reader)
        next(csv_it)
        msoa_cnt = 0
        for line in csv_it:
            # line[2]: msoa code
            # line[4]: number of population
            if line[2] not in seir_data: # 如果line[2]不在seir_data字典中，跳过此行，继续下一行
                continue
            line[4] = line[4].replace(',', '') # 移除人口数中的逗号（如千位分隔符），以确保字符串可以正确转换为整数
            seir_data[line[2]]['population'] = int(line[4])
            # 使用int()函数将line[4](人口数)转换为整数并存储在seir_data[line[2]]['population']中
            msoa_cnt += 1
        print("load population data: {}".format(msoa_cnt))

# 从名为newCasesBySpecimenData_msoa_2020.csv的文件中读取MSOA的COVID-19病例数据，通过匹配MSOA代码，在字典seir_data中更新相应的MSOA病例数
def parse_covid(seir_data, file_name):
    with open(file_name, 'r') as f:
        csv_reader = csv.reader(f)
        csv_it = iter(csv_reader)
        next(csv_it)
        msoa_cnt = 0
        for line in csv_it:
            # line[2]: msoa code
            # line[10]: covid_cnt
            if line[2] not in seir_data:
                continue
            if line[10] == 'NA':
                line[10] = 0
            seir_data[line[2]]['covid'].append(int(line[10]))
            seir_data[line[2]]['covid_case'].append(int(line[10]))
            if len(seir_data[line[2]]['covid']) > 1:
                seir_data[line[2]]['covid_case'][-1] += seir_data[line[2]]['covid'][-2]
            if len(seir_data[line[2]]['covid']) > 2:
                covered = seir_data[line[2]]['covid_covered'][-1] + seir_data[line[2]]['covid'][-2]
                seir_data[line[2]]['covid_covered'].append(covered)
            else:
                seir_data[line[2]]['covid_covered'].append(0)

            # 将line[10]转换为整数并追加到seir_data[line[2]]['covid']列表中
            msoa_cnt += 1
        print("load covid data: {}".format(msoa_cnt))



# 初始化MSOA数据，读取并整合IMD、人口和COVID-19数据，清理不完整的条目
def init_data():
    imd_data = 'datas/IMD2019_MSOA.csv'
    population_data = 'datas/N.csv'
    covid_data = 'datas/newCasesBySpecimenDate_msoa_2020.csv'
    seir_dict = {}
    '''
        'MSOA' : {
            'imd' : float
            'population': int
            'covid' : []
        }
    '''
    parse_imd(seir_dict, imd_data)
    parse_N(seir_dict, population_data)
    # 删除没有人口数据的条目
    del_list = [] # 创建一个空列表，用于存储需要删除的MSOA条目键
    for key in seir_dict: # 遍历seir_dict，如果population字段为None，将该条目的键添加到del_list中
        if seir_dict[key]['population'] is None:
            del_list.append(key)
    for item in del_list: # 遍历del_list，从seir_dict中删除相应的条目
        seir_dict.pop(item)

    parse_covid(seir_dict, covid_data)
    # 删除COVID-19病例数据不完整的MSOA条目
    del_list = []
    for key in seir_dict: # 遍历seir_dict，如果covid列表长度不是30（表示缺少数据），将该条目的键添加到del_list中
        if len(seir_dict[key]['covid']) != 30:
            del_list.append(key)
    for item in del_list: # 遍历del_list，从seir_dict中删除相应的条目
        seir_dict.pop(item)
    return seir_dict # 返回清理和整理后的seir_dict，其中包含完整的MSOA数据

