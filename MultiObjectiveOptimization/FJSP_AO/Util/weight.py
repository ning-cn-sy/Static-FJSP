import numpy as np


def generate_weights(n, beta, sigma=0.1):
    """
    生成和为 1 且有主导规则的随机权重
    :param n: 规则数量
    :param beta: 衰减参数
    :param sigma: 对数正态分布的标准差
    :return: 权重列表
    """
    # 生成初始指数衰减序列
    initial_sequence = np.exp(-beta * np.arange(n))
    # 添加对数正态分布的扰动
    perturbed_sequence = initial_sequence * np.random.lognormal(mean=0, sigma=sigma, size=n)
    # 归一化
    weights = perturbed_sequence / np.sum(perturbed_sequence)
    return weights


# 示例：生成 3 个规则的权重
n = 3
beta = 1.5
weights = generate_weights(n, beta)
np.random.shuffle(weights)
print("3 个规则打乱后的权重:", [f"{weight:.8f}" for weight in weights])

# 示例：生成 8 个规则的权重
n = 8
beta = 2
weights = generate_weights(n, beta)
np.random.shuffle(weights)
print("8 个规则打乱后的权重:", [f"{weight:.8f}" for weight in weights])