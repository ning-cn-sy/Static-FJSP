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
from ExactAlgorithm.Util.name_util import b_name, x_name, Y_name, constraint_name, A_name, constraint_name_ass, Z_name
from ExactAlgorithm.Util.pub_data import W
from ExactAlgorithm.Util.pub_func import split_every_element
from MultiObjectiveOptimization.FJSP.Config.Operation import Operation
from MultiObjectiveOptimization.FJSP.Util.Draw_gantt import plot_gantt_chart
from MultiObjectiveOptimization.FJSP_AO.Config.Assemble_style import Assemble_style
from MultiObjectiveOptimization.FJSP_AO.Config.Job import Job_style
from MultiObjectiveOptimization.FJSP_AO1.Util.Instance.Instance_read_generator import Instance_read_generator_by_fjs
import io
from contextlib import redirect_stdout


import re
import cplex

problem = cplex.Cplex()
# 设置时间限制为3600秒（1小时）
problem.parameters.timelimit.set(60)
problem.solve()


def split(s):
    # 1. 按左括号分割，分离前缀和参数部分
    parts = s.split("(")  # ["x", "2, 4, 10)"]
    # 2. 处理参数部分：去掉右括号，按逗号分割，并去除空格
    prefix = parts[0]  # "x"
    params_str = parts[1].strip(")")  # "2, 4, 10"
    params = [prefix]
    params_nums = [p.strip() for p in params_str.split(",")]
    for p in params_nums:
        params.append(p)
    # ["2", "4", "10"]
    return params


def find_op(job_list, parse_variable_num):
    for job in job_list:
        for op in job.ops:
            if op.op_id == parse_variable_num[2] and op.job_id == parse_variable_num[1]:
                return op


def spilt_variable_name(result):
    return list(result[0].replace("(", "").replace(")", "").replace(",", "").replace(" ", ""))


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



x = 1
type = "AB"

job_list, machine_list, astyles, gs, filename = Instance_read_generator_by_fjs(
    "D:\pycharmproject\MultiObjectiveOptimization\FJSP_AO\Example\Example_AB\MFJS01.fjs", x, type)
# 准备决策变量   列表
decision_variables = [[], [], [], [], []]

for job in job_list:
    for g, aa in enumerate(gs):
        decision_variables[3].append(milp_variable(A_name(job.id, g + 1), 1, 0, type="I"))
    for op in job.ops:
        decision_variables[0].append(milp_variable(b_name(job.id, op.op_id), type="C"))
        for machine in machine_list:
            decision_variables[1].append(milp_variable(x_name(job.id, op.op_id, machine.id), 1, 0, type="I"))
        for _job in job_list:
            for _op in _job.ops:
                if _op != op:
                    decision_variables[2].append(
                        milp_variable(Y_name(job.id, op.op_id, _job.id, _op.op_id), 1, 0, type="I"))
                if job.id < _job.id:
                    for g, style in enumerate(gs):
                        decision_variables[4].append(
                            milp_variable(
                                Z_name(job.id, op.op_id, _job.id, _op.op_id, g + 1),
                                1,
                                0, type="I"))

decision_variables.append([milp_variable("C_max", type="C")])


def get_assemble_by_jobid(i1, i2):
    ret = []
    job_1 = job_list[i1 - 1]
    job_2 = job_list[i2 - 1]
    style1 = job_1.style
    style2 = job_2.style
    for g, style in enumerate(gs):
        param1 = style[0]
        param2 = style[1]
        if style1 in [param1, param2] and style2 in [param1, param2]:
            ret.append(g + 1)

    return ret


def extract_job_styles(node):
    """递归提取样式树中的所有Job_style值"""
    if isinstance(node, Job_style):
        return [node.value]
    elif isinstance(node, Assemble_style):
        left = extract_job_styles(node.param1)
        right = extract_job_styles(node.param2)
        return left + right
    return []  # 未知类型返回空列表


def if_hebing(s, j, _s, _j, g):
    for astyle in astyles:
        # 提取样式树中所有底层Job_style的值
        styles = extract_job_styles(astyle)

        if s in styles and _s in styles:
            idx1 = styles.index(s)
            idx2 = styles.index(_s)
            # 检查操作是否与样式定义的位置完全匹配
            if j == astyle.ops[idx1] and _j == astyle.ops[idx2]:
                return 1.0
    return 0.0


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
constraint14 = []
constraint15 = []
constraint16 = []
constraint17 = []
constraint18 = []

# 约束8：准备合并约束1，工件得根据类型分配给对应的装配任务
for g, astyle in enumerate(gs):
    for s, style in enumerate(astyle):
        constraint8.append(
            milp_constraint(constraint_name_ass(8, g + 1, style.value),
                            [A_name(job.id, g + 1) for job in job_list if job.style == style],
                            [1.0 for job in job_list if job.style == style],
                            1.0 if style in astyle else 0.0, "E"))

