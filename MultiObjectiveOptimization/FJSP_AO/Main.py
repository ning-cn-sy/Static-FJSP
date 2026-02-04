# -*- coding: utf-8 -*-
# @Time    : 2024/12/28 14:02
# @Author  : 宁诗铎
# @Site    : 
# @File    : Main.py
# @Software: PyCharm 
# @Comment : 装配调度问题的主函数

import csv
import os
import time
import uuid
from multiprocessing import Process

from jmetal.logger import get_logger
from jmetal.operator.crossover import CompositeCrossover, PMXCrossover, IntegerSBXCrossover
from jmetal.operator.mutation import CompositeMutation, PermutationSwapMutation, IntegerPolynomialMutation
from jmetal.util.termination_criterion import StoppingByEvaluations
from tqdm import tqdm

from MultiObjectiveOptimization.FJSP_AO.Algrithm.Decode import Decode
from MultiObjectiveOptimization.FJSP_AO.Algrithm.FJSP_AO_Problem import FJSP_AO_Problem
from MultiObjectiveOptimization.FJSP_AO.Algrithm.improved_genetic_algorithm import improved_genetic_algorithm
from MultiObjectiveOptimization.FJSP_AO.Util.Plot_util.Plot_Func import plot_gantt_chart, \
    plot_line
from MultiObjectiveOptimization.FJSP_AO.Util.Plot_util.Plot_point_Func import plot_points_and_connections_by_jobs
from MultiObjectiveOptimization.FJSP_AO.Util.Pub_func import get_cur_time, time_format, get_time_delta
from MultiObjectiveOptimization.FJSP_AO.Util.Instance.Instance_read_generator import Instance_read_generator_by_fjs
from MultiObjectiveOptimization.FJSP_AO.Util.distinct_graph.Draw_distinct_graph import distinct_graph


