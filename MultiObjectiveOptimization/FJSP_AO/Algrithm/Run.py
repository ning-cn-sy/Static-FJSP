# -*- coding: utf-8 -*-
# @Time    : 2025/2/2 20:34
# @Author  : 宁诗铎
# @Site    : 
# @File    : Run.py
# @Software: PyCharm 
# @Comment : 运行算法类
from jmetal.algorithm.multiobjective import NSGAII
from jmetal.operator.crossover import CompositeCrossover, PMXCrossover, IntegerSBXCrossover
from jmetal.operator.mutation import CompositeMutation, PermutationSwapMutation, IntegerPolynomialMutation
from jmetal.util.termination_criterion import StoppingByEvaluations


from MultiObjectiveOptimization.FJSP_AO.Algrithm.FJSP_AO_Problem import FJSP_AO_Problem


# 优化算法类
class OptimizationAlgorithm:
    def __init__(self, jobs, machines, astyles, flag, population_size=100,
                 offspring_population_size=100, crossover_probability=1.0, mutation_probability=0.5, iterations=900):
        self.jobs = jobs
        self.machines = machines
        self.astyles = astyles
        self.flag = flag
        self.population_size = population_size
        self.offspring_population_size = offspring_population_size
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        self.iterations = iterations
        self.problem = FJSP_AO_Problem(self.jobs, self.machines, self.astyles, flag=self.flag)
        self.algorithm = NSGAII(
            problem=self.problem,
            population_size=self.population_size,
            offspring_population_size=self.offspring_population_size,
            mutation=CompositeMutation([PermutationSwapMutation(self.mutation_probability),
                                        IntegerPolynomialMutation(self.mutation_probability)]),
            crossover=CompositeCrossover(
                [PMXCrossover(self.crossover_probability), IntegerSBXCrossover(self.crossover_probability)]),
            termination_criterion=StoppingByEvaluations(max_evaluations=self.iterations * self.population_size)
        )
        # 初始化解集
        self.algorithm.solutions = self.algorithm.create_initial_solutions()
        self.algorithm.solutions = self.algorithm.evaluate(self.algorithm.solutions)

    def run_once(self):
        self.algorithm.step()  # 进行一步优化
        return self.algorithm.solutions  # 返回当前种群的解集

    def run(self):
        # 开始迭代
        for i in range(self.iterations):
            self.run_once()  # 每次优化一步

        return self.algorithm.get_result()  # 返回最终的解集
