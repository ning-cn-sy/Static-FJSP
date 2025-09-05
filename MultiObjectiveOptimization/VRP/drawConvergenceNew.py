"""
其余画收敛图的都是错的，这个对了
跑每个目标函数随迭代次数的收敛图
其中，每一代的目标函数值取所有个体的平均值
"""
import csv
import math
import os

import numpy as np
import pandas as pd
from brokenaxes import brokenaxes
from jmetal.algorithm.multiobjective import NSGAII, SPEA2, IBEA, SMPSO, RandomSearch, MOEAD
from jmetal.logger import get_logger
from jmetal.util.aggregative_function import Tschebycheff
from jmetal.util.archive import CrowdingDistanceArchive
from jmetal.util.termination_criterion import StoppingByEvaluations
import time
from matplotlib import pyplot as plt, rcParams
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import FixedLocator, FixedFormatter
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from Algorithm.AllocationOperator import AllocationPolynomialMutation, AllocationSBXCrossover
from Algorithm.AllocationOperator2 import AllocationPolynomialMutation2, AllocationSBXCrossover2
from Algorithm.CargoAllocationProblem import CAProblem
from Algorithm.CargoAllocationProblem2 import CAProblem2
from config.Cargo import Cargo
from config.Shelf import Shelf
from config.Stacker import Stacker
from util.PubFunc import drawCuboid

config = {
    "font.family": 'Times New Roman',  # 设置字体类型
    "font.size": 12,
}

rcParams.update(config)

