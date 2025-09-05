# -*- coding: utf-8 -*-
# @Time    : 2025/1/6 14:47
# @Author  : 
# @Site    : 
# @File    : temp.py
# @Software: PyCharm 
# @Comment :
# from MultiObjectiveOptimization.FJSP.Algorithm.Decode import Decode
# from MultiObjectiveOptimization.FJSP.Util.Draw_gantt import plot_gantt_chart
# from MultiObjectiveOptimization.FJSP.Util.GetNodeEdges import get_nodes_edges
# from MultiObjectiveOptimization.FJSP.Util.Draw_distinct_graph import graph
from MultiObjectiveOptimization.FJSP.Util.Read_By_FJS import readDataByFJS

# jobs, machines = readDataByFJS("D:\pythonProject\MultiObjectiveOptimization\FJSP\Example\MFJS01.fjs")
# temp_sequence = [7, 5, 11, 6, 14, 8, 13, 2, 12, 0, 9, 4, 10, 3, 1]
#
# machine_selection = [0, 0, 1, 1, 0, 1, 1, 1, 2, 1, 0, 1, 2, 2, 1]
# decode = Decode(jobs, machines)
# # 运行解码器，计算调度方案
# decode.run_semi_active_schedule(temp_sequence, machine_selection)
#
# plot_gantt_chart(decode.jobs, decode.machines)
# nodes, edges = get_nodes_edges(decode.jobs)
# xiqvgraph1 = graph(nodes=nodes, edges=edges)
# xiqvgraph1.draw_network()
# print(xiqvgraph1.longest_path())


# def split_variable_name(result):  # 修正函数名拼写错误（spilt -> split）
#     # 提取括号中的内容，例如从'B(10, 2)'中提取'10, 2'
#     content = result[0].split('(')[1].split(')')[0]
#     # 按逗号分割并去除空格，得到['10', '2']
#     parts = [p.strip() for p in content.split(',')]
#     # 返回 [前缀, job_id, op_id]
#     return [result[0][0]] + parts
#
# job_list, machine_list = readDataByFJS(
#     "D:\PhD\Research\PythonResearch\pythonProject\MultiObjectiveOptimization\FJSP\Example\Mk01.fjs")
#
# results = [('B(1, 1)', 19.0),
#            ('B(10, 1)', 19.0)]
#
# for result in results:
#     result_name = split_variable_name(result)
#     style = result_name[0]
#     job_id = int(result_name[1])
#     op_id = int(result_name[2])




from jmetal.algorithm.multiobjective.nsgaii import NSGAII
from jmetal.problem import ZDT1
from jmetal.operator import SBXCrossover, PolynomialMutation
from jmetal.util.termination_criterion import StoppingByEvaluations
# from jmetal.util.solution_list_output import SolutionListOutput

def main():
    # 定义问题（ZDT1是一个经典的多目标优化测试问题）
    problem = ZDT1()

    # 定义算法参数
    max_evaluations = 25000  # 最大评估次数
    population_size = 100    # 种群大小

    # 定义交叉和变异算子
    crossover = SBXCrossover(probability=0.9, distribution_index=20)
    mutation = PolynomialMutation(probability=1.0 / problem.number_of_variables, distribution_index=20)

    # 实例化NSGA-II算法
    algorithm = NSGAII(
        problem=problem,
        population_size=population_size,
        offspring_population_size=population_size,
        crossover=crossover,
        mutation=mutation,
        termination_criterion=StoppingByEvaluations(max=max_evaluations)
    )

    # 运行算法
    algorithm.run()

    # 获取并输出结果
    front = algorithm.get_result()
    print(f"算法运行完成，找到 {len(front)} 个非支配解")

    # # 将结果保存到文件
    # SolutionListOutput(front).print()
    # SolutionListOutput(front).write_to_file("ZDT1_results.csv")

if __name__ == "__main__":
    main()