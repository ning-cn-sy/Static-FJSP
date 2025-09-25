# -*- coding: utf-8 -*-
# @Time    : 2024/7/10 14:55
# @Author  : XXX
# @Site    : 
# @File    : lalalalalla.py
# @Software: PyCharm 
# @Comment :


from functools import cmp_to_key
from typing import List, TypeVar

from jmetal.config import store
from jmetal.core.algorithm import EvolutionaryAlgorithm
from jmetal.core.operator import Crossover, Mutation, Selection, Operator
from jmetal.core.problem import Problem
from jmetal.operator import BinaryTournamentSelection, BestSolutionSelection
from jmetal.util.comparator import Comparator, ObjectiveComparator
from jmetal.util.evaluator import Evaluator
from jmetal.util.generator import Generator
from jmetal.util.termination_criterion import TerminationCriterion

from MultiObjectiveOptimization.FJSP_MR.Util.Neiborhood_search_operator import Neighborhood_search

import pymannkendall as mk

S = TypeVar("S")
R = TypeVar("R")

"""
.. module:: genetic_algorithm
   :platform: Unix, Windows
   :synopsis: Implementation of Genetic Algorithms.
.. moduleauthor:: Antonio J. Nebro <antonio@lcc.uma.es>, Antonio Benítez-Hidalgo <antonio.b@uma.es>
"""


class Genetic_Algorithm(EvolutionaryAlgorithm[S, R]):
    def __init__(
            self,
            problem: Problem,
            population_size: int,
            offspring_population_size: int,
            width: int,
            neighborhood_iter: int,
            mutation: Mutation,
            crossover: Crossover,
            neighborhood: Neighborhood_search,
            selection: Selection,
            termination_criterion: TerminationCriterion = store.default_termination_criteria,
            population_generator: Generator = store.default_generator,
            population_evaluator: Evaluator = store.default_evaluator,
            solution_comparator: Comparator = ObjectiveComparator(0),
    ):
        super(Genetic_Algorithm, self).__init__(
            problem=problem, population_size=population_size, offspring_population_size=offspring_population_size
        )
        self.mutation_operator = mutation
        self.crossover_operator = crossover
        self.neighborhood_operator = neighborhood
        self.solution_comparator = solution_comparator

        self.selection_operator = selection

        self.population_generator = population_generator
        self.population_evaluator = population_evaluator

        self.termination_criterion = termination_criterion
        self.observable.register(termination_criterion)

        self.mating_pool_size = (
                self.offspring_population_size
                * self.crossover_operator.get_number_of_parents()
                // self.crossover_operator.get_number_of_children()
        )

        if self.mating_pool_size < self.crossover_operator.get_number_of_children():
            self.mating_pool_size = self.crossover_operator.get_number_of_children()

        self.objectives = []
        self.width = width
        self.neighborhood_iter = neighborhood_iter

    def create_initial_solutions(self) -> List[S]:
        return [self.population_generator.new(self.problem) for _ in range(self.population_size)]

    def evaluate(self, population: List[S]):
        return self.population_evaluator.evaluate(population, self.problem)

    def stopping_condition_is_met(self) -> bool:
        return self.termination_criterion.is_met

    def selection(self, population: List[S]):
        mating_population = []

        for _ in range(self.mating_pool_size):
            solution = self.selection_operator.execute(population)
            mating_population.append(solution)

        return mating_population

    def reproduction(self, mating_population: List[S]) -> List[S]:
        number_of_parents_to_combine = self.crossover_operator.get_number_of_parents()

        if len(mating_population) % number_of_parents_to_combine != 0:
            raise Exception("Wrong number of parents")

        offspring_population = []

        for i in range(0, self.offspring_population_size, number_of_parents_to_combine):
            parents = []
            for j in range(number_of_parents_to_combine):
                parents.append(mating_population[i + j])

            offspring = self.crossover_operator.execute(parents)

            for solution in offspring:
                self.mutation_operator.execute(solution)
                offspring_population.append(solution)
                if len(offspring_population) >= self.offspring_population_size:
                    break
        sorted_offspring_population = sorted(offspring_population, key=lambda x: x.objectives[0])
        self.objectives.append(self.get_result().objectives[0])
        # flag 为 True 进行邻域搜索
        flag = self.need_Neighborhood_search(self.objectives, 500)
        if flag == True:
            # 进行几次邻域搜索
            # 可以在某个范围之后搜索次数开始衰减
            # for j in range(self.neighborhood_iter):
            for j in range(1):
                # 对哪些解进行邻域搜索
                for i, solution in enumerate(sorted_offspring_population):
                    if i < len(sorted_offspring_population) / 2:
                        sorted_offspring_population[i] = self.neighborhood_operator.execute(
                            sorted_offspring_population[i])
                        sorted_offspring_population = sorted(sorted_offspring_population, key=lambda x: x.objectives[0])
            return sorted_offspring_population
        else:
            return offspring_population

    def need_Neighborhood_search(self, objectives_list, total_generations):
        ### 自适应步长
        cur_generations = len(objectives_list)
        max_range = 30
        min_range = 10
        # width = int(min_range + (max_range - min_range) * (cur_generations / total_generations))
        growth_factor = 0.1
        factor = 0.4
        # width = int(0.1 * len(objectives_list))
        if len(objectives_list) > 300 and len(objectives_list) % 20 == 0:
            # if cur_generations > 99:
            begin_node = int(factor * len(objectives_list))
            result = mk.original_test(objectives_list[cur_generations - self.width:cur_generations], alpha=0.05)
            # width = width * growth_factor
            if result.trend == 'no trend':
                return True
        return 0

    def replacement(self, population: List[S], offspring_population: List[S]) -> List[S]:
        population.extend(offspring_population)

        population.sort(key=cmp_to_key(self.solution_comparator.compare))

        return population[: self.population_size]

    def get_result(self) -> R:
        return self.solutions[0]

    def get_name(self) -> str:
        return "Genetic algorithm"
