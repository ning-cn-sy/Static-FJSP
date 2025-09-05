# -*- coding: utf-8 -*-
# @Time    : 2024/6/5 15:58
# @Author  : XXX
# @Site    :
# @File    : test_main.py
# @Software: PyCharm
# @Comment :
import csv
import re

from ExactAlgorithm.Config.Milp import milp_variable, milp_constraint
from ExactAlgorithm.Solver.CPLEX.Cplex_Solver import cplex_solver
from ExactAlgorithm.Util.name_util_old import b_name, x_name, Y_name, constraint_name
from ExactAlgorithm.Util.pub_data import W
from ExactAlgorithm.Util.pub_func import split_every_element
from MultiObjectiveOptimization.FJSP.Config.Job import Job
from MultiObjectiveOptimization.FJSP.Config.Machine import Machine
from MultiObjectiveOptimization.FJSP.Config.Operation import Operation
from MultiObjectiveOptimization.FJSP.Util.Draw_gantt import plot_gantt_chart
from MultiObjectiveOptimization.FJSP.Util.Read_By_FJS import readDataByFJS


def find_op(job_list, parse_variable_num):
    for job in job_list:
        for op in job.ops:
            if op.op_id == parse_variable_num[2] and op.job_id == parse_variable_num[1]:
                return op


# def spilt_variable_name(result):
#     return list(result[0].replace("(", "").replace(")", "").replace(",", "").replace(" ", ""))

def spilt_variable_name(result):  # 修正函数名拼写错误（spilt -> split）
    # 提取括号中的内容，例如从'B(10, 2)'中提取'10, 2'
    content = result[0].split('(')[1].split(')')[0]
    # 按逗号分割并去除空格，得到['10', '2']
    parts = [p.strip() for p in content.split(',')]
    # 返回 [前缀, job_id, op_id]
    return [result[0][0]] + parts


def if_processed_(op: Operation, machine):
    for key in op.available_machines:
        if key[0] == machine:
            return key[1]
    return 0.0


def tuple_first_intersection(list_a, list_b):
    # 提取第一个元素并转为集合
    set_a = {t[0] for t in list_a}
    set_b = {t[0] for t in list_b}
    # 求交集
    common = set_a & set_b
    # 按 list_a 的顺序去重输出
    result = []
    seen = set()
    for tpl in list_a:
        num = tpl[0]
        if num in common and num not in seen:
            result.append(num)
            seen.add(num)
    return result


