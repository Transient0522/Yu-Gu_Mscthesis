from utils import error
from lmfit import minimize, Parameters
import numpy as np

# 使用SEIR模型和lmfit库来估计模型参数(beta,sigma,gamma)，以使模型预测的感染者数据与实际数据最匹配
def estimate_par(es_data):
    # es_data是一个字典，包含了MSOA的疫情数据，具体字段有IMD、population和COVID-19

    '''
        'MSOA' : {
            'imd' : float
            'population': int
            'covid' : []
        }
    '''

    # 初始条件
    initN = es_data['population'] # 总人口数
    initE = 0                     # 初始潜伏者人数
    initI = 1                     # 初始感染者人数
    initR = 0                     # 初始康复者人数
    initial_conditions = [initE, initI, initR, initN] # 将这些初始条件组合成一个列表，以便在模型中使用

    # 从模拟中获取参数的初始估计值
    beta = 1.14
    sigma = 0.02
    gamma = 0.02

    # 使用lmfit库的Parameters对象来定义模型参数并设置其初始值及约束(min=0, max=10)
    # lmfit库的Parameters对象是一个用于存储和管理模型参数的容器，允许用户定义参数的初始值、边界约束及其他与参数优化相关的属性
    # Parameters对象的主要功能：定义和管理多个参数；控制参数的优化；简化参数的读取和写入
    # 创建Parameters对象
    params = Parameters()
    # 添加参数
    params.add('beta', value = beta, min = 0, max = 10)
    params.add('sigma', value = sigma, min = 0, max = 10)
    params.add('gamma', value = gamma, min = 0, max = 10)

    # 设置预测的时间跨度
    days = 30
    tspan = np.arange(0, days, 1)
    # np.arange是Numpy提供的一个函数，用于生成一个等差数列
    # 参数(0, days, 1)表示生成一个从0到days-1的序列，步长为1
    # tspan是一个从0到29的整数数组

    # 实际感染数据
    data = es_data['covid_case']

    # 使用lmfit库的minimize函数，通过最小化误差函数error来优化参数params
    # minimize函数用于执行
    #
    # 最小二乘优化，它通过调整参数使模型与数据之间的差异（误差）最小化
    # error是用户定义的误差函数，它接受参数、初始条件、时间范围和实际数据作为输入，并返回模型预测值与实际数据之间的误差
    # params是Parameters对象，包含了需要优化的参数，这些参数会在优化过程中被调整，以使误差函数返回的值最小
    # args是传递给error函数的其他参数
    # method='leastsq'表示使用非线性最小二乘法进行优化
    # 最小二乘法尝试找到参数集，使得模型预测值与实际观测数据之间的误差的平方和最小
    # 优化过程的工作原理：
    # 1.初始参数估计：以给定的初始参数(beta,sigma,gamma)开始，计算误差函数的值
    # 2.调整参数：minimize函数会逐步调整这些参数，以最小化误差函数的返回值
    # 3.收敛：当误差函数的值达到一个最小值或满足某个收敛准则时，优化过程停止
    # 4.返回结果：result是一个包含优化结果的对象，它存储了优化后的参数值、优化过程的状态、拟合优度等信息
    result = minimize(error, params, args = (initial_conditions, tspan, data), method = 'leastsq')

    # result对象包含了优化的详细信息和结果：
    # result.params:优化后的参数
    # result.success:一个布尔值，表示优化是否成功
    # result.chisqr:最小化的误差平方和
    # result.nfev:函数被调用的次数
    # result.message:优化过程中返回的状态信息

    # 保存拟合结果
    es_data['estimate_res'] = result
    es_data['beta'] = result.params['beta'].value
    es_data['sigma'] = result.params['sigma'].value
    es_data['gamma'] = result.params['gamma'].value
