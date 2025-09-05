import random

import numpy as np
from jmetal.core.operator import Mutation
from jmetal.core.solution import PermutationSolution
from jmetal.util.ckecking import Check


class testMutation(Mutation[PermutationSolution]):
    def execute(self, solution: PermutationSolution) -> PermutationSolution:
        Check.that(type(solution) is PermutationSolution, "Solution type invalid")

        rand = random.random()

        if rand <= self.probability:
            # pos_one, pos_two = random.sample(range(solution.number_of_variables), 2)
            pos_one, pos_two = np.random.choice(range(solution.number_of_variables), 2)
            solution.variables[pos_one], solution.variables[pos_two] = (
                solution.variables[pos_two],
                solution.variables[pos_one],
            )

        return solution

    def get_name(self):
        return "测试用Mutation"
