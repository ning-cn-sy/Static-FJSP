"""
同时输出Pareto图和均值收敛图
"""

import time
import numpy as np
from brokenaxes import brokenaxes
from jmetal.algorithm.multiobjective import NSGAII
from jmetal.logger import get_logger
from jmetal.operator import PMXCrossover, PermutationSwapMutation
from jmetal.util.termination_criterion import StoppingByEvaluations
from matplotlib import pyplot as plt, rcParams
from config.CargoVRP import Cargo
from Algorithm.VRPProblem import VRPProblem

config = {
    "font.family": 'Times New Roman',  # 设置字体类型
    "font.size": 12,
}

rcParams.update(config)
# 日志,不用管
logger = get_logger(__name__)

# TODO 准备cargolist
cargo01 = Cargo("cargo2", 24, [1, 5, 3], [100, 600])
cargo02 = Cargo("cargo4", 28, [1, 2, 3], [200, 600])
cargo03 = Cargo("cargo6", 19, [1, 3, 5], [200, 600])
cargo04 = Cargo("cargo9", 16, [1, 4, 2], [300, 700])
cargo05 = Cargo("cargo12", 18, [1, 6, 4], [300, 700])
cargo06 = Cargo("cargo15", 26, [1, 3, 2], [300, 600])
cargo07 = Cargo("cargo17", 34, [1, 2, 4], [180, 650])
cargo08 = Cargo("cargo20", 19, [1, 6, 5], [100, 500])
cargo09 = Cargo("cargo22", 29, [1, 3, 5], [200, 700])
cargo10 = Cargo("cargo24", 12, [1, 2, 4], [300, 800])
cargo11 = Cargo("cargo27", 15, [1, 6, 4], [150, 700])
cargo12 = Cargo("cargo30", 17, [1, 4, 5], [500, 1000])
cargo13 = Cargo("cargo33", 26, [1, 5, 3], [10, 150])
cargo14 = Cargo("cargo36", 30, [1, 4, 2], [150, 600])
cargo15 = Cargo("cargo39", 23, [1, 3, 2], [300, 600])
cargo16 = Cargo("cargo43", 26, [1, 1, 4], [10, 500])
cargo17 = Cargo("cargo3", 24, [2, 6, 4], [500, 700])
cargo18 = Cargo("cargo5", 31, [2, 4, 5], [150, 400])
cargo19 = Cargo("cargo8", 36, [2, 6, 3], [150, 500])
cargo20 = Cargo("cargo11", 16, [2, 5, 1], [300, 600])
cargo21 = Cargo("cargo14", 37, [2, 1, 5], [200, 500])
cargo22 = Cargo("cargo19", 22, [2, 4, 3], [150, 300])
cargo23 = Cargo("cargo23", 37, [2, 6, 3], [200, 600])
cargo24 = Cargo("cargo26", 18, [2, 4, 5], [300, 900])
cargo25 = Cargo("cargo29", 34, [2, 5, 3], [80, 950])
cargo26 = Cargo("cargo32", 11, [2, 3, 5], [150, 700])
cargo27 = Cargo("cargo35", 18, [2, 1, 3], [200, 700])
cargo28 = Cargo("cargo38", 36, [2, 6, 1], [10, 950])
cargo29 = Cargo("cargo42", 11, [2, 2, 2], [250, 800])
cargo30 = Cargo("cargo44", 15, [2, 2, 5], [200, 700])

cargolist = [cargo01, cargo02, cargo03, cargo04, cargo05,
             cargo06, cargo07, cargo08, cargo09, cargo10,
             cargo11, cargo12, cargo13, cargo14, cargo15,
             cargo16, cargo17, cargo18, cargo19, cargo20,
             cargo21, cargo22, cargo23, cargo24, cargo25,
             cargo26, cargo27, cargo28, cargo29, cargo30]

# 定义Problem,要传参,传坐标
problem = VRPProblem(Cargolist=cargolist)
# 一些算法参数
population_size = 200
offspring_population_size = population_size
crossover_probability = 0.7
crossover_distribution_index = 20
mutation_probability = 0.25
mutation_distribution_index = 20
max_evaluations = population_size * 200

algorithm = NSGAII(
    problem=problem,
    population_size=population_size,
    offspring_population_size=offspring_population_size,
    mutation=PermutationSwapMutation(probability=mutation_probability),
    crossover=PMXCrossover(probability=crossover_probability),
    termination_criterion=StoppingByEvaluations(max_evaluations=max_evaluations)
)

# 新调用方式
"""Execute the algorithm_old."""
algorithm.start_computing_time = time.time()

logger.debug("Creating initial set of solutions...")
algorithm.solutions = algorithm.create_initial_solutions()

logger.debug("Evaluating solutions...")
algorithm.solutions = algorithm.evaluate(algorithm.solutions)

logger.debug("Initializing progress...")
algorithm.init_progress()

logger.debug("Running main loop until termination criteria is met")

objectivesMean = []
processData = []
F1 = []
F2 = []
F1_mean = []
F2_mean = []
i = 0
while not algorithm.stopping_condition_is_met():
    for solution in algorithm.solutions:
        F1.append(solution.objectives[0])
        F2.append(solution.objectives[1])
    F1_mean.append(np.mean(F1))  # 每次迭代，所有个体的F1的均值
    F2_mean.append(np.mean(F2))  # 每次迭代，所有个体的F2的均值
    F1.clear()
    F2.clear()
    # objectivesMean.append(algorithm_old.solutions[0].objectives)  # 存放每一代中每个子代的函数平均值
    # processData.append([i for i in algorithm_old.solutions[0].variables])  # 存放每一代中排序第一的子代的编码
    print("第%d次" % i)
    # print(processData[0])
    print('-----------------------------------------------------------------------------------------------------------')
    # print(processData[len(processData) - 1])
    algorithm.step()
    i = i + 1
    algorithm.update_progress()
logger.debug("Finished!")

algorithm.total_computing_time = time.time() - algorithm.start_computing_time
solutions = algorithm.get_result()

iterations = range(1, i + 1)
bax = brokenaxes(ylims=((400, 620), (5580, 5800)), wspace=0.005)
bax.plot(iterations, F1_mean, label='Total distance')
bax.plot(iterations, F2_mean, label='Time window of punishment')

# bax.set_xlabel('Iterations')
# bax.set_ylabel('Mean Value')
# bax.set_title('F1_mean and F2_mean over Iterations')
bax.legend()
# plt.show()


# 最后一代的Pareto图
last_data = []
for solution in solutions:
    last_data.append(solution.objectives)
x = [point[0] for point in last_data]
y = [point[1] for point in last_data]

plt.figure()
plt.scatter(x, y, s=20)
plt.xlabel('F1')
plt.ylabel('F2')
plt.show()


# # 存储数据
# output_directory = 'D:/Desktop/'
# file_name = "1.csv"
# file_path = os.path.join(output_directory, file_name)
# with open(file_path, 'w', newline='', encoding='utf-8') as file:
#     writer = csv.writer(file)
#     writer.writerow(['X', 'Y'])  # 写入文件标题
#     solutions = algorithm_old.get_result()
#     for solution in solutions:
#         writer.writerow([solution.objectives[0], solution.objectives[1]])
#
# print("数据成功保存到指定的 CSV 文件目录中。")
