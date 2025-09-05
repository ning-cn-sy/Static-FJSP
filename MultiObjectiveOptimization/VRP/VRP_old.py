import time

import numpy as np
from jmetal.algorithm.multiobjective import NSGAII
from jmetal.logger import get_logger
from jmetal.operator import PMXCrossover
from jmetal.util.termination_criterion import StoppingByEvaluations
from matplotlib import pyplot as plt

from VRP.config.CargoVRP import Cargo
from VRP.Algorithm.VRPProblem import VRPProblem
from testMutation import testMutation

from draw import draw
# 日志,不用管
logger = get_logger(__name__)

# TODO 准备cargolist
cargo01 = Cargo("cargo01", 17, [1, 1, 2])
cargo02 = Cargo("cargo02", 20, [2, 1, 1])
cargo03 = Cargo("cargo03", 30, [3, 3, 2])
cargo04 = Cargo("cargo04", 22, [2, 1, 4])
cargo05 = Cargo("cargo05", 15, [1, 3, 2])
cargolist = [cargo01, cargo02, cargo03, cargo04, cargo05]

# 定义Problem,要传参,传坐标
problem = VRPProblem(Cargolist=cargolist)
# 一些算法参数
population_size = 100
offspring_population_size = 100
crossover_probability = 1.0
crossover_distribution_index = 20
mutation_probability = 1.0 / 2.0
mutation_distribution_index = 20
max_evaluations = 300 * 100
# TODO 算法改成单目标？
algorithm = NSGAII(
    problem=problem,
    population_size=population_size,
    offspring_population_size=offspring_population_size,
    mutation=testMutation(probability=mutation_probability),
    crossover=PMXCrossover(probability=crossover_probability),
    termination_criterion=StoppingByEvaluations(max_evaluations=max_evaluations)
)

# algorithm_old.run()  #原调用方式

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
objective1s = []
processData = []
i = 0
while not algorithm.stopping_condition_is_met():
    objective1s.append(algorithm.solutions[0].objectives[0])
    processData.append([i for i in algorithm.solutions[0].variables])
    print("第%d次", {i})
    print(processData[len(processData) - 1])
    print(objective1s[len(objective1s) - 1])
    algorithm.step()
    i = i + 1
    algorithm.update_progress()

logger.debug("Finished!")

algorithm.total_computing_time = time.time() - algorithm.start_computing_time
solutions = algorithm.get_result()

# from jmetal.lab.visualization import Plot

# plot_front = Plot(title='Pareto front approximation', axis_labels=['x', 'y'])
# plot_front.plot(solutions, label='aaa', filename='路径规划', format='png')

xs = [i for i in range(len(objective1s))]
plt.scatter(xs, objective1s)
plt.show()
data_collection = []

# 画路线图
for processDatum in processData:
    data_point = data
    data_line = []
    data_line_part = np.array([[[0, 0], [0, 0]] for i in range(len(processDatum))])
    for i in range(1, len(processDatum)):
        data_line_part[i - 1] = [[data[processDatum[i]][0], data[processDatum[i]][1]], [data[processDatum[i - 1]][0],
                                                                                        data[processDatum[i - 1]][1]]]
    data_collection.append([data_point, data_line_part])
print()
draw(data, data_collection)
