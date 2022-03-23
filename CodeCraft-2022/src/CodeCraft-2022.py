import numpy as np
from io_helper import *

# 变量注释:
# Q: QoS约束上限
# M: 用户ID列表
# N: 边缘节点ID列表
# D: 需求矩阵
# Y: QoS矩阵 (|M|行|N|列)
# C: 带宽上限列表 ()
# T: 时刻列表

                            

Q, M, N, D, Y, C, T = read_data()


X = []   #  分配结果

for t in range(len(T)):
    idle_capacity = np.array(C)
    for m in range(len(M)):
        legal_sites = np.argwhere(Y[m] < Q).flatten()
        demand = D[t, m]
        avg_demand = demand // len(legal_sites)
        allocated = 0
        strategy = np.zeros(len(N), dtype=np.int32)
        while demand > 0:
            for index_site in legal_sites:
                if demand <= 0 or demand < avg_demand:
                    break
                if idle_capacity[index_site] >= avg_demand:
                    idle_capacity[index_site] -= avg_demand
                    allocated += avg_demand
                    strategy[index_site] += avg_demand
                    demand -= avg_demand
                # 如果site的容量不满足avg_demand
                else:
                    allocated += idle_capacity[index_site]
                    strategy[index_site] += idle_capacity[index_site]
                    demand -= idle_capacity[index_site]
                    idle_capacity[index_site] = 0
            avg_demand = demand // len(legal_sites)
            allocated = 0
            if avg_demand == 0:
                if demand == 0:
                    break
                else:
                    avg_demand = 1
        X.append(strategy)
X = np.array(X)


output_result(M, N, X, T)
