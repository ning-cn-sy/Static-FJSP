# -*- coding: utf-8 -*-
# @Time    : 2025/1/5 14:55
# @Author  : 宁诗铎
# @Site    : 
# @File    : FJSP_Problem.py
# @Software: PyCharm 
# @Comment : 柔性作业车间调度问题
import random

from jmetal.core.problem import PermutationProblem
from jmetal.core.solution import PermutationSolution, S, IntegerSolution, CompositeSolution
from werkzeug.routing import RuleFactory

from MultiObjectiveOptimization.FJSP.Algorithm.Decode import Decode
from MultiObjectiveOptimization.FJSP.Algorithm.Rule.MachineRules import SPT_MachineRule
from MultiObjectiveOptimization.FJSP.Algorithm.Rule.SequencingRules import SPT_SequencingRule


class FJSP_Problem_1(PermutationProblem):

    def __init__(self, jobs, machines):

        super(FJSP_Problem_1, self).__init__()
        self.obj_directions = [self.MINIMIZE]  # 目标方向，当前为最小化
        self.obj_labels = ["makespan"]  # 目标标签，当前优化目标为完工时间
        self.jobs = jobs  # 工件列表
        self.machines = machines  # 机器列表

    def number_of_objectives(self) -> int:
        """
        获取目标函数的数量。

        Returns:
            int: 目标函数的数量。
        """
        return len(self.obj_directions)

    def number_of_constraints(self) -> int:
        """
        获取约束条件的数量。

        Returns:
            int: 约束条件的数量，当前为 0。
        """
        return 0

    def number_of_variables(self) -> int:
        """
        获取决策变量的数量。

        Returns:
            int: 决策变量的数量，等于所有工件的操作数总和。
        """
        return sum(job.get_num_ops() for job in self.jobs)

    def evaluate(self, solution: PermutationSolution) -> PermutationSolution:
        """
        评估给定解的质量，根据作业顺序和机器分配计算调度结果。

        Args:
            solution (PermutationSolution): 包含作业顺序和机器分配信息的解。

        Returns:
            PermutationSolution: 更新目标值后的解。
        """
        # ------------✌️准备数据✌️------------ #

        # 提取当前解中的作业顺序
        temp_sequence = solution.variables[0].variables[:]

        # 提取机器分配方案
        machine_selection = solution.variables[1].variables

        # print(temp_sequence)
        # print(machine_selection)

        # temp_sequence = [20, 37, 64, 29, 41, 27, 5, 50, 17, 73, 1, 24, 47, 55, 33, 30, 12, 54, 46, 16, 35, 23, 58, 66,
        #                  4, 36, 38, 7, 67, 3, 31, 28, 13, 34, 72, 62, 68, 45, 53, 69, 8, 70, 74, 0, 59, 52, 2, 10, 25,
        #                  32, 63, 60, 19, 9, 21, 56, 61, 51, 57, 48, 6, 44, 18, 15, 49, 11, 26, 75, 14, 71, 39, 40, 22,
        #                  42, 43, 65]
        # machine_selection = [2, 1, 1, 2, 2, 0, 1, 1, 0, 0, 1, 0, 0, 2, 3, 0, 1, 2, 0, 1, 0, 2, 1, 0, 1, 2, 2, 0, 0, 3,
        #                      2, 0, 3, 2, 1, 2, 1, 3, 2, 1, 0, 2, 2, 1, 0, 3, 2, 0, 2, 1, 0, 1, 2, 1, 3, 2, 2, 0, 2, 3,
        #                      0, 1, 1, 2, 0, 0, 1, 2, 3, 0, 2, 3, 2, 0, 0, 1]

        # ------------✌️开始解码✌️------------ #
        # 初始化解码器1
        decode = Decode(self.jobs, self.machines)
        # 运行解码器，计算调度方案
        decode.run_semi_active_schedule(temp_sequence, machine_selection)
        # fitness = decode.calculate_fitness()

        # # 初始化解码器2
        # decode1 = Decode(self.jobs, self.machines)
        # # 运行解码器，计算调度方案
        # decode1.run_active_schedule(temp_sequence, machine_selection)
        # plot_gantt_chart(decode.jobs, decode.machines, "semi_active")
        # plot_points_and_connections_by_jobs(decode.jobs)
        # plot_gantt_chart(decode1.jobs, decode1.machines, "active")
        # plot_points_and_connections_by_jobs(decode1.jobs)
        # 计算目标值
        # 当前目标值设置为 0，实际应用中需根据目标函数重新计算

        solution.objectives[0] = max(op.end_time for job in decode.jobs for op in job.ops)

        return solution

    def create_solution(self) -> S:
        """
        创建一个基于确定性规则组合的初始解，每次调用自动切换规则。
        """
        # --- 保留原始初始化逻辑 ---
        jobs_solution = PermutationSolution(
            number_of_variables=self.number_of_variables(),
            number_of_objectives=self.number_of_objectives()
        )
        # 生成初始编码
        jobs_solution.variables = list(range(self.number_of_variables()))
        random.shuffle(jobs_solution.variables)
        lower_bound, upper_bound = [], []
        i = 0
        for job in self.jobs:
            for op in job.ops:
                # jobs_solution.variables[i] = i
                lower_bound.append(0)
                upper_bound.append(len(op.available_machines) - 1)
                i += 1
        #
        # --- 新增逻辑1：定义规则组合池（完全在方法内部）---
        # 规则组合格式: (顺序规则实例, 机器规则实例)
        # rule_combinations = [
        #     (SPT_SequencingRule(), SPT_MachineRule())
        #     # 可扩展混合规则，例如:
        #     # (SPT_SequencingRule(), EDD_MachineRule()),
        # ]

        # # --- 新增逻辑2：通过闭包持久化规则索引 ---
        # if not hasattr(self, "_rule_index"):
        #     self._rule_index = 0  # 初始化索引
        # else:
        #     self._rule_index = (self._rule_index + 1) % len(rule_combinations)  # 循环递增
        #
        # # 获取当前规则组合
        # sequencing_rule, machine_rule = rule_combinations[self._rule_index]
        #
        # # --- 修改点1：应用顺序规则 ---
        # jobs_solution.variables = sequencing_rule.execute(self.jobs)  # 替换 random.shuffle

        # --- 保留机器解初始化 ---
        machines_solution = IntegerSolution(
            lower_bound,
            upper_bound,
            number_of_objectives=self.number_of_objectives()
        )
        machines_solution.variables = [random.randint(lb, ub) for lb, ub in
                                       zip(machines_solution.lower_bound, machines_solution.upper_bound)]

        # # --- 修改点2：应用机器规则 ---
        # machine_selection = []
        # for job in self.jobs:
        #     for op in job.ops:
        #         available_machines = op.available_machines
        #         selected_idx = machine_rule.execute(op, available_machines)
        #         machine_selection.append(selected_idx)
        # machines_solution.variables = machine_selection  # 替换原随机生成

        # --- 保留组合解逻辑 ---
        new_solution = CompositeSolution([jobs_solution, machines_solution])
        return new_solution

    def name(self):
        """
        获取问题名称。

        Returns:
            str: 问题的名称，描述为柔性作业车间调度问题（带装配操作）。
        """
        return "flexible job-shop scheduling problem"