# 准备货物信息
cargo01 = Cargo("cargo01", 17, "类别1", 0.2)
cargo02 = Cargo("cargo02", 20, "类别2", 0.7)
cargo03 = Cargo("cargo03", 30, "类别1", 0.2)
cargo04 = Cargo("cargo04", 22, "类别4", 0.5)
cargo05 = Cargo("cargo05", 15, "类别2", 0.7)
cargo06 = Cargo("cargo06", 25, "类别2", 0.7)
cargo07 = Cargo("cargo07", 16, "类别3", 0.9)
cargo08 = Cargo("cargo08", 40, "类别4", 0.5)
cargo09 = Cargo("cargo09", 28, "类别3", 0.9)
cargo10 = Cargo("cargo10", 35, "类别1", 0.2)
cargo11 = Cargo("cargo11", 15, "类别4", 0.5)
cargo12 = Cargo("cargo12", 38, "类别2", 0.7)
cargo13 = Cargo("cargo13", 29, "类别2", 0.7)
cargo14 = Cargo("cargo14", 20, "类别4", 0.5)
cargo15 = Cargo("cargo15", 12, "类别3", 0.9)
cargo16 = Cargo("cargo16", 21, "类别2", 0.7)
cargo17 = Cargo("cargo17", 8, "类别4", 0.5)
cargo18 = Cargo("cargo18", 31, "类别1", 0.2)
cargo19 = Cargo("cargo19", 22, "类别2", 0.7)
cargo20 = Cargo("cargo20", 45, "类别1", 0.2)
cargo21 = Cargo("cargo21", 30, "类别4", 0.5)
cargo22 = Cargo("cargo22", 10, "类别4", 0.5)
cargo23 = Cargo("cargo23", 32, "类别2", 0.7)
cargo24 = Cargo("cargo24", 42, "类别1", 0.2)
cargo25 = Cargo("cargo25", 24, "类别4", 0.5)
cargo26 = Cargo("cargo26", 13, "类别2", 0.7)
cargo27 = Cargo("cargo27", 32, "类别1", 0.2)
cargo28 = Cargo("cargo28", 24, "类别2", 0.7)
cargo29 = Cargo("cargo29", 51, "类别2", 0.7)
cargo30 = Cargo("cargo30", 12, "类别2", 0.7)
cargo31 = Cargo("cargo31", 7, "类别3", 0.9)
cargo32 = Cargo("cargo32", 32, "类别1", 0.2)
cargo33 = Cargo("cargo33", 13, "类别4", 0.5)
cargo34 = Cargo("cargo34", 12, "类别3", 0.9)
cargo35 = Cargo("cargo35", 41, "类别1", 0.2)
cargo36 = Cargo("cargo36", 51, "类别1", 0.2)
cargo37 = Cargo("cargo37", 12, "类别4", 0.5)
cargo38 = Cargo("cargo38", 34, "类别2", 0.7)
cargo39 = Cargo("cargo39", 21, "类别2", 0.7)
cargo40 = Cargo("cargo40", 52, "类别4", 0.5)
cargo41 = Cargo("cargo41", 41, "类别2", 0.7)
cargo42 = Cargo("cargo42", 12, "类别1", 0.2)
cargo43 = Cargo("cargo43", 3, "类别1", 0.2)
cargo44 = Cargo("cargo44", 22, "类别2", 0.7)
cargo45 = Cargo("cargo45", 43, "类别1", 0.2)
cargo46 = Cargo("cargo36", 21, "类别1", 0.2)
cargo47 = Cargo("cargo37", 20, "类别3", 0.9)
cargo48 = Cargo("cargo38", 14, "类别1", 0.2)
cargo49 = Cargo("cargo39", 41, "类别4", 0.5)
cargo50 = Cargo("cargo40", 9, "类别3", 0.9)
cargo51 = Cargo("cargo41", 21, "类别3", 0.9)
cargo52 = Cargo("cargo42", 17, "类别4", 0.5)
cargo53 = Cargo("cargo43", 31, "类别2", 0.7)
cargo54 = Cargo("cargo44", 12, "类别1", 0.2)
cargo55 = Cargo("cargo45", 35, "类别1", 0.2)
cargo56 = Cargo("cargo36", 11, "类别3", 0.9)
cargo57 = Cargo("cargo37", 27, "类别2", 0.7)
cargo58 = Cargo("cargo38", 24, "类别4", 0.5)
cargo59 = Cargo("cargo39", 21, "类别2", 0.7)
cargo60 = Cargo("cargo40", 52, "类别2", 0.7)
cargo61 = Cargo("cargo61", 23, "类别2", 0.7)
cargo62 = Cargo("cargo62", 32, "类别1", 0.2)
cargo63 = Cargo("cargo63", 42, "类别3", 0.9)
cargo64 = Cargo("cargo64", 22, "类别4", 0.5)
cargo65 = Cargo("cargo65", 4, "类别2", 0.7)
cargo66 = Cargo("cargo66", 13, "类别1", 0.2)
cargo67 = Cargo("cargo67", 14, "类别3", 0.9)
cargo68 = Cargo("cargo68", 19, "类别2", 0.7)
cargo69 = Cargo("cargo69", 52, "类别4", 0.5)
cargo70 = Cargo("cargo70", 13, "类别3", 0.9)
cargo71 = Cargo("cargo71", 34, "类别3", 0.9)
cargo72 = Cargo("cargo72", 12, "类别4", 0.5)
cargo73 = Cargo("cargo73", 17, "类别1", 0.2)
cargo74 = Cargo("cargo74", 19, "类别3", 0.9)
cargo75 = Cargo("cargo75", 9, "类别4", 0.5)

cargo_list = [cargo01, cargo02, cargo03, cargo04, cargo05,
              cargo06, cargo07, cargo08, cargo09, cargo10,
              cargo11, cargo12, cargo13, cargo14, cargo15,
              cargo16, cargo17, cargo18, cargo19, cargo20,
              cargo21, cargo22, cargo23, cargo24, cargo25,
              cargo26, cargo27, cargo28, cargo29, cargo30,
              cargo31, cargo32, cargo33, cargo34, cargo35,
              cargo36, cargo37, cargo38, cargo39, cargo40,
              cargo41, cargo42, cargo43, cargo44, cargo45,
              cargo46, cargo47, cargo48, cargo49, cargo50,
              cargo51, cargo52, cargo53, cargo54, cargo55,
              cargo56, cargo57, cargo58, cargo59, cargo60,
              cargo61, cargo62, cargo63, cargo64, cargo65,
              cargo66, cargo67, cargo68, cargo69, cargo70,
              cargo71, cargo72, cargo73, cargo74, cargo75]

