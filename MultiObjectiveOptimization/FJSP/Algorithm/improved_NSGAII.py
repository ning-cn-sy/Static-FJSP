import time
from functools import cmp_to_key
from typing import Generator, List, TypeVar

from MultiObjectiveOptimization.FJSP.Algorithm.YcjMutation import ycjMutation

try:
    import dask
    from distributed import Client, as_completed
except ImportError:
    pass

from jmetal.algorithm.singleobjective.genetic_algorithm import GeneticAlgorithm
from jmetal.config import store
from jmetal.core.algorithm import Algorithm, DynamicAlgorithm, EvolutionaryAlgorithm
from jmetal.core.operator import Crossover, Mutation, Selection
from jmetal.core.problem import DynamicProblem, Problem
from jmetal.operator import BinaryTournamentSelection
from jmetal.util.comparator import Comparator, DominanceComparator, MultiComparator, ObjectiveComparator
from jmetal.util.density_estimator import CrowdingDistance
from jmetal.util.evaluator import Evaluator
from jmetal.util.ranking import FastNonDominatedRanking
from jmetal.util.replacement import (
    RankingAndDensityEstimatorReplacement,
    RemovalPolicyType,
)
from jmetal.util.termination_criterion import TerminationCriterion

S = TypeVar("S")
R = TypeVar("R")


class i_GeneticAlgorithm(EvolutionaryAlgorithm[S, R]):
    def __init__(
            self,
            problem: Problem,
            population_size: int,
            offspring_population_size: int,
            mutation: Mutation,
            crossover: Crossover,
            neighborhood: Mutation,
            selection: Selection = BinaryTournamentSelection(ObjectiveComparator(0)),
            termination_criterion: TerminationCriterion = store.default_termination_criteria,
            population_generator: Generator = store.default_generator,
            population_evaluator: Evaluator = store.default_evaluator,
            solution_comparator: Comparator = ObjectiveComparator(0)
    ):
        super(i_GeneticAlgorithm, self).__init__(
            problem=problem, population_size=population_size, offspring_population_size=offspring_population_size
        )
        self.mutation_operator = mutation
        self.crossover_operator = crossover
        self.neighborhood = neighborhood

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
                self.neighborhood.execute(solution)
                offspring_population.append(solution)
                if len(offspring_population) >= self.offspring_population_size:
                    break

        return offspring_population

    def replacement(self, population: List[S], offspring_population: List[S]) -> List[S]:
        population.extend(offspring_population)

        population.sort(key=cmp_to_key(self.solution_comparator.compare))

        return population[: self.population_size]

    def get_result(self) -> R:
        return self.solutions[0]

    def get_name(self) -> str:
        return "Genetic algorithm"


class I_NSGAII(i_GeneticAlgorithm[S, R]):
    def __init__(
            self,
            problem: Problem,
            population_size: int,
            offspring_population_size: int,
            mutation: Mutation,
            crossover: Crossover,
            neighborhood: Mutation,
            selection: Selection = BinaryTournamentSelection(
                MultiComparator([FastNonDominatedRanking.get_comparator(), CrowdingDistance.get_comparator()])
            ),
            termination_criterion: TerminationCriterion = store.default_termination_criteria,
            population_generator: Generator = store.default_generator,
            population_evaluator: Evaluator = store.default_evaluator,
            dominance_comparator: Comparator = store.default_comparator,
    ):
        """
        NSGA-II implementation as described in

        * K. Deb, A. Pratap, S. Agarwal and T. Meyarivan, "A fast and elitist
          multiobjective genetic algorithm: NSGA-II," in IEEE Transactions on Evolutionary Computation,
          vol. 6, no. 2, pp. 182-197, Apr 2002. doi: 10.1109/4235.996017

        NSGA-II is a genetic algorithm (GA), i.e. it belongs to the evolutionary algorithms (EAs)
        family. The implementation of NSGA-II provided in jMetalPy follows the evolutionary
        algorithm template described in the algorithm module (:py:mod:`jmetal.core.algorithm`).

        .. note:: A steady-state version of this algorithm can be run by setting the offspring size to 1.

        :param problem: The problem to solve.
        :param population_size: Size of the population.
        :param mutation: Mutation operator (see :py:mod:`jmetal.operator.mutation`).
        :param crossover: Crossover operator (see :py:mod:`jmetal.operator.crossover`).
        """
        super(I_NSGAII, self).__init__(
            problem=problem,
            population_size=population_size,
            offspring_population_size=offspring_population_size,
            mutation=mutation,
            crossover=crossover,
            neighborhood=neighborhood,
            selection=selection,
            termination_criterion=termination_criterion,
            population_evaluator=population_evaluator,
            population_generator=population_generator,
        )
        self.dominance_comparator = dominance_comparator

    def replacement(self, population: List[S], offspring_population: List[S]) -> List[List[S]]:
        """This method joins the current and offspring populations to produce the population of the next generation
        by applying the ranking and crowding distance selection.

        :param population: Parent population.
        :param offspring_population: Offspring population.
        :return: New population after ranking and crowding distance selection is applied.
        """
        ranking = FastNonDominatedRanking(self.dominance_comparator)
        density_estimator = CrowdingDistance()

        r = RankingAndDensityEstimatorReplacement(ranking, density_estimator, RemovalPolicyType.ONE_SHOT)
        solutions = r.replace(population, offspring_population)

        return solutions

    def get_result(self) -> R:
        return self.solutions

    def get_name(self) -> str:
        return "I_NSGAII"
