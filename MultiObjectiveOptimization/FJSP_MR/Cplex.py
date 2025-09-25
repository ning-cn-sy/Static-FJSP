# -*- coding: utf-8 -*-
# @Time    : 2024/6/5 15:58
# @Author  : XXX
# @Site    : 
# @File    : test_main.py
# @Software: PyCharm 
# @Comment :
import csv
from datetime import time



from ExactAlgorithm.Config.Milp import milp_variable, milp_constraint
from ExactAlgorithm.Config.Task import Task
from ExactAlgorithm.Solver.CPLEX.Cplex_Solver import cplex_solver

from ExactAlgorithm.Util.draw_util import draw_gantt_chart
from Util.generate import read_info
from Util.name_util import t_name, c_name, x_name, y_name, h_name, s_name, constraint_name, spilt_variable_name
from Util.pub_data import W
from Util.pub_func import get_process_time, if_processed, if_processed_by_machine, get_y_factor, \
    split_every_element, get_task_by_id, get_reconfigure_time_τ, get_reconfigure_time_γ, arr

def writecsv(file_name, data):
    """将数据写入CSV文件"""
    with open(file_name, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        for row in data:
            csv_writer.writerow(row)
# job_list, machine_list, auxiliary_module_list = generate_data()

for i in range(1, 2):
    if i < 10:
        case = f"MFJS0{i}"
    else:
        case = f"MFJS{i}"
        # MFJS01.fjs
    job_list, machine_list, auxiliary_module_list = read_info(f"D:\PhD\Research\PythonResearch\pythonProject\MultiObjectiveOptimization\FJSP_MR_1\Example\\{case}.fjs")
    # job_list, machine_list, auxiliary_module_list = read_info(r"D:\pythonlearning\ExactAlgorithm\Example\Mk01_MR.fjs")
    # job_list, machine_list, auxiliary_module_list = generate_test_data()

    decision_variables = [[], [], [], [], [], []]
    for job in job_list:
        decision_variables[0].append(milp_variable(t_name(job.id), type="C"))
        for op in job.op_list:
            decision_variables[1].append(milp_variable(c_name(job.id, op.id), type="C"))
            for machine in machine_list:
                decision_variables[2].append(milp_variable(x_name(job.id, op.id, machine.id), 1, 0, type="I"))
                for am in auxiliary_module_list:
                    decision_variables[3].append(
                        milp_variable(y_name(job.id, op.id, machine.id, am.id), 1, 0, type="I"))
            for _job in job_list:
                for _op in _job.op_list:
                    if _op != op:
                        decision_variables[4].append(
                            milp_variable(h_name(job.id, op.id, _job.id, _op.id), 1, 0, type="I"))
                        decision_variables[5].append(
                            milp_variable(s_name(job.id, op.id, _job.id, _op.id), 1, 0, type="I"))
    # 准备目标
    obj = []
    for index, decision_variable in enumerate(decision_variables):
        for _index, variable in enumerate(decision_variable):
            if index == 0:
                obj.append(job_list[_index].weight)
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
        op_len = len(job.op_list)
        # 准备约束1和2
        constraint1.append(
            milp_constraint(constraint_name(1, job_id), [t_name(job_id), c_name(job_id, op_len)], [1.0, -1.0],
                            -job.delivery_time, "G"))
        constraint2.append(
            milp_constraint(constraint_name(2, job_id), [t_name(job_id)], [1.0],
                            0.0, "G"))
        # 准备约束3
        for op in job.op_list:
            op_id = op.id
            constraint3.append(
                milp_constraint(constraint_name(3, job_id, op_id),
                                [x_name(job_id, op_id, machine.id) for machine in machine_list],
                                [1.0 for machine in machine_list],
                                1.0, "E"))
            # 准备约束4
            for machine in machine_list:
                machine_id = machine.id
                constraint4.append(milp_constraint(name=constraint_name(4, job_id, op_id, machine_id),
                                                   variables_name=[x_name(job_id, op_id, machine.id)], weights=[1.0],
                                                   rhs=if_processed_by_machine(op, machine), sense="L"))

                # 准备约束5
                constraint5.append(
                    milp_constraint(constraint_name(5, job_id, op_id, machine_id),
                                    [y_name(job_id, op_id, machine_id, am.id) for am in auxiliary_module_list] + [
                                        x_name(job_id, op_id, machine_id)],
                                    [1.0 for am in auxiliary_module_list] + [-1.0], 0.0, "E"))
                # 准备约束6
                for am in auxiliary_module_list:
                    am_id = am.id
                    constraint6.append(
                        milp_constraint(constraint_name(6, job_id, op_id, machine_id, am_id),
                                        [y_name(job_id, op_id, machine_id, am.id)], [1.0],
                                        rhs=if_processed(op, machine, am),
                                        sense="L"))
                    # 准备约束10
                    for _job in job_list:
                        _job_id = _job.id
                        for _op in list(set(_job.op_list) - set(list([op]))):
                            _op_id = _op.id
                            for _am in auxiliary_module_list:
                                _am_id = _am.id
                                # 准备约束10
                                constraint10.append(milp_constraint(
                                    name=constraint_name(10, job_id, op_id, machine_id, am_id, _job_id, _op_id, _am.id),
                                    variables_name=[c_name(job_id, op_id)] + [c_name(_job_id, _op_id)] + [
                                        y_name(job_id, op_id, machine_id, am.id)] + [
                                                       y_name(_job_id, _op_id, machine_id, _am_id)] + [
                                                       h_name(job_id, op_id, _job_id, _op_id)],
                                    weights=[1.0] + [-1.0] + [-W] + [-W] + [-W],
                                    rhs=get_process_time(op, machine, am) + get_reconfigure_time_γ(machine, am,
                                                                                                   _am) - 3.0 * W,
                                    sense="G"
                                ))
                                # 准备约束11
                                constraint11.append(milp_constraint(
                                    name=constraint_name(11, job_id, op_id, machine_id, am_id, _job_id, _op_id, _am.id,
                                                         0),
                                    variables_name=[c_name(_job_id, _op_id)] + [c_name(job_id, op_id)] + [
                                        y_name(job_id, op_id, machine_id, am.id)] + [
                                                       y_name(_job_id, _op_id, machine_id, _am_id)] + [
                                                       h_name(job_id, op_id, _job_id, _op_id)],
                                    weights=[1.0] + [-1.0] + [-W] + [-W] + [W],
                                    rhs=get_process_time(_op, machine, _am) + get_reconfigure_time_γ(machine, _am,
                                                                                                     am) - 2.0 * W,
                                    sense="G"))
                    if am_id != 0:
                        # 准备约束12
                        for _job in job_list:
                            _job_id = _job.id
                            for _op in list(set(_job.op_list) - set(list([op]))):
                                _op_id = _op.id
                                for _machine in machine_list:
                                    _machine_id = _machine.id
                                    constraint12.append(milp_constraint(
                                        name=constraint_name(12, job_id, op_id, machine_id, am_id, _job_id, _op_id,
                                                             _machine.id, 1),
                                        variables_name=[c_name(job_id, op_id)] + [c_name(_job_id, _op_id)] + [
                                            y_name(job_id, op_id, machine_id, am_id)] + [
                                                           y_name(_job_id, _op_id, _machine_id, am_id)] + [
                                                           s_name(job_id, op_id, _job_id, _op_id)],
                                        weights=[1.0] + [-1.0] + [-W] + [-W] + [-W],
                                        rhs=get_process_time(op, machine, am) + get_reconfigure_time_τ(machine,
                                                                                                       _machine,
                                                                                                       am) - 3.0 * W,
                                        sense="G"))
                                    # 准备约束13
                                    constraint13.append(milp_constraint(
                                        name=constraint_name(13, job_id, op_id, machine_id, am_id, _job_id, _op_id,
                                                             _machine.id, 1),
                                        variables_name=[c_name(_job_id, _op_id)] + [c_name(job_id, op_id)] + [
                                            y_name(job_id, op_id, machine_id, am_id)] + [
                                                           y_name(_job_id, _op_id, _machine_id, am_id)] + [
                                                           s_name(job_id, op_id, _job_id, _op_id)],
                                        weights=[1.0] + [-1.0] + [-W] + [-W] + [W],
                                        rhs=get_process_time(_op, _machine, am) +
                                            get_reconfigure_time_τ(_machine, machine, am) - 2.0 * W, sense="G"))

            # 准备约束7
            y_variable_name = [y_name(job_id, op_id, machine.id, am.id) for machine in machine_list
                               for am in auxiliary_module_list]

            if op_id == 1:
                constraint7.append(milp_constraint(constraint_name(7, job_id, op_id),
                                                   [c_name(job_id, op_id)] + y_variable_name,
                                                   [1.0] + get_y_factor(False, op, machine_list,
                                                                        auxiliary_module_list),
                                                   rhs=job.release_time, sense="G"))
            else:
                # 准备约束8
                constraint8.append(milp_constraint(constraint_name(8, job_id, op_id),
                                                   [c_name(job_id, op_id)] + [
                                                       c_name(job_id, op_id - 1)] + y_variable_name,
                                                   [1.0] + [-1.0] + get_y_factor(False, op, machine_list,
                                                                                 auxiliary_module_list), rhs=0.0,
                                                   sense="G"))
            # 准备约束9
            constraint9.append(
                milp_constraint(constraint_name(9, job_id, op_id),
                                [c_name(job_id, op_id)] + y_variable_name,
                                [1.0] + get_y_factor(True, op, machine_list, auxiliary_module_list), rhs=0.0,
                                sense="G"))

    variables = split_every_element(decision_variables)
    constraints = split_every_element(
        [constraint1, constraint2, constraint3, constraint4, constraint5, constraint6, constraint7,
         constraint8, constraint9, constraint10, constraint11, constraint12, constraint13])

    solver = cplex_solver(variables, constraints, obj, "MIN")
    # 开始计算

    result = solver.run()
    tasks_list = []
    num = 0
    for i in range(len(result)):
        variable_name = spilt_variable_name(result, i)
        if variable_name[0] == "C":
            op = job_list[int(variable_name[1]) - 1].op_list[int(variable_name[2]) - 1]
            tasks_list.append(Task(op=op, start_time=-3.1, duration=-3.2, complete_time=result[i][1],
                                   machine=None, am=None))
        if variable_name[0] == "y" and result[i][1] > 0.5:
            # num = num + 1
            # print(num)
            # print(get_task_by_id(variable_name[1], variable_name[2], tasks_list).id)
            cur_task = get_task_by_id(variable_name[1], variable_name[2], tasks_list)
            cur_task.duration = cur_task.op.available_machines_am[(int(variable_name[3]), int(variable_name[4]))]
            cur_task.set_start_time_automatic()
            cur_task.machine = machine_list[int(variable_name[3]) - 1]
            # if int(variable_name[4]) == 0:
            #     print()
            cur_task.am = auxiliary_module_list[int(variable_name[4])]
        # print(variable_name)
    tasks_list = arr(tasks_list)
    draw_gantt_chart(tasks_list, machine_list, auxiliary_module_list)
    print()
