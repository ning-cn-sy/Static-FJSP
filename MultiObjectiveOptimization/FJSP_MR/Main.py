# -*- coding: utf-8 -*-
# @Time    : 2024/6/5 14:30
# @Author  : 宁诗铎
# @Site    : 
# @File    : Main.py
# @Software: PyCharm 
# @Comment : 单次运行测试

import time
from datetime import datetime

from jmetal.algorithm.singleobjective import GeneticAlgorithm
from jmetal.operator import BestSolutionSelection
from jmetal.operator.crossover import CompositeCrossover, PMXCrossover, IntegerSBXCrossover
from jmetal.operator.mutation import CompositeMutation, ScrambleMutation, IntegerPolynomialMutation
from jmetal.util.termination_criterion import StoppingByEvaluations
from tqdm import tqdm

from MultiObjectiveOptimization.FJSP_MR.Algorithm.FJSP_MR_Problem import FJSPMR_Problem
from MultiObjectiveOptimization.FJSP_MR.Util.DrawUtil import draw_line_chart, draw_gantt_chart
from MultiObjectiveOptimization.FJSP_MR.Util.Pub_Func_generate_data import read_info

iterations = 600


def prepare_origin_genetic_alg(population_size, mutation_probability, crossover_probability, problem, iterations):
    # 后代的种群大小
    offspring_population_size = population_size
    # 最大评估次数(迭代次数 * 种群大小)
    max_evaluations = population_size * iterations
    # 准备遗传算法参数
    return GeneticAlgorithm(
        problem=problem,
        population_size=population_size,
        offspring_population_size=offspring_population_size,
        mutation=CompositeMutation([ScrambleMutation(probability=mutation_probability),
                                    IntegerPolynomialMutation(probability=mutation_probability)]),
        crossover=CompositeCrossover(
            [PMXCrossover(probability=crossover_probability), IntegerSBXCrossover(probability=crossover_probability)]),
        selection=BestSolutionSelection(),
        termination_criterion=StoppingByEvaluations(max_evaluations=max_evaluations),
    )


def run_alg(algorithm):
    """Execute the algorithm."""
    algorithm.start_computing_time = time.time()
    algorithm.solutions = algorithm.create_initial_solutions()
    algorithm.solutions = algorithm.evaluate(algorithm.solutions)
    algorithm.init_progress()
    objective_list = []
    progress_bar = tqdm(total=iterations)
    start_time = get_cur_time()
    while not algorithm.stopping_condition_is_met():
        algorithm.step()
        # .objective 要他第一个解的目标值
        objective_list.append(algorithm.solutions[0].objectives[0])
        algorithm.update_progress()
        progress_bar.set_description("Progress")
        end_time = get_cur_time()
        progress_bar.set_postfix(_1_start_time=time_format(start_time), _2_end_time=time_format(end_time),
                                 _3_duration=get_time_delta(start_time, end_time).total_seconds())
        progress_bar.update(1)
    return algorithm, objective_list


def get_time_delta(start_time, end_time):
    return end_time - start_time


def time_format(time):
    return time.strftime("%Y-%m-%d %H:%M:%S")


def get_cur_time():
    return datetime.now()


def run(width, neighborhood_iter, mutation_probability, crossover_probability, population_size,
        job_list, machine_list, auxiliary_module_list, problem):
    alg, objective_list = run_alg(
        prepare_origin_genetic_alg(population_size, mutation_probability, crossover_probability, problem, iterations))
    # alg, objective_list = run_alg(
    #     prepare_origin_genetic_alg(population_size, mutation_probability, crossover_probability,
    #                                problem, iterations))
    tasks = problem.decode(alg.get_result())
    draw_gantt_chart(tasks, machine_list, auxiliary_module_list)
    draw_line_chart(objective_list, title='总加权延迟')
    print(alg.solutions[0].objectives[0])


job_list, machine_list, auxiliary_module_list = read_info("./Example/MFJS10.fjs")
problem = FJSPMR_Problem(job_list, machine_list, auxiliary_module_list)
crossover_distribution_index = 20
width = 20
neighborhood_iter = 20
mutation_probability = 0.15
crossover_probability = 0.9
population_size = 100
run(width, neighborhood_iter, mutation_probability, crossover_probability, population_size,
    job_list, machine_list, auxiliary_module_list, problem)
