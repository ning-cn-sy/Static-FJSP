import math

from jmetal.core.problem import PermutationProblem
from jmetal.core.solution import PermutationSolution, S


class VRPProblem(PermutationProblem):
    h = 0.8
    p = 1
    s = 4
    vx = 2.5
    vy = 2.5
    vz = 1

    def __init__(self, Cargolist=[]):
        """:param number_of_variables: Number of decision variables of the problem."""
        super(VRPProblem, self).__init__()
        # 定义obj数量，现在只有一个,另一个假设
        self.obj_directions = [self.MINIMIZE, self.MINIMIZE]
        # self.obj_directions = [self.MINIMIZE]
        # self.obj_labels = ["路径长度", "电量"]
        # self.lower_bound = number_of_variables * [0.0]
        # self.upper_bound = number_of_variables * [1.0]
        self.cargolist = Cargolist

    def number_of_objectives(self) -> int:
        return len(self.obj_directions)

    def number_of_constraints(self) -> int:
        return 0

    def number_of_variables(self) -> int:
        return len(self.cargolist)

    def evaluate(self, solution: PermutationSolution) -> PermutationSolution:
        # shunxu = solution.variables[0]
        shunxu = [yuansu for yuansu in solution.variables]

        # 定义堆垛机容量
        maxLoad = 50

        # # 存储不同子路径的路径数组
        # subPath = []
        # subPathLength = [0]
        # cargo_dict = {cargo['id']: cargo for cargo in self.cargolist}
        # for i in range(0, len(shunxu)):
        #     if cargo_dict[shunxu[i]]:
        #         # 往里放
        #         subPathLength.append(shunxu)

        current_load = 0
        orgin_location = "起点"
        current_location = 0
        pathes = []
        subPath = [orgin_location]
        i = 0
        for cargo_index in shunxu:
            cargo = self.cargolist[cargo_index]  # 根据顺序编码获取货物信息
            # 超过最大承重，返回原点重新出发
            if current_load + cargo.weight > maxLoad:
                subPath.append(orgin_location)
                pathes.append(subPath)
                subPath = [orgin_location]
                current_load = 0
            # 没超过，那需要放到堆垛机上
            current_load += cargo.weight
            subPath.append(cargo_index)

            if i == len(shunxu) - 1:
                subPath.append(orgin_location)
                pathes.append(subPath)
            i += 1

        total_distance = 0
        total_time = 0
        total_punishTime = 0
        for path in pathes:
            total_distance += self.calSubPath(path)
            # total_time += self.calSubPathTime(path)
            total_punishTime += self.calWindowTime(path)

        solution.objectives[0] = total_distance
        solution.objectives[1] = total_punishTime

        return solution

    def calSubPath(self, path):
        length = 0
        for i in range(1, len(path)-2):
            id = path[i]
            point1 = self.id2allocatedBin(id - 1)
            point2 = self.id2allocatedBin(id)
            length += self.calculate_distance(point2, point1)
        pathBeginEnd = self.id2allocatedBin("起点")
        begin = self.id2allocatedBin(path[1])
        end = self.id2allocatedBin(path[-2])
        length += self.calculate_distance(pathBeginEnd, begin)
        length += self.calculate_distance(pathBeginEnd, end)
        return length

    def calSubPathTime(self, path):
        time = 0
        for i in range(1, len(path)-2):
            id = path[i]
            point1 = self.id2allocatedBin(id - 1)
            point2 = self.id2allocatedBin(id)
            time += self.calculate_time(point2, point1)
        pathBeginEnd = self.id2allocatedBin("起点")
        begin = self.id2allocatedBin(path[1])
        end = self.id2allocatedBin(path[-2])
        time += self.calculate_time(pathBeginEnd, begin)
        time += self.calculate_time(pathBeginEnd, end)
        return time

    def calWindowTime(self, path):
        punishTime = 0
        for i in range(1, len(path)):
            id = path[i]
            requiredTime = self.id2timeWindow(id)
            realTime = self.calSubPathTime(path)
            if realTime > requiredTime[1]:
                punishTime += (realTime - requiredTime[1])
            elif realTime < requiredTime[0]:
                punishTime += (requiredTime[0] - realTime)
            else:
                punishTime += 0
        return punishTime

    def id2allocatedBin(self, point):
        return (0, 0, 0) if point == "起点" else self.cargolist[point].allocatedBin

    def id2timeWindow(self, point):
        return [0, 10000] if point == "起点" else self.cargolist[point].timeWindow

    def calculate_distance(self, position1, position2):
        # TODO 再看一下
        x1, y1, z1 = position1
        x2, y2, z2 = position2
        if x1 == x2:
            distance = abs(y2 - y1) * self.p + abs(z2 - z1) * self.h
        else:
            distance = abs(x2 - x1) * self.s + (y2 + y1) * self.p + (z2 + z1) * self.h
        return distance

    def calculate_time(self, position1, position2):
        x1, y1, z1 = position1
        x2, y2, z2 = position2
        if x1 == x2:
            time = abs(y2 - y1) * self.p /self.vy + abs(z2 - z1) * self.h / self.vz
        else:
            time = abs(x2 - x1) * self.s / self.vx + (y2 + y1) * self.p /self.vy + (z2 + z1) * self.h / self.vz
        return time

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
            # new_solution.variables[i] = i
            new_solution.variables[i] = self.number_of_variables() - i - 1

        return new_solution

    def name(self):
        return "quxinranProblem"
