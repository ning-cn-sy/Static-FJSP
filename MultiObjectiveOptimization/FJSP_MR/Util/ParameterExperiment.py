import pandas as pd
import matplotlib.pyplot as plt

# 1. 读取CSV文件
# 假设你的CSV文件名为 `experiment_results.csv`
# 第一列为目标值，后五列为参数，最后一列为当前组合的运行次数
df = pd.read_csv("D:\论文\可重构制造系统\实验结果\正交实验\\1104\params_list.csv", header=None)
df.columns = ['target_value', 'width', 'neighborhood_iter', 'mutation_probability', 'crossover_probability', 'population_size', 'run_count','OS','CS']

# 2. 计算每组组合的十次平均目标值
grouped = df.groupby(['width', 'neighborhood_iter', 'mutation_probability', 'crossover_probability', 'population_size'])
average_target_per_combination = grouped['target_value'].mean().reset_index()
average_target_per_combination.rename(columns={'target_value': 'average_target_value'}, inplace=True)

# 3. 计算每个参数水平下的平均目标值
parameter_means = {}
parameters = ['width', 'neighborhood_iter', 'mutation_probability', 'crossover_probability', 'population_size']
parameter_levels = {
    'width': [20, 30, 40, 50],
    'neighborhood_iter': [10, 15, 20, 25],
    'mutation_probability': [0.10, 0.15, 0.20, 0.25],
    'crossover_probability': [0.80, 0.85, 0.90, 0.95],
    'population_size': [100, 200, 300, 400]
}

for param in parameters:
    parameter_means[param] = df.groupby(param)['target_value'].mean()

# 4. 绘制每个参数水平下的平均目标值（折线图）
for param, means in parameter_means.items():
    plt.figure(figsize=(8, 6))
    means.plot(kind='line', marker='o')
    plt.title(f'Average Target Value by {param.capitalize()} Levels')
    plt.xlabel(f'{param.capitalize()} Level')
    plt.ylabel('Average Target Value')
    plt.xticks(parameter_levels[param])  # 设置横坐标为指定的四个刻度
    plt.grid(True)
    plt.show()

# 输出每组组合的平均目标值
print(average_target_per_combination)
