# -*- coding: utf-8 -*-
# @Time    : 2025/3/27 8:47
# @Author  : 
# @Site    : 
# @File    : GA_1.py
# @Software: PyCharm 
# @Comment :


import csv
import os
import time
from datetime import datetime
import random

from jmetal.algorithm.singleobjective import GeneticAlgorithm
from jmetal.operator.crossover import CompositeCrossover, IntegerSBXCrossover
from jmetal.operator.mutation import CompositeMutation, IntegerPolynomialMutation
from tqdm import tqdm

from MultiObjectiveOptimization.FJSP.Algorithm.Decode import Decode
from MultiObjectiveOptimization.FJSP.Algorithm.FJSP_Problem import FJSP_Problem

from jmetal.logger import get_logger
from jmetal.algorithm.multiobjective import NSGAII
from jmetal.operator import PMXCrossover, PermutationSwapMutation
from jmetal.util.termination_criterion import StoppingByEvaluations

from MultiObjectiveOptimization.FJSP.Algorithm.FJSP_Problem_2 import FJSP_Problem_1

from MultiObjectiveOptimization.FJSP.Util.Draw_gantt import plot_gantt_chart
from MultiObjectiveOptimization.FJSP.Util.Draw_line import plot_line

from MultiObjectiveOptimization.FJSP.Util.Read_By_FJS import readDataByFJS
from MultiObjectiveOptimization.FJSP.abcccccc import aaaSBXCrossover


def write_csv(params_list, name):
    # 文件名，可以根据需要修改
    folder_path = os.path.join("D:\\result\\a")
    # 创建文件夹（如果不存在）
    os.makedirs(folder_path, exist_ok=True)
    csv_file_name = os.path.join(folder_path, f"{name}.csv")

    # 将数据写入 CSV 文件
    with open(csv_file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        # 写入数据
        for param in params_list:
            if not isinstance(param, (list, tuple)):
                param = [param]  # 将非可迭代的 params 转换为单元素列表
            writer.writerow(param)


def get_time_delta(start_time, end_time):
    return end_time - start_time


def time_format(time):
    return time.strftime("%Y-%m-%d %H:%M:%S")


def get_cur_time():
    return datetime.now()


jobs, machines = readDataByFJS(
    "D:\PhD\Research\PythonResearch\pythonProject\MultiObjectiveOptimization\FJSP\Example\XSL01.fjs")

problem = FJSP_Problem_1(jobs, machines)

# 初始化日志记录器
logger = get_logger(__name__)

# 一些算法参数配置
population_size = 100  # 种群大小
offspring_population_size = 100  # 子代种群大小
crossover_probability = 1.0  # 交叉概率
crossover_distribution_index = 20  # 交叉分布指数
mutation_probability = 0.2  # 变异概率 0.001
mutation_distribution_index = 20  # 变异分布指数
neighborhood_probability = 0.01
iterations = 1
max_evaluations = iterations * population_size  # 最大评价次数

### 正常的NSGA-II
algorithm = GeneticAlgorithm(
    problem=problem,  # 定义问题实例
    population_size=population_size,
    offspring_population_size=offspring_population_size,
    # 定义复合变异算子，包括交换变异和多项式变异
    mutation=CompositeMutation([
        PermutationSwapMutation(mutation_probability),
        IntegerPolynomialMutation(mutation_probability)
    ]),
    # 定义复合交叉算子，包括部分匹配交叉 (PMX) 和整数SBX交叉
    crossover=CompositeCrossover([
        PMXCrossover(crossover_probability),
        # aaaSBXCrossover(crossover_probability)
        IntegerSBXCrossover(crossover_probability)
    ]),
    # 定义终止条件（基于最大评价次数）
    termination_criterion=StoppingByEvaluations(max_evaluations=max_evaluations)
)

# 使用新的方式运行算法（替代旧的调用方式）
"""Execute the algorithm."""
algorithm.start_computing_time = time.time()  # 记录开始时间

logger.debug("Creating initial set of solutions...")
algorithm.solutions = algorithm.create_initial_solutions()  # 生成初始解集

logger.debug("Evaluating solutions...")
algorithm.solutions = algorithm.evaluate(algorithm.solutions)  # 评估初始解集

logger.debug("Initializing progress...")
algorithm.init_progress()  # 初始化算法进度

logger.debug("Running main loop until termination criteria is met")
# 初始化记录结果的变量
objective1s = []  # 用于记录目标值1的变化过程
processData = []  # 用于记录每次迭代的解集
i = 0  # 迭代计数器
progress_bar = tqdm(total=iterations)
start_time = get_cur_time()
objectives = []
# 主循环：运行直到满足终止条件
while not algorithm.stopping_condition_is_met():
    # 获取当前解的目标值（fitness function，即目标值1）
    current_fitness = algorithm.solutions[0].objectives[0]
    objectives.append(current_fitness)
    # 记录当前解的目标值
    objective1s.append(current_fitness)

    # 记录当前解集的变量值
    processData.append([var for var in algorithm.solutions[0].variables])
    progress_bar.set_description("Progress")
    end_time = get_cur_time()

    progress_bar.set_postfix(_1_start_time=time_format(start_time), _2_end_time=time_format(end_time),
                             _3_duration=get_time_delta(start_time, end_time).total_seconds())
    # 执行算法的下一步
    algorithm.step()
    i += 1
    algorithm.update_progress()
    progress_bar.update(1)

# 记录算法总运行时间
algorithm.total_computing_time = time.time() - algorithm.start_computing_time

plot_line(objectives)
write_csv(objectives, "bbb")
# 获取最终解集
solutions = algorithm.get_result()

solution = solutions

# 提取当前解中的作业顺序
temp_sequence = solution.variables[0].variables[:]

# 提取机器分配方案
machine_selection = solution.variables[1].variables

decode = Decode(jobs, machines)
# 运行解码器，计算调度方案
decode.run_semi_active_schedule(temp_sequence, machine_selection)
plot_gantt_chart(decode.jobs, decode.machines)