for index, job in enumerate(job_list):
    job_id = job.id
    op_len = len(job.ops)
    # 准备约束1和2
    # G 大于号
    # 约束1：determine the maximum End time of scheduling plan
    constraint1.append(
        milp_constraint(constraint_name(1, job_id), ['C_max'] + [b_name(job_id, op_len)] +
                        [x_name(job_id, op_len, machine[0]) for machine in job.ops[-1].available_machines],
                        [1.0, -1.0] + [-if_processed_(job.ops[-1], machine[0]) for machine in
                                       job.ops[-1].available_machines],
                        0, "G"))

    # 约束9：工件只能分配给一个装配任务
    constraint9.append(
        milp_constraint(constraint_name(9, job.id),
                        [A_name(job.id, g + 1) for g, astyle in enumerate(gs)],
                        [1.0 for g, astyle in enumerate(gs)],
                        1.0, "E"))

    for op in job.ops:
        # 约束9：ensures an operation to be scheduled exactly once
        constraint2.append(
            milp_constraint(constraint_name(2, job_id, op.op_id),
                            [x_name(job.id, op.op_id, machine[0]) for machine in op.available_machines],
                            [1.0 for machine in op.available_machines],
                            1.0, "E"))

        # 约束3、4：avoids the first operation of a job from being processed before the release date
        if op.op_id == 1:
            constraint3.append(milp_constraint(constraint_name(3, job_id, 1),
                                               [b_name(job.id, op.op_id)], [1.0], job.release_time, "G"))
        constraint4.append(milp_constraint(constraint_name(4, job_id, op.op_id),
                                           [b_name(job.id, op.op_id)], [1.0], 0, "G"))
        if op.op_id < len(job.ops):
            # 约束5：restricts that an operation cannot be processed until its job predecessor operation has been finished.
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
                    machine_list_intersection = tuple_first_intersection(op.available_machines, _op.available_machines)
                    # TODO 合并工序的开始时间约束，一会放在别的地方
                    for g, astyle in enumerate(gs):
                        # if (_op.job_id == 3 and _op.op_id == 3) or (op.job_id == 1 and op.op_id == 4):
                        #     print()
                        if (op.style.name == "assembling"
                                and if_hebing(job.style.value, op.op_id, _job.style.value, _op.op_id, g + 1)):

                            constraint10.append(
                                milp_constraint(
                                    name=constraint_name(10, job_id, op.op_id, '', '', _job.id,
                                                         _op.op_id) + '-g' + str(
                                        g + 1),
                                    variables_name=[b_name(_job.id, _op.op_id)] + [
                                        A_name(job_id, g + 1)] + [
                                                       A_name(_job.id, g + 1)] + [
                                                       b_name(job.id, op.op_id)],
                                    weights=[1.0] + [-W] + [-W] + [-1.0],
                                    rhs=-W * 2,
                                    sense="G"))

                            constraint11.append(
                                milp_constraint(
                                    name=constraint_name(11, _job.id, _op.op_id, '', '', job.id,
                                                         op.op_id) + '-g' + str(
                                        g + 1),
                                    variables_name=[b_name(job.id, op.op_id)] + [
                                        A_name(job_id, g + 1)] + [
                                                       A_name(_job.id, g + 1)] + [
                                                       b_name(_job.id, _op.op_id)],
                                    weights=[1.0] + [-W] + [-W] + [-1.0],
                                    rhs=-W * 2,
                                    sense="G"))

                            for machine in machine_list_intersection:
                                constraint12.append(
                                    milp_constraint(
                                        name=constraint_name(12, _job.id, _op.op_id, '', '', job.id,
                                                             op.op_id) + '-g' + str(
                                            g + 1),
                                        variables_name=[x_name(job.id, op.op_id, machine)] + [
                                            A_name(job_id, g + 1)] + [
                                                           A_name(_job.id, g + 1)] + [
                                                           x_name(_job.id, _op.op_id, machine)],
                                        weights=[1.0] + [-W] + [-W] + [-1.0],
                                        rhs=-W * 2,
                                        sense="G"))

                                constraint13.append(
                                    milp_constraint(
                                        name=constraint_name(13, _job.id, _op.op_id, '', '', job.id,
                                                             op.op_id) + '-g' + str(
                                            g + 1),
                                        variables_name=[x_name(_job.id, _op.op_id, machine)] + [
                                            A_name(job_id, g + 1)] + [
                                                           A_name(_job.id, g + 1)] + [
                                                           x_name(job.id, op.op_id, machine)],
                                        weights=[1.0] + [-W] + [-W] + [-1.0],
                                        rhs=-W * 2,
                                        sense="G"))
                        # TODO 不是所有的g，而是i，i'的g，并集
                        constraint14.append(milp_constraint(
                            name=constraint_name(14, job.id, op.op_id, _job.id, _op.op_id, g, job.style.value,
                                                 _job.style.value),
                            variables_name=[A_name(job.id, g + 1),
                                            Z_name(job.id, op.op_id, _job.id, _op.op_id, g + 1)],
                            weights=[1.0, -1.0],
                            rhs=0.0,
                            sense="G"
                        ))

                        constraint15.append(milp_constraint(
                            name=constraint_name(15, job.id, op.op_id, _job.id, _op.op_id, g, job.style.value,
                                                 _job.style.value),
                            variables_name=[A_name(_job.id, g + 1),
                                            Z_name(job.id, op.op_id, _job.id, _op.op_id, g + 1)],
                            weights=[1.0, -1.0],
                            rhs=0.0,
                            sense="G"
                        ))

                        constraint16.append(milp_constraint(
                            name=constraint_name(16, job.id, op.op_id, _job.id, _op.op_id, g, job.style.value,
                                                 _job.style.value),
                            variables_name=[Z_name(job.id, op.op_id, _job.id, _op.op_id, g + 1)],
                            weights=[-1.0],
                            rhs=-if_hebing(job.style.value, op.op_id, _job.style.value, _op.op_id, g + 1),
                            sense="G"
                        ))

                        constraint17.append(milp_constraint(
                            name=constraint_name(17, job.id, op.op_id, _job.id, _op.op_id, g, job.style.value,
                                                 _job.style.value),
                            variables_name=[A_name(job.id, g + 1), A_name(_job.id, g + 1),
                                            Z_name(job.id, op.op_id, _job.id, _op.op_id, g + 1)],
                            weights=[1.0, 1.0, -1.0],
                            rhs=-if_hebing(job.style.value, op.op_id, _job.style.value, _op.op_id, g + 1) + 2,
                            sense="L"
                        ))
                    for machine in machine_list_intersection:
                        # 约束6、7： avoid the overlap of operations processed by the same machine
                        constraint6.append(
                            milp_constraint(
                                name=constraint_name(6, job_id, op.op_id, _job.id, _op.op_id, machine),
                                variables_name=[b_name(_job.id, _op.op_id)] + [
                                    Y_name(job_id, op.op_id, _job.id, _op.op_id)] + [
                                                   x_name(job_id, op.op_id, machine)] + [
                                                   x_name(_job.id, _op.op_id, machine)
                                               ] +
                                               [b_name(job.id, op.op_id)] +
                                               [Z_name(job.id, op.op_id, _job.id,
                                                       _op.op_id, g + 1) for g, st in enumerate(gs)],
                                weights=[1.0] + [-W] + [-W] + [-W] + [-1.0] + [W for g, st in enumerate(gs)],
                                rhs=if_processed_(op, machine) -
                                    3.0 * W, sense="G"))

                        constraint7.append(
                            milp_constraint(
                                name=constraint_name(7, job_id, op.op_id, _job.id, _op.op_id, machine),
                                variables_name=[b_name(job.id, op.op_id)] + [
                                    Y_name(job_id, op.op_id, _job.id, _op.op_id)] + [
                                                   x_name(job_id, op.op_id, machine)] + [
                                                   x_name(_job.id, _op.op_id, machine)] +
                                               [b_name(_job.id, _op.op_id)] +
                                               [Z_name(job.id, op.op_id, _job.id,
                                                       _op.op_id, g + 1) for g, st in enumerate(gs)],
                                weights=[1.0] + [W] + [-W] + [-W] + [-1.0] + [W for g, st in enumerate(gs)],
                                rhs=if_processed_(_op, machine) -
                                    2.0 * W, sense="G"))

