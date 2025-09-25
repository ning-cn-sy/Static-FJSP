# -*- coding: utf-8 -*-
# @Time    : 2024/6/5 14:42
# @Author  : 宁诗铎
# @Site    : 
# @File    : FJSP_MR_Problem.py
# @Software: PyCharm 
# @Comment : flexible job shop scheduling problem with machine reconfigurations (FJSP-MR)
import random
from abc import ABC
from typing import Dict

from jmetal.core.problem import IntegerProblem
from jmetal.core.solution import CompositeSolution, PermutationSolution, IntegerSolution

from MultiObjectiveOptimization.FJSP_MR.Config.AuxiliaryModules import AuxiliaryModules
from MultiObjectiveOptimization.FJSP_MR.Config.Job import Job
from MultiObjectiveOptimization.FJSP_MR.Config.Machine import Machine
from MultiObjectiveOptimization.FJSP_MR.Config.Operation import Operation
# from FJSP_MR.Config.Task import Task
from MultiObjectiveOptimization.FJSP_MR.Util.DrawUtil import draw_gantt_chart
# 改种子
# random.seed(6)

class FJSPMR_Problem(IntegerProblem, ABC):
    def __init__(self, job_list: [Job], machine_list, auxiliary_module_list):
        super(FJSPMR_Problem, self).__init__()
        # 目标的信息（方向、名称）
        self.obj_directions = [self.MINIMIZE]
        self.obj_labels = ["总加权延迟"]
        self.job_list = job_list

        self.job_complete_time = []
        self.machine_list = machine_list
        self.auxiliary_module_list = auxiliary_module_list
        # 2.机器/模式 序列上下限
        self.machine_mode_lower_bound = [0 for job in job_list for op in job.op_list]
        self.machine_mode_upper_bound = [(len(op.available_machines_am) - 1) for job in job_list for op in job.op_list]
        self.op_list = [op for job in job_list for op in job.op_list]

    def appears_time(self, operation_count, i):
        # 记录每个job出现的次数

        # 数当前i的次数
        count = operation_count.get(i, 0)

        # 更新 i的次数
        operation_count[i] = count + 1
        return count

    def generate_code(self, sequence, allocation):
        # 不会先给一个op_list？  数字i不就是第几个吗
        code1 = [self.op_list[i].job_id for i in sequence]
        code2 = []
        for index, i in enumerate(allocation):
            # 想到写列表了，不会debug看看里头
            available_machines = list(self.op_list[index].available_machines_am.items())
            machine = available_machines[i][0][0]
            auxiliary = available_machines[i][0][1]
            # 索引从零开始，找机器加个1,机器 是 123   而 am 现在是0， 1 ，2
            machine_index = self.machine_list.index(machine) + 1
            auxiliary_index = self.auxiliary_module_list.index(auxiliary)
            code2.append((machine_index, auxiliary_index))

        return code1, code2

    def create_solution(self):
        # 因为是多序列问题，构建问题list
        solution_list = []
        # 工序顺序编码，直接用排序编码就解决掉
        solution1 = PermutationSolution(
            number_of_variables=self.number_of_variables(), number_of_objectives=self.number_of_objectives(),
            number_of_constraints=self.number_of_variables()
        )
        # 生成初始编码
        solution1.variables = list(range(self.number_of_variables()))
        random.shuffle(solution1.variables)
        # 机器和模式编码，每个机器还有不同的模型
        solution2 = IntegerSolution(
            lower_bound=self.machine_mode_lower_bound,
            upper_bound=self.machine_mode_upper_bound,
            number_of_objectives=self.number_of_objectives(),
            number_of_constraints=self.number_of_variables()
        )
        # 生成初始编码
        solution2.variables = [random.randint(lb, ub) for lb, ub in
                               zip(solution2.lower_bound, solution2.upper_bound)]

        solution_list.append(solution1)
        solution_list.append(solution2)

        new_solution = CompositeSolution(solutions=solution_list)
        return new_solution

    def decode(self, solution):
        sequence = solution.variables[0].variables
        allocation = solution.variables[1].variables
        # step1：根据sequence找到工序
        OS, CS = self.generate_code(sequence, allocation)
        # temp
        # OS = [1, 2, 4, 1, 6, 7, 10, 2, 4, 5, 8, 8, 9, 2, 3, 8, 5, 7, 7, 7, 4, 4, 9, 4, 8, 5, 10, 3, 6, 3, 9, 9, 5, 10, 1, 1, 3, 6, 1, 6, 7, 10, 6, 5, 2, 6, 1, 10, 9, 8, 5, 3, 2, 9, 10]
        # CS = [(3, 0), (5, 0), (3, 2), (6, 3), (3, 2), (6, 1), (2, 1), (3, 0), (1, 0), (4, 0), (6, 1), (2, 0), (3, 0), (2, 0), (2, 0), (5, 1), (2, 1), (2, 1), (3, 0), (2, 2), (6, 0), (5, 0), (6, 0), (2, 0), (3, 1), (4, 0), (6, 1), (3, 0), (1, 2), (2, 0), (2, 1), (1, 2), (4, 0), (6, 2), (4, 0), (3, 0), (2, 0), (3, 1), (6, 3), (3, 2), (1, 0), (2, 0), (2, 0), (6, 0), (1, 0), (6, 3), (1, 2), (2, 0), (2, 0), (6, 0), (3, 3), (2, 0), (6, 3), (2, 0), (1, 0)]

        # temp
        # print(OS, CS)
        # 当前的工序序列
        machine_op_list: Dict[Machine, list] = {}
        am_op_list: Dict[AuxiliaryModules, list] = {}
        # 记录每个job出现的次数
        operation_count = {}
        tasks = []
        # start_time = []
        # during = []
        # complete_time = []
        # machine = []
        # am = []
        # 遍历OS p就是当前的位置
        for p in range(len(OS)):
            #  i那个位置的数字
            i = OS[p] - 1
            j = self.appears_time(operation_count, i)
            Oij = self.job_list[i].op_list[j]
            # 是否为工件的第一道工序
            if j == 0:
                Cjp = self.job_list[i].release_time
            else:
                Cjp = self.job_list[i].op_list[j - 1].complete_time
            # 检查Oij在CS中的位置
            index = self.op_list.index(Oij)
            # 找到对应位置的数字， 在机器am list里找对应的
            Mk = self.machine_list[CS[index][0] - 1]
            Aq = self.auxiliary_module_list[CS[index][1]]
            # 找Mk上最后一个工序，以及Aq上最后一个工序  没有这个mk就填进去[]
            if Mk.id not in machine_op_list:
                machine_op_list.setdefault(Mk.id, [])
            if Aq.id not in am_op_list:
                am_op_list.setdefault(Aq.id, [])

            machine_op_list[Mk.id].append(Oij)
            am_op_list[Aq.id].append(Oij)
            # null operation  没有的工序
            op_null = Operation(-1, -1, [])
            # 判断机器上有没有上道工序
            # machine_op_list长度为1 说明刚填进去 没有前序工序
            # 否则 上一道工序为当前的倒数第二道 长度 - 2
            MPOij = op_null if len(machine_op_list[Mk.id]) == 1 else machine_op_list[Mk.id][
                len(machine_op_list[Mk.id]) - 2]
            APOij = op_null if len(am_op_list[Aq.id]) == 1 else am_op_list[Aq.id][
                len(am_op_list[Aq.id]) - 2]
            sij = -1.3
            # 如果都不是空
            if MPOij == APOij and MPOij is not op_null and APOij is not op_null:
                sij = max(Cjp, MPOij.complete_time)
            else:
                # Aq0 是机器上正在用的am 把他拆下来
                # 通过工序的索引 找到cs序列对应的<,> 两个数字  然后在auxiliary_module_list里找
                Aq0 = self.auxiliary_module_list[0] if MPOij.id == -1 else self.auxiliary_module_list[
                    CS[self.op_list.index(MPOij)][1]]
                # machine准备好  上工序完成 拆装
                machine_ready_time = MPOij.complete_time + self.auxiliary_module_list[
                    Aq0.id].disassemble_time[Mk.name] + Aq.assemble_time[Mk.name]
                # am上一工序完成 拆装  有可能是 am0 或 上一工序没有
                am_ready_time = (0.0 if Aq.id == 0 else APOij.complete_time) + (
                    0.0 if APOij.id == -1 else Aq.disassemble_time[APOij.machine.name]) + Aq.assemble_time[Mk.name]
                sij = max(Cjp, machine_ready_time, am_ready_time)

            #  print("当前的工件", Oij.job_id, Oij.id, "机器、模块", Mk.id, Aq.id, MPOij, APOij)

            pij = Oij.available_machines_am[(Mk.id, Aq.id)]
            Oij.duration = pij
            Oij.machine = Mk
            Oij.am = Aq
            tasks.append(Oij)
            Oij.start_time = sij
            Oij.complete_time = Oij.start_time + pij
            #  print(Oij.start_time, pij, Oij.complete_time)

            # 首先找每个工件的完成时间 job_complete_time

            if j == len(self.job_list[i].op_list) - 1:
                self.job_list[i].job_complete_time = Oij.complete_time

            # tasks.append(Oij)
            # start_time.append(Oij.start_time)
            # during.append(pij)
            # complete_time.append(Oij.complete_time)
            # machine.append(Mk)
            # am.append(Aq)

        return tasks

    def evaluate(self, solution: CompositeSolution) -> CompositeSolution:
        self.decode(solution)
        TWT = 0
        for i in range(len(self.job_list)):
            t = max((self.job_list[i].job_complete_time - self.job_list[i].delivery_time), 0)
            TWT = TWT + t * self.job_list[i].weight
        # print(TWT)
        solution.objectives[0] = TWT
        return solution

    def name(self) -> str:
        return "可重构车间调度"

    def number_of_variables(self) -> int:
        return sum(len(job.op_list) for job in self.job_list)

    def number_of_objectives(self) -> int:
        return len(self.obj_directions)

    def number_of_constraints(self) -> int:
        return 0
