# -*- coding: utf-8 -*-
# @Time    : 2024/6/27 16:42
# @Author  : XXX
# @Site    : 
# @File    : pub_func.py
# @Software: PyCharm 
# @Comment :



def get_task_by_id(job_id, op_id, task_list):
    for task in task_list:
        if task.op.job_id == int(job_id) and task.op.id == int(op_id):
            return task
    return None


def split_every_element(group=[[]]):
    return [element for group_element in group for element in group_element]

#
# def if_processed_by_machine(op: Operation, machine: Machine):
#     for key in op.available_machines_am:
#         if key[0] == machine.id:
#             return 1.0
#     return 0.0
#
#
# def if_processed(op: Operation, machine: Machine, am: AuxiliaryModules = AuxiliaryModules(0, "", 0, 0)):
#     for key in op.available_machines_am:
#         if key[0] == machine.id and key[1] == am.id:
#             return 1.0
#     return 0.0
#
#
# def get_process_time(op: Operation, machine: Machine, am: AuxiliaryModules):
#     return 0.0 if (machine.id, am.id) not in op.available_machines_am else float(
#         op.available_machines_am[(machine.id, am.id)])
#
#
# def get_y_factor(is_assemble, op, machine_list, auxiliary_module_list):
#     return [-(get_process_time(op, machine, am) + (is_assemble * am.assemble_time)) for machine in machine_list
#             for am in auxiliary_module_list]
#
#
# def get_reconfigure_time_τ(machine: Machine, _machine: Machine, am: AuxiliaryModules):
#     return 0.0 if machine == _machine else float(am.disassemble_time + am.assemble_time)
#
#
# def get_reconfigure_time_γ(am: AuxiliaryModules, _am: AuxiliaryModules):
#     return 0.0 if am == _am else float(am.assemble_time + _am.disassemble_time)
#
#
# # γ
# def get_reconfigure_time_g(am: AuxiliaryModules, _am: AuxiliaryModules):
#     return 0.0 if am == _am else float(am.assemble_time + _am.disassemble_time)
#
#
# def get_reconfigure_time_t(machine: Machine, _machine: Machine, am: AuxiliaryModules):
#     return 0.0 if machine == _machine else float(am.disassemble_time + am.assemble_time)


def arr(tasks_list):
    n = len(tasks_list)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if tasks_list[j].start_time > tasks_list[j + 1].start_time:
                tasks_list[j], tasks_list[j + 1] = tasks_list[j + 1], tasks_list[j]
                swapped = True
        if not swapped:
            break
    return tasks_list
