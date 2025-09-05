import math

from jmetal.core.problem import PermutationProblem
from jmetal.core.solution import PermutationSolution, S


class TSPProblem(PermutationProblem):

    def __init__(self, number_of_variables: int = 30, zuobiao=[]):
        """:param number_of_variables: Number of decision variables of the problem."""
        super(TSPProblem, self).__init__()
        # 定义obj数量，现在只有一个,另一个假设
        self.obj_directions = [self.MINIMIZE, self.MAXIMIZE]
        self.obj_labels = ["路径长度", "电量"]
        # self.lower_bound = number_of_variables * [0.0]
        # self.upper_bound = number_of_variables * [1.0]
        self.zuobiao = zuobiao

    def number_of_objectives(self) -> int:
        return len(self.obj_directions)

    def number_of_constraints(self) -> int:
        return 0

    def number_of_variables(self) -> int:
        return len(self.zuobiao)

    def evaluate(self, solution: PermutationSolution) -> PermutationSolution:
        # shunxu = solution.variables[0]
        shunxu = [yuansu for yuansu in solution.variables]
        # 这里可以弄成如何计算适应度函数
        obj1 = 0
        for i in range(1, len(shunxu)):
            curCity = shunxu[i]
            lastCity = shunxu[i - 1]
            curCityx = self.zuobiao[curCity][0]
            curCityy = self.zuobiao[curCity][1]
            lastCityx = self.zuobiao[lastCity][0]
            lastCityy = self.zuobiao[lastCity][1]
            obj1 += math.sqrt((curCityx - lastCityx) ** 2 + (curCityy - lastCityy) ** 2)

        # print(shunxu)
        # print(obj1)
        solution.objectives[0] = obj1
        solution.objectives[1] = 0

        return solution

    def create_solution(self) -> S:
        """Creates a random_search solution to the problem.
        :return: Solution."""
        # 可以直接重写Solution
        new_solution = PermutationSolution(
            number_of_variables=self.number_of_variables(), number_of_objectives=self.number_of_objectives()
        )
        # my_list = [i for i in range(len(self.zuobiao))]
        # random.shuffle(my_list)
        # new_solution.variables[0] = my_list
        for i in range(self.number_of_variables()):
            new_solution.variables[i] = i

        return new_solution

    def name(self):
        return "quxinranProblem"