def writecsv(file_name, data):
    """将数据写入CSV文件"""
    with open(file_name, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        for row in data:
            csv_writer.writerow(row)


# job_list, machine_list, auxiliary_modul e_list = generate_data()


job_list, machine_list = readDataByFJS(
    "D:\PhD\Research\PythonResearch\pythonProject\MultiObjectiveOptimization\FJSP\Example\Mk01.fjs")
for machine in machine_list:
    machine.id = machine.id + 1
#
# job_list[0].release_time = 295
# job_list[1].release_time = 90
# job_list[2].release_time = 342
# job_list[3].release_time = 63
# job_list[4].release_time = 132

# job_list, machine_list = [], [Machine(1), Machine(2), Machine(3)]
#
# # 准备装配job1：
# op1 = Operation(1, 1, [(1, 119), (2, 95), (3, 104)])
# op1.realease_time = 634
# op2 = Operation(1, 2, [(1, 110), (2, 141), (3, 147)])
# op2.realease_time = 634
# ops1 = [op1, op2]
# job1 = Job(1, ops1, 0)

# # 准备装配job2：
# op21 = Operation(2, 1, [(1, 135), (2, 156), (3, 159)])
# op21.realease_time = 698
# ops2 = [op21]
# job2 = Job(2, ops2, 0)
#
# job_list.append(job1)
# job_list.append(job2)


# 准备决策变量   列表
decision_variables = [[], [], []]
for job in job_list:
    for op in job.ops:
        decision_variables[0].append(milp_variable(b_name(job.id, op.op_id), type="C"))
        for machine in machine_list:
            decision_variables[1].append(milp_variable(x_name(job.id, op.op_id, machine.id), 1, 0, type="I"))
        for _job in job_list:
            for _op in _job.ops:
                if _op != op:
                    decision_variables[2].append(
                        milp_variable(Y_name(job.id, op.op_id, _job.id, _op.op_id), 1, 0, type="I"))

decision_variables.append([milp_variable("C_max", type="C")])
# 准备目标
# obj目标的系数
# obj = []
# for index, decision_variable in enumerate(decision_variables):
#     for _index, variable in enumerate(decision_variable):
#         if index == 0:
#             obj.append(1.0)
#         else:
#             obj.append(0.0)


obj = []
# 准备c——max
for index, decision_variable in enumerate(decision_variables):
    for _index, variable in enumerate(decision_variable):
        if index == len(decision_variables) - 1:
            obj.append(1.0)
        else:
            obj.append(0.0)

constraint1 = []
constraint2 = []
constraint3 = []
constraint4 = []
constraint5 = []
constraint6 = []
constraint7 = []
constraint8 = []
constraint9 = []
constraint10 = []
constraint11 = []
constraint12 = []
constraint13 = []
for index, job in enumerate(job_list):
    job_id = job.id
    op_len = len(job.ops)
    # 准备约束1和2
    # G 大于号
    constraint1.append(
        milp_constraint(constraint_name(1, job_id), ['C_max'] + [b_name(job_id, op_len)] +
                        [x_name(job_id, op_len, machine[0]) for machine in job.ops[-1].available_machines],
                        [1.0, -1.0] + [-if_processed_(job.ops[-1], machine[0]) for machine in
                                       job.ops[-1].available_machines],
                        0, "G"))
    for op in job.ops:
        constraint2.append(
            milp_constraint(constraint_name(2, job_id, op.op_id),
                            [x_name(job.id, op.op_id, machine[0]) for machine in op.available_machines],
                            [1.0 for machine in op.available_machines],
                            1.0, "E"))
        constraint8.append(
            milp_constraint(
                constraint_name(8, job_id, op.op_id),
                [b_name(job.id, op.op_id)], [1.0], op.realease_time, "G")
        )
        # 准备约束3
        if op.op_id == 1:
            constraint3.append(milp_constraint(constraint_name(3, job_id, 1),
                                               [b_name(job.id, op.op_id)], [1.0], job.release_time, "G"))
        constraint4.append(milp_constraint(constraint_name(4, job_id, op.op_id),
                                           [b_name(job.id, op.op_id)], [1.0], 0, "G"))
        if op.op_id < len(job.ops):
            constraint5.append(
                milp_constraint(name=constraint_name(5, job_id, op.op_id),
                                variables_name=[b_name(job_id, op.op_id + 1)] + [b_name(job_id, op.op_id)] +
                                               [x_name(job_id, op.op_id, machine[0]) for machine in
                                                op.available_machines],
                                weights=[1.0, -1.0] + [-if_processed_(op, machine[0]) for machine in
                                                       op.available_machines], rhs=0, sense="G"))
        for index1, _job in enumerate(job_list):
            for _op in _job.ops:
                if index < index1:
                    machine_list1 = tuple_first_intersection(op.available_machines, _op.available_machines)
                    for machine in machine_list1:
                        constraint6.append(
                            milp_constraint(name=constraint_name(6, job_id, op.op_id, _job.id, _op.op_id, machine),
                                            variables_name=[b_name(_job.id, _op.op_id)] + [
                                                Y_name(job_id, op.op_id, _job.id, _op.op_id)] + [
                                                               x_name(job_id, op.op_id, machine)] + [
                                                               x_name(_job.id, _op.op_id, machine)
                                                           ] +
                                                           [b_name(job.id, op.op_id)],
                                            weights=[1.0] + [-W] + [-W] + [-W] + [-1.0],
                                            rhs=if_processed_(op, machine) -
                                                3.0 * W, sense="G"))
                        constraint7.append(
                            milp_constraint(name=constraint_name(7, job_id, op.op_id, _job.id, _op.op_id, machine),
                                            variables_name=[b_name(job.id, op.op_id)] + [
                                                Y_name(job_id, op.op_id, _job.id, _op.op_id)] + [
                                                               x_name(job_id, op.op_id, machine)] + [
                                                               x_name(_job.id, _op.op_id, machine)] +
                                                           [b_name(_job.id, _op.op_id)],
                                            weights=[1.0] + [W] + [-W] + [-W] + [-1.0],
                                            rhs=if_processed_(_op, machine) -
                                                2.0 * W, sense="G"))

variables = split_every_element(decision_variables)
constraints = split_every_element(
    [constraint1, constraint2, constraint3, constraint4, constraint5, constraint6, constraint7, constraint8])

solver = cplex_solver(variables, constraints, obj, "MIN")
# 开始计算

results = solver.run()
print(results)
for result in results:
    result_name = spilt_variable_name(result)
    style = result_name[0]
    job_id = int(result_name[1])
    op_id = int(result_name[2])
    machine_id = int(result_name[3]) if style == 'x' else -1
    op = job_list[job_id - 1].ops[op_id - 1]
    decision_making = result[1]
    if style == 'B':
        op.start_time = int(round(decision_making))
    elif style == 'x':
        if decision_making > 0.5:
            op.to_machine = machine_id
            op.assigned_end_time_by_start()
    else:
        break

for job in job_list:
    op = job.ops[-1]
    print(str(job.id) + "_" + str(op.op_id) + "   " + str(op.end_time))

plot_gantt_chart(job_list, machine_list)
