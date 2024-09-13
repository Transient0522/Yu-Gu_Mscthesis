from parse_data import init_data
from estimate import estimate_par
from tqdm import tqdm
import numpy as np
from scipy.stats import pearsonr
from scipy.stats import spearmanr
from sklearn.metrics import mutual_info_score
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
# 分析不同区域的疫情数据，并计算每个区域的SEIR模型参数(beta、sigma和gamma)与IMD的相关性
if __name__ == '__main__':
    with open('data.pkl', 'rb') as f:
        se_dict = pickle.load(f)
    '''
        'MSOA' : {
            'imd' : float
            'population': int
            'covid' : []
        }
    '''
    cnt = 0
    imd_list = []
    beta_list = []
    sigma_list = []
    gamma_list = []
    for key in tqdm(se_dict, desc='Estimating par'):
    # 使用tqdm显示进度条，遍历每个区域的数据
    # tqdm是一个用于显示进度条的Python库，可以方便地监控代码的执行进度，提供视觉反馈
    # desc是tqdm的常用参数，用来自定义进度条的显示方式，desc使用字符串，在进度条前面显示的描述信息
        se_data = se_dict[key] # se_data是MSOA每个区域的数据

        if 'beta' not in se_data:
            continue
        ##############################################

        if se_data['sigma'] < 9:
           continue
        # 剔除beta中某种数据

        ################################################
        # 对于每个区域数据se_data，调用estimate_par(se_data)函数来估计其SEIR模型的参数
        """
            se_data['imd']
            se_data['beta']
            se_data['sigma']
            se_data['gamma']
        """
        # 提取出该区域的IMD值和估计的参数，将其分别添加到对应的列表中
        imd_list.append(se_data['imd'])
        beta_list.append(se_data['beta'])
        sigma_list.append(se_data['sigma'])
        gamma_list.append(se_data['gamma'])

    # 二元变量图和趋势线

    sns.regplot(x=imd_list, y=beta_list, ci=None)
    plt.xlabel('IMD')
    plt.ylabel('Beta')
    plt.title('Scatter Plot of IMD vs. Beta')
    plt.show()

    sns.regplot(x=imd_list, y=sigma_list, ci=None)
    plt.xlabel('IMD')
    plt.ylabel('Sigma')
    plt.title('Scatter Plot of IMD vs. Sigma')
    plt.show()

    sns.regplot(x=imd_list, y=gamma_list, ci=None)
    plt.xlabel('IMD')
    plt.ylabel('Gamma')
    plt.title('Scatter Plot of IMD vs. Gamma')
    plt.show()
    
    # 计算参数与IMD之间的皮尔逊相关系数(Pearson Correlation Coefficient)和p值，用来评估参数与IMD之间的线性关系

    # 皮尔逊相关系数(Pearson Correlation Coefficient)是一种衡量两个变量之间线性关系的统计量
    # 皮尔逊相关系数的值介于-1和1之间：1表示完全正相关；-1表示完全负相关；0表示没有线性相关性
    # 重要特性：皮尔逊相关系数假定数据是正态分布的，且主要检测的是线性关系

    # p值(p-value)用于测试相关系数的显著性
    # p值小于某个阈值（通常是0.05）表示相关系数是显著的，即两个变量之间存在线性关系
    correlation, p_value = pearsonr(imd_list, beta_list)
    print(f"IMD与beta的相关性：")
    print(f"皮尔逊相关系数: {correlation}, p值: {p_value}")

    correlation, p_value = pearsonr(imd_list, sigma_list)
    print(f"IMD与sigma的相关性：")
    print(f"皮尔逊相关系数: {correlation}, p值: {p_value}")

    correlation, p_value = pearsonr(imd_list, gamma_list)
    print(f"IMD与gamma的相关性：")
    print(f"皮尔逊相关系数: {correlation}, p值: {p_value}")

    # 计算参数与IMD之间的斯皮尔曼秩相关系数

    correlation, p_value = spearmanr(imd_list, beta_list)
    print(f"IMD与beta的相关性：")
    print(f"斯皮尔曼秩相关系数: {correlation}, p值: {p_value}")

    correlation, p_value = spearmanr(imd_list, sigma_list)
    print(f"IMD与sigma的相关性：")
    print(f"斯皮尔曼秩相关系数: {correlation}, p值: {p_value}")

    correlation, p_value = spearmanr(imd_list, gamma_list)
    print(f"IMD与gamma的相关性：")
    print(f"斯皮尔曼秩相关系数: {correlation}, p值: {p_value}")

    # 线性回归模型和回归系数

    model = LinearRegression().fit(np.array(imd_list).reshape(-1, 1), beta_list)
    r_squared = model.score(np.array(imd_list).reshape(-1, 1), beta_list)
    print(f"IMD与beta的相关性：")
    print(f"线性回归系数:{r_squared}")

    model = LinearRegression().fit(np.array(imd_list).reshape(-1, 1), sigma_list)
    r_squared = model.score(np.array(imd_list).reshape(-1, 1), sigma_list)
    print(f"IMD与sigma的相关性：")
    print(f"线性回归系数:{r_squared}")

    model = LinearRegression().fit(np.array(imd_list).reshape(-1, 1), gamma_list)
    r_squared = model.score(np.array(imd_list).reshape(-1, 1), gamma_list)
    print(f"IMD与gamma的相关性：")
    print(f"线性回归系数:{r_squared}")


    
    