# 准备货架信息
shelf1 = Shelf("shelf1", 5, 6, 1, 4)
shelf2 = Shelf("shelf2", 5, 6, 1, 4)
shelf3 = Shelf("shelf3", 5, 6, 1, 4)
shelf_list = [shelf1, shelf2, shelf3]
# shelf_list = [shelf1, shelf2]
# shelf_list = [shelf1]

# 准备堆垛机信息
stacker1 = Stacker("stacker1", 1, 1, 0.8)
stacker2 = Stacker("stacker2", 1, 1, 0.8)
stacker_list = [stacker1, stacker2]

# 日志,不用管
logger = get_logger(__name__)

# 定义Problem,要传参,传坐标
problem1 = CAProblem(cargoInfo=cargo_list, shelfInfo=shelf_list, stackerInfo=stacker_list)

# 一些算法参数
offspring_population_size = 100
crossover_probability = 0.7
crossover_distribution_index = 20
mutation_probability = 0.25
mutation_distribution_index = 20

# 定义算法

algorithm = MOEAD(
    problem=problem1,
    population_size=500,
    mutation=AllocationPolynomialMutation(probability=mutation_probability, shelfInfo=shelf_list, cargoInfo=cargo_list),
    crossover=AllocationSBXCrossover(probability=crossover_probability, shelfInfo=shelf_list, cargoInfo=cargo_list),
    aggregative_function=Tschebycheff(dimension=len(problem1.obj_directions)),
    neighbor_size=20,
    neighbourhood_selection_probability=0.9,
    max_number_of_replaced_solutions=2,
    weight_files_path='resources/MOEAD_weights',
    termination_criterion=StoppingByEvaluations(max_evaluations=500*1000)
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

F1 = []
F2 = []
F3 = []
F1_mean = []
F2_mean = []
F3_mean = []
iii = 0
while not algorithm.stopping_condition_is_met():
    for solution in algorithm.solutions:
        F1.append(solution.objectives[0])
        F2.append(solution.objectives[1])
        F3.append(solution.objectives[2])
    F1_mean.append(np.mean(F1))  # 每次迭代，所有个体的F1的均值
    F2_mean.append(np.mean(F2))  # 每次迭代，所有个体的F2的均值
    F3_mean.append(np.mean(F3))  # 每次迭代，所有个体的F3的均值
    F1.clear()
    F2.clear()
    F3.clear()
    # objectivesMean.append(algorithm_old.solutions[0].objectives)  # 存放每一代中每个子代的函数平均值
    # processData.append([i for i in algorithm_old.solutions[0].variables])  # 存放每一代中排序第一的子代的编码
    print("第%d次" % iii)
    # print(processData[0])
    # print(processData[len(processData) - 1])
    algorithm.step()
    iii = iii + 1
    algorithm.update_progress()
logger.debug("Finished!")

algorithm.total_computing_time = time.time() - algorithm.start_computing_time
solutions = algorithm.get_result()
# print(F1_mean)
# print(F2_mean)
# print(F3_mean)

data = {
    'F1_mean': F1_mean,
    'F2_mean': F2_mean,
    'F3_mean': F3_mean
}
# 创建DataFrame
df = pd.DataFrame(data)
# 导出到CSV文件
df.to_csv('D:/Desktop/solutions_data.csv', index=False)

iterations = range(1, len(F1_mean) + 1)
bax = brokenaxes(ylims=((2, 4), (8, 10.5)), wspace=0.005)
bax.plot(iterations, F1_mean, label='F1_mean')
bax.plot(iterations, F2_mean, label='F2_mean')
bax.plot(iterations, F3_mean, label='F3_mean')

bax.set_xlabel('Iterations')
bax.set_ylabel('Mean Value')

bax.legend()
plt.show()
