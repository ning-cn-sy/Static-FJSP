# -*- coding: utf-8 -*-
# @Time    : 2024/12/28 14:04
# @Author  : 宁诗铎
# @Site    : 
# @File    : FJSP_AO_Problem.py
# @Software: PyCharm 
# @Comment : 机加 - 装配 调度问题的函数，用于Jmetalpy


import random

from jmetal.core.problem import PermutationProblem
from jmetal.core.solution import PermutationSolution, S, IntegerSolution, CompositeSolution


from MultiObjectiveOptimization.FJSP_AO.Algrithm.Decode import Decode
from MultiObjectiveOptimization.FJSP_AO.Algrithm.Rule.MachineRules import SPT_MachineRule
from MultiObjectiveOptimization.FJSP_AO.Algrithm.Rule.SequencingRule import SPT_SequencingRule


class FJSP_AO_Problem(PermutationProblem):
    """
    FJSP_AO_Problem 类表示一个带有装配操作的柔性作业车间调度问题（Flexible Job-Shop Scheduling Problem with Assembly Operations）。
    该问题包含作业调度与装配规则，目标是优化调度方案，例如最小化完工时间（makespan）。

    Attributes:
        obj_directions (list): 目标优化方向列表，默认为最小化（MINIMIZE）。
        obj_labels (list): 目标标签列表，描述优化目标，例如 "makespan"。
        jobs (list): 工件列表，每个工件包含一组操作信息。
        machines (list): 机器列表，记录可用机器信息。
        assemble_styles (list): 装配规则列表，描述装配操作的要求。
    """

    def __init__(self, jobs, machines, assemble_styles, need_styles, decoding_flag="active", init_flag=False):
        """
        初始化 FJSP_AO_Problem 类。

        Args:
            jobs (list): 工件列表，每个工件包含一组操作信息。
            machines (list): 机器列表，记录可用机器信息。
            assemble_styles (list): 装配规则列表，描述装配操作的要求。
        """
        super(FJSP_AO_Problem, self).__init__()
        self.obj_directions = [self.MINIMIZE, self.MINIMIZE, self.MINIMIZE]  # 目标方向，当前为最小化
        self.obj_labels = ["make_span", "use_energy", "idle_energy"]  # 目标标签，当前优化目标为完工时间
        self.jobs = jobs  # 工件列表
        self.machines = machines  # 机器列表
        self.assemble_styles = assemble_styles  # 装配规则列表
        self.need_styles = need_styles
        self.decoding_flag = decoding_flag
        self.init_flag = init_flag

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
        assembly_selection = solution.variables[2].variables

        # temp_sequence = [49, 31, 105, 98, 52, 97, 19, 36, 83, 62, 25, 34, 5, 46, 61, 89, 107, 118, 28, 68, 35, 103, 29,
        #                  4, 101, 74, 2,
        #                  64, 59, 82, 70, 96, 65, 18, 51, 38, 43, 50, 57, 12, 30, 84, 95, 119, 40, 56, 94, 63, 27, 113,
        #                  60, 33, 90, 114,
        #                  86, 58, 117, 23, 21, 120, 3, 53, 16, 93, 20, 91, 26, 45, 54, 85, 110, 81, 92, 104, 24, 39, 71,
        #                  0, 99, 55, 111,
        #                  1, 108, 10, 72, 73, 100, 15, 75, 80, 44, 32, 116, 87, 69, 8, 9, 115, 112, 78, 79, 48, 66, 102,
        #                  77, 37, 17, 6,
        #                  13, 47, 67, 109, 42, 22, 11, 88, 14, 41, 7, 76, 106]
        # machine_selection = [5, 1, 0, 0, 0, 0, 2, 2, 2, 1, 0, 0, 2, 2, 2, 1, 0, 1, 2, 0, 0, 2, 3, 0, 4, 0, 0, 0, 1, 3,
        #                      2, 0, 1, 0, 0, 0, 2,
        #                      1, 2, 0, 1, 1, 0, 0, 4, 0, 0, 0, 1, 0, 2, 2, 2, 0, 0, 2, 2, 2, 3, 0, 2, 0, 0, 2, 2, 5, 2,
        #                      0, 2, 1, 0, 0, 2, 0,
        #                      0, 0, 1, 0, 0, 0, 3, 1, 0, 0, 1, 2, 0, 0, 0, 0, 1, 2, 0, 4, 0, 3, 1, 0, 2, 2, 5, 0, 4, 5,
        #                      2, 1, 2, 0, 0, 1, 0,
        #                      0, 1, 0, 2, 0, 5, 4, 3, 0, 0]
        # assembly_selection = [6, 13, 1, 11, 16, 12, 15, 14, 3, 4, 2, 9, 8, 7, 10, 0, 5]

        # ------------✌️开始解码✌️------------ #
        # 初始化解码器1
        decode = Decode(self.jobs, self.machines, self.assemble_styles, self.need_styles)
        if self.decoding_flag == "semi_active":
            # 运行解码器，计算调度方案
            decode.run_semi_active_schedule(temp_sequence, machine_selection, assembly_selection)
        elif self.decoding_flag == "active":
            decode.run_active_schedule(temp_sequence, machine_selection, assembly_selection)

        # 可视化生成的甘特图（用于调试或分析）
        # plot_gantt_chart(decode.jobs, decode.machines, self.decoding_flag)
        # plot_points_and_connections_by_jobs(decode.jobs)
        machine_run_energy = decode.calculate_running_energy_usage()
        machine_idle_energy = decode.calculate_idle_energy_usage()
        job_delay_time = decode.calculate_job_delay_time()
        solution.objectives[0] = decode.calculate_makespan()
        solution.objectives[1] = sum(machine_run_energy) + sum(machine_idle_energy)
        solution.objectives[2] = sum(job_delay_time)

        # plot_points_and_connections_by_jobs(decode.jobs)

        return solution

    def create_solution(self) -> S:
        """
        创建一个随机初始解，包含工件顺序和机器分配。

        Returns:
            CompositeSolution: 包含作业顺序和机器分配的复合解。
        """
        # 初始化用于存储工件顺序的解
        jobs_solution = PermutationSolution(
            number_of_variables=self.number_of_variables(),
            number_of_objectives=self.number_of_objectives()
        )
        assembly_solution = PermutationSolution(
            number_of_variables=len(self.jobs),
            number_of_objectives=self.number_of_objectives()
        )
        # 定义上下界列表，分别存储每个变量的最小值和最大值
        lower_bound, upper_bound = [], []

        # 遍历所有作业及其操作
        j = 0
        i = 0
        for job in self.jobs:
            assembly_solution.variables[i] = i
            for op in job.ops:
                # 设置变量值为当前索引值
                jobs_solution.variables[j] = j

                # 设置每个变量的下界为 0
                lower_bound.append(0)

                # 设置每个变量的上界为可用机器数量 - 1
                upper_bound.append(len(op.available_machines) - 1)

                # 索引值加一
                j += 1
            i += 1

        # 创建用于存储机器分配的解
        machines_solution = IntegerSolution(
            lower_bound,
            upper_bound,
            number_of_objectives=self.number_of_objectives()
        )
        if self.init_flag is True:
            # --- 新增逻辑1：定义规则组合池（完全在方法内部）---
            # 规则组合格式: (顺序规则实例, 机器规则实例)
            rule_combinations = [
                (SPT_SequencingRule(), SPT_MachineRule())
                # 可扩展混合规则，例如:
                # (SPT_SequencingRule(), EDD_MachineRule()),
            ]

            # --- 新增逻辑2：通过闭包持久化规则索引 ---
            if not hasattr(self, "_rule_index"):
                self._rule_index = 0  # 初始化索引
            else:
                self._rule_index = (self._rule_index + 1) % len(rule_combinations)  # 循环递增

            # 获取当前规则组合
            sequencing_rule, machine_rule = rule_combinations[self._rule_index]

            # --- 修改点1：应用顺序规则 ---
            jobs_solution.variables = sequencing_rule.execute(self.jobs)  # 替换 random.shuffle
            machine_selection = []
            for job in self.jobs:
                for op in job.ops:
                    available_machines = op.available_machines
                    selected_idx = machine_rule.execute(op, available_machines)
                    machine_selection.append(selected_idx)
            machines_solution.variables = machine_selection  # 替换原随机生成
        else:
            # 🎈 Start  生成所需要的初始值
            random.shuffle(jobs_solution.variables)
            # 为机器分配解生成随机初始值，确保值在上下界范围内
            machines_solution.variables = [
                random.randint(lb, ub) for lb, ub in zip(machines_solution.lower_bound, machines_solution.upper_bound)
            ]
            random.shuffle(assembly_solution.variables)
            # 🎈 End  生成所需要的初始值

        # 将工件顺序解和机器分配解组合为一个复合解
        new_solution = CompositeSolution([jobs_solution, machines_solution, assembly_solution])

        return new_solution

    def name(self):
        """
        获取问题名称。

        Returns:
            str: 问题的名称，描述为柔性作业车间调度问题（带装配操作）。
        """
        return "flexible job-shop scheduling problem with assembly operations"