class Main():
    def __init__(self):
        self.TARGET_FOLDER = "D:\pycharmproject\MultiObjectiveOptimization\FJSP_AO_test\Outcome"
        self.path1 = "D:\pycharmproject\MultiObjectiveOptimization\FJSP_AO\Example\Example_AB"
        self.path = "D:\pycharmproject\MultiObjectiveOptimization\FJSP_AO\Example\Example_AB"
        self.distinct = False
        self.op_str = [0]
        self.x = [1]
        self.type = ["AB"]
        self.init_flag = [False]
        self.instance = [
            [self.path1 + "\MFJS08.fjs"
             ],
            [
                self.path + "\MFJS08.fjs"
            ]
        ]
        self.cross = [0.8]
        self.mutation = [0.2]
        self.iteration = [self.instance, self.op_str, self.cross, self.mutation, self.init_flag, self.x, self.type]

        self.i = 0
        os.makedirs(self.TARGET_FOLDER, exist_ok=True)

    def run_once(self, jobs, machines, astyles, need_styles, decoding_flag, init_flag, population_size=100,
                 offspring_population_size=100,
                 crossover_probability=1.0, mutation_probability=0.5, iterations=900):
        """
        运行一次多目标优化算法（NSGA-II），并返回优化过程中的解和目标值。

        参数:
        jobs (list): 工作任务列表，包含任务的详细信息。
        machines (list): 机器列表，包含机器的详细信息。
        astyles (list): 工艺样式的列表。
        flag (str): 标记用于指定算法或优化目标的类型。
        population_size (int): 种群大小，默认为100。
        offspring_population_size (int): 子代种群大小，默认为100。
        crossover_probability (float): 交叉概率，默认为1.0。
        mutation_probability (float): 变异概率，默认为0.5。
        iterations (int): 最大迭代次数，默认为900。

        返回:
        solutions (list): 优化后的解集。
        objectives (list): 每代的目标值记录。
        objective1s (list): 目标1的变化过程。
        """

        # 初始化问题实例
        problem = FJSP_AO_Problem(jobs, machines, astyles, need_styles, decoding_flag=decoding_flag,
                                  init_flag=init_flag)

        # 初始化日志记录器
        logger = get_logger(__name__)

        # 定义最大评价次数
        max_evaluations = iterations * population_size  # 最大评价次数 = 最大迭代次数 * 每代解集大小

        # 定义多目标优化算法（NSGA_II）
        algorithm = improved_genetic_algorithm(
            problem=problem,  # 定义问题实例
            population_size=population_size,
            offspring_population_size=offspring_population_size,
            # 定义复合变异算子，包括交换变异和多项式变异
            mutation=CompositeMutation([
                PermutationSwapMutation(mutation_probability),
                IntegerPolynomialMutation(mutation_probability),
                PermutationSwapMutation(mutation_probability)
            ]),
            # 定义复合交叉算子，包括部分匹配交叉 (PMX) 和整数SBX交叉
            crossover=CompositeCrossover([
                PMXCrossover(crossover_probability),
                IntegerSBXCrossover(crossover_probability),
                PMXCrossover(crossover_probability)
            ]),
            # 定义终止条件（基于最大评价次数）
            termination_criterion=StoppingByEvaluations(max_evaluations=max_evaluations)
        )

        # 记录开始时间
        algorithm.start_computing_time = time.time()

        # 初始化解决方案
        logger.debug("Creating initial set of solutions...")
        algorithm.solutions = algorithm.create_initial_solutions()  # 生成初始解集

        logger.debug("Evaluating solutions...")
        algorithm.solutions = algorithm.evaluate(algorithm.solutions)  # 评估初始解集

        # 初始化进度条
        logger.debug("Initializing progress...")
        algorithm.init_progress()  # 初始化算法进度

        logger.debug("Running main loop until termination criteria is met")
        # 初始化记录结果的变量
        objective1s = []  # 用于记录目标值1的变化过程
        objective2s = []
        processData = []  # 用于记录每次迭代的解集
        i = 0  # 迭代计数器
        progress_bar = tqdm(total=iterations)  # 显示进度条
        start_time = get_cur_time()  # 获取当前时间
        objectives = []  # 存储目标值
        # 主循环：运行直到满足终止条件
        while not algorithm.stopping_condition_is_met():
            # 记录当前解集的变量值
            processData.append([var for var in algorithm.solutions[0].variables])  # 保存当前解的变量值
            end_time = get_cur_time()  # 获取当前时间
            # 更新进度条显示信息
            progress_bar.set_postfix(_1_start_time=time_format(start_time), _2_end_time=time_format(end_time),
                                     _3_duration=get_time_delta(start_time, end_time).total_seconds())
            # 执行算法的下一步
            algorithm.step()  # 执行一步算法
            i += 1  # 更新迭代计数器
            algorithm.update_progress()  # 更新进度
            progress_bar.update(1)  # 更新进度条
            # 记录当前解的目标值
            objective, objective1, objective2 = zip(
                *[(solution.objectives[0], solution.objectives[1], solution.objectives[2]) for solution in
                  algorithm.solutions])
            objectives.append(objective)  # 记录目标值
            objective1s.append(objective1)  # 记录目标1的值
            objective2s.append(objective2)
            # plot_pareto(algorithm.solutions)
            # print()

        # 记录算法总运行时间
        algorithm.total_computing_time = time.time() - algorithm.start_computing_time

        # 获取最终解集和pareto
        result = algorithm.get_result()
        # pareto_front = get_non_dominated_front(result)
        # plot_pareto_frontier_3d(result, pareto_front)
        return result, objectives, algorithm.total_computing_time, population_size, crossover_probability, mutation_probability

    # 包装单个任务为可并行函数
    def process_task(self, params):
        i, instance, op_str, cross, mutation, init_flag, x, type = params

        # 生成数据
        jobs, machines, astyles, need_style, filename = Instance_read_generator_by_fjs(instance, x, type)

        # 运行优化算法
        strategy = "semi_active" if op_str == 0 else "active"

        solution1, objectives1, t1, pop_size, cross_prob, mut_prob = self.run_once(
            jobs, machines, astyles, need_style, strategy, init_flag,
            population_size=100,
            offspring_population_size=100,
            crossover_probability=cross,
            mutation_probability=mutation,
            iterations=10
        )

        # 绘图
        plot_line(objectives1, flag1=f"{strategy}_no_init", flag2=f"{strategy}_init")

        # 解码结果
        decode = Decode(jobs, machines, astyles, need_style)
        temp_sequence = solution1.variables[0].variables[:]
        machine_selection = solution1.variables[1].variables
        assembly_selection = solution1.variables[2].variables

        if op_str == 1:
            decode.run_active_schedule(temp_sequence, machine_selection, assembly_selection)
        elif op_str == 0:
            decode.run_semi_active_schedule(temp_sequence, machine_selection, assembly_selection)
        else:
            print("错！！！！！！！！！！！！！！！！")

        if self.distinct:
            distinct_graph(decode)

        # 生成甘特图
        group, line_filename = plot_points_and_connections_by_jobs(decode.jobs)
        if x == 1:
            csv_filename = (
                f"{type[0]}"
                f"{filename[-8:-4]}_"
                f"{solution1.objectives[0]}_"
                f"NAGA-II_{init_flag}-one-{strategy}-{pop_size}-{cross_prob}-{mut_prob}-"
                f"{t1}_"
                f"{uuid.uuid1()}.csv"
            )
        else:
            csv_filename = (
                f"{type[1]}"
                f"{filename[-8:-4]}_"
                f"{solution1.objectives[0]}_"
                f"NAGA-II_{init_flag}-two-{strategy}-{pop_size}-{cross_prob}-{mut_prob}-"
                f"{t1}_"
                f"{uuid.uuid1()}.csv"
            )
        plot_gantt_chart(decode.jobs, decode.machines, group, line_filename, csv_filename)

        # 保存数据
        data = [
            solution1.variables[0].variables,
            solution1.variables[1].variables,
            solution1.variables[2].variables,
            [solution1.objectives[0]],
            [objectives1[i][0] for i in range(len(objectives1))]
        ]
        full_path = os.path.join(self.TARGET_FOLDER, csv_filename)
        with open(full_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)

        return True

    def run(self):
        for i in range(1):
            for type in self.iteration[6]:
                for x in self.iteration[5]:
                    for init_flag in self.iteration[4]:
                        for cross in self.iteration[2]:
                            for mutation in self.iteration[3]:
                                for op_str in self.iteration[1]:
                                    if type == "AB":
                                        for instance in self.iteration[0][0]:
                                            params = i, instance, op_str, cross, mutation, init_flag, x, type
                                            self.process_task(params)
                                    else:
                                        for instance in self.iteration[0][1]:
                                            params = i, instance, op_str, cross, mutation, init_flag, x, type
                                            self.process_task(params)


# 主程序
if __name__ == "__main__":
    runner = Main()
    processes = []
    for _ in range(4):
        p = Process(target=runner.run())
        processes.append(p)
        p.start()
    for p in processes:
        p.join()
