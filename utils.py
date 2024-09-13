from scipy.integrate import odeint

# 定义SEIR模型的微分方程
def ode_model(z, t, beta, sigma, gamma):
    # z是一个包含[S,E,I,R]四个状态变量的列表或数组
    # t是时间变量，odeint会自动传递这个参数
    # beta是感染率infection rate（传播速度the rate of spread），表示每个感染者每天平均导致的新的感染数
    # sigma是潜伏者向感染者转变的速率the rate of latent individuals becoming infectious（潜伏期时长为1/sigma）
    # gamma是康复率recovery rate（感染者向康复者转变的速率）
    # 返回值是一个列表[dSdt,dEdt,dIdt,dRdt]，代表四个状态变量相对于时间t的导数（变化率）

    S, E, I, R = z
    N = S + E + I + R
    dSdt = - beta * S * I / N
    dEdt = beta * S * I / N - sigma * E
    dIdt = sigma * E - gamma * I
    dRdt = gamma * I
    return [dSdt, dEdt, dIdt, dRdt]

# 使用odeint函数求解ODE(Ordinary Differential Equation，常微分方程)
def ode_solver(t, initial_conditions, params):
    # t是时间序列（数组），表示求解ODE的时间点
    # initial_conditions是包含初始条件的元组(initS,initE,initI,initR,initN)，分别表示易感、潜伏、感染、康复人群和总人群的初始数量
    # params是包含SEIR模型参数的字典，包含beta、sigma和gamma
    # 返回值res是一个二维数组，每行表示时间序列t中的各个时间点的状态[S.E.I,R]
    initE, initI, initR, initN = initial_conditions
    beta, sigma, gamma = params['beta'].value, params['sigma'].value, params['gamma'].value
    initS = initN - (initE + initI + initR)
    res = odeint(ode_model, [initS, initE, initI, initR], t, args=(beta, sigma, gamma))
    return res

# 计算模型预测值和真实数据之间的误差
def error(params, initial_conditions, tspan, data):
    # params是包含SEIR模型参数的字典，包含beta、sigma和gamma
    # initial_conditions是包含初始条件的元组(initS,initE,initI,initR,initN)
    # tspan是时间范围（时间序列）
    # data是实际观察到的数据，用于与模型预测结果进行比较
    # 返回值是模型预测值sol与实际数据data之间的误差，作为一个展平数组
    # 展平数组是指将一个多维数组转换为一维数组的过程，展平操作将数组的所有元素按行或列顺序依次排列成一个简单的线性序列
    sol = ode_solver(tspan, initial_conditions, params)
    # ode_solver函数使用odeint求解SEIR模型的常微分方程，返回的sol是一个包含模型状态(S、E、I、R)的二维数组
    # sol的每一行代表时间tspan中的一个时间点对应的状态[S,E,I,R]
    return (sol[:, 2:3] - data).ravel()
    # 取出sol的第三列（即I，感染者人数）与实际数据data比较，返回误差的展平数组，用于优化或拟合过程
    # : 表示选择所有行，2:3表示选择第三列
    # sol[:,2:3]会选择sol的第三列（I列），并保持二维数组的结构，这是因为切片2:3生成的是一个包含所有行但仅包含列索引在2到3范围内的二维数组
    # 使用2:3而不是2是为了保持切片操作的结果是二维数组
    # .ravel()方法将误差数组展平为一维数组
