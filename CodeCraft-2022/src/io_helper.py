import numpy as np


# 打包注意：1. 添加\r  2.删掉所有路径前面的.

def read_data():
    with open('./data/config.ini', 'r') as reader:
        qos_constraint = int(reader.readlines()[1].strip().split('=')[1])
        
        
    # get demand
    with open('./data/demand.csv', 'r') as reader:
        lines = reader.readlines()
        idx_user_list = lines[0].rstrip().split(',')[1:]   # idx_list
        user_index_dic = {}
        for index in range(len(idx_user_list)):
            user_index_dic[idx_user_list[index]] = index
        time_list = []
        demand_matrix = np.zeros((len(lines) - 1, len(idx_user_list)), dtype=np.int32) # demand_matrix
        for i in range(len(lines) - 1):
            content = lines[i + 1].rstrip().split(',')
            time_list.append(content[0])
            content = content[1:]
            for j in range(len(idx_user_list)):
                demand_matrix[i, j] = int(content[j])

    # get bandwidth
    with open('./data/site_bandwidth.csv', 'r') as reader:
        lines = reader.readlines()
        idx_site_list = []
        site_index_dic = {}
        bandwidth = []
        for line in lines[1:]:
            content = line.rstrip().split(',')
            idx_site_list.append(content[0])
            bandwidth.append(int(content[1]))
        bandwidth = np.array(bandwidth)
        for index in range(len(idx_site_list)):
            site_index_dic[idx_site_list[index]] = index

   
    # get qos
    with open('./data/qos.csv', 'r') as reader:
        lines = reader.readlines()
        qos_matrix = np.zeros((len(idx_user_list), len(idx_site_list)), dtype=np.int32)
        tmp_user_list = lines[0].rstrip().split(',')[1:]
        for i in range(len(lines) - 1):
            content = lines[i + 1].rstrip().split(',')
            site_index = site_index_dic[content[0]]
            for j in range(len(content) - 1):
                user_index = user_index_dic[tmp_user_list[j]]
                qos_matrix[user_index][site_index] = int(content[j + 1])
    #      return Q,       idx_user_list, idx_site_list, D,             Y,          C,         T
    return qos_constraint, idx_user_list, idx_site_list, demand_matrix, qos_matrix, bandwidth, time_list


def output_result(M, N, X, T):
    # M: 用户ID列表
    # N: 边缘节点ID列表
    # X: |T| * |M|行，|N|列
    # T: 时刻列表
    with open('./output/solution.txt', 'w') as writer:
        for t in range(len(T)):
            for m in range(len(M)):
                header = M[m]
                strategy = X[t * len(M) + m]
                allocated_index = np.argwhere(strategy > 0).flatten()
                part_list = []
                for site_index in allocated_index:
                    part = '<{0},{1}>'.format(N[site_index], strategy[site_index])
                    part_list.append(part)
                if len(part_list) > 0:
                    writer.write(header + ':' + ','.join(part_list) + '\n')
                else:
                    writer.write(header + ':' + '\n')