variables = split_every_element(decision_variables)
constraints = split_every_element(
    [constraint1,  # determine the maximum End time of scheduling plan
     constraint2,  # ensures an operation to be scheduled exactly once
     constraint3, constraint4,  # avoids the first operation of a job from being processed before the release date/0
     constraint5,  # 前序工序完成才能干下一个
     constraint6, constraint7,  # avoid the overlap of operations processed by the same machine
     constraint8,  # 准备合并约束1，工件得根据类型分配给对应的装配任务
     constraint9,  # 工件只能分配给一个装配任务
     constraint10, constraint11,  # 需要合并装配的工序，开始时间必须一致
     constraint12, constraint13,  # 需要合并装配的工序，必须强制分配到一个机器
     constraint14, constraint15, constraint16, constraint17  # 确定松弛变量，必须要求的装配在一起，Z=1，否则为0
     ])

solver = cplex_solver(variables, constraints, obj, "MIN")
solver.print_model()
# 开始计算

results = solver.run()
# 假设solver是你的求解器对象
try:
    # 创建一个字符串缓冲区来捕获输出
    with io.StringIO() as buf, redirect_stdout(buf):
        # 执行打印模型操作，输出会被捕获到buf中
        solver.print_model()
        # 获取捕获的内容
        model_output = buf.getvalue()

    # 将捕获的内容写入文件
    with open("model_output.txt", "w", encoding="utf-8") as f:
        f.write(model_output)

    print("模型输出已成功保存到 model_output.txt")
except Exception as e:
    print(f"保存文件时发生错误: {str(e)}")


for result in results:
    # result_name = spilt_variable_name(result)
    result_name = split(result[0])
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
    op = job.ops[2]
    print(str(job.id) + "_" + str(op.op_id)+"   "+str(op.end_time))
plot_gantt_chart(job_list, machine_list)
