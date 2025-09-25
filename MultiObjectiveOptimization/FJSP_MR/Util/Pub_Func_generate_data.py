# -*- coding: utf-8 -*-
# @Time    : 2024/6/25 21:26
# @Author  : XXX
# @Site    : 
# @File    : Pub_Func_generatedataaaaa.py
# @Software: PyCharm 
# @Comment :
import math
import random
from MultiObjectiveOptimization.FJSP_MR.Util.Random_seed import seed

random.seed(6)

from MultiObjectiveOptimization.FJSP_MR.Config.AuxiliaryModules import AuxiliaryModules
from MultiObjectiveOptimization.FJSP_MR.Util.Read_data import readDataByFJS
from MultiObjectiveOptimization.FJSP_MR.Config.Job import Job
from MultiObjectiveOptimization.FJSP_MR.Config.Machine import Machine
from MultiObjectiveOptimization.FJSP_MR.Config.Operation import Operation


def generate_test_data():
    # 自己做小算例
    machine1 = Machine(1, "钻床")
    machine2 = Machine(2, "铣床")
    machine3 = Machine(3, "车床")
    am0 = AuxiliaryModules(0, None, 0, 0)
    am1 = AuxiliaryModules(1, "主轴", 2, 1)
    am2 = AuxiliaryModules(2, "刀架", 1, 2)

    job1 = Job(1, "工件1", 3.0, 8.0, 4.0)
    job2 = Job(2, "工件2", 2.0, 12.0, 1.0)
    job3 = Job(3, "工件3", 4.0, 10.0, 2.0)
    op1 = Operation(1, 1, {(3, 0): 4.0, (2, 1): 3.0}, job1)
    op2 = Operation(2, 1, {(2, 0): 5.0, (3, 1): 4.0}, job1)
    op3 = Operation(3, 1, {(1, 2): 3.0, (3, 0): 4.0, (3, 2): 2.0}, job1)
    op4 = Operation(1, 2, {(1, 2): 2.0, (3, 0): 5.0}, job2)
    op5 = Operation(2, 2, {(2, 0): 3.0, (3, 0): 5.0, (3, 2): 4.0}, job2)
    op6 = Operation(1, 3, {(1, 0): 5.0, (1, 2): 3.0, (2, 2): 2.0, (3, 2): 4.0}, job3)
    op7 = Operation(2, 3, {(2, 0): 3.0, (2, 1): 2.0, (3, 0): 3.0}, job3)
    op8 = Operation(3, 3, {(1, 2): 4.0, (3, 0): 3.0}, job3)
    op9 = Operation(4, 3, {(2, 1): 2.0, (2, 2): 2.0, (3, 0): 3.0}, job3)

    job1.op_list = [op1, op2, op3]
    job2.op_list = [op4, op5]
    job3.op_list = [op6, op7, op8, op9]
    job_list = [job1, job2, job3]
    machine_list = [machine1, machine2, machine3]
    auxiliary_module_list = [am0, am1, am2]
    return job_list, machine_list, auxiliary_module_list


def generate_job_info(con_digit, job_list):
    # con_digit常数 系数
    # 文章里的 p min和pmax  min 与Oij的加工时间有关
    p_max = 0
    for job in job_list:
        p_min_add = 0
        for op in job.op_list:
            p_max = max(max(op.available_machines_am.values()), p_max)
            # 一个工件的所有的pmin 加和
            p_min_add += min(op.available_machines_am.values())
        job.release_time = random.randint(0, p_max)
        job.delivery_time = con_digit * p_min_add
        job.weight = calculate_job_weight(job.id, len(job_list))
    return p_max



def generate_am_list(flex, job_list, machine_list):
    auxiliary_module_list = []
    # 机器数量
    m = len(machine_list)
    # am数量
    # am_num = round(random.uniform(m / 4, m / 2))
    am_num = 2
    # 配置时间后边根据p_max算
    for i in range(am_num + 1):
        auxiliary_module_list.append(AuxiliaryModules(id=i, name=f"am{i}", assemble_time={}, disassemble_time={}))
    #  对每一个工序的可用机器am里头加
    for job in job_list:
        for op in job.op_list:
            # 遍历字典不能添加值
            origin_available_machine_list = list(op.available_machines_am.items())
            # 单独把机器拿出来
            origin_available_machine_id = []
            sum_process_time = 0
            # 对当前工序的每一个可用机器
            for available_machine, process_time in origin_available_machine_list:
                # 遍历可用的机器 填进id列表里，方便后边排除
                origin_available_machine_id.append(available_machine[0])
                # 能用的加工时间 总和，求平均时间给后边的机器
                sum_process_time = sum_process_time + process_time
                # 可选的am列表，选flex个，表示一个工序可以用当前机器的flex种配置加工
                ### 每次选择不都用固定的那几个am了吗，实际是每次循环一个值
                avail_ams_list = random.sample(range(1, am_num + 1), flex - 1)
                # 遍历可以用的am
                for avail_am in avail_ams_list:
                    # 新的一个配置组合
                    machine_add_am = (available_machine[0], avail_am)
                    op.available_machines_am[machine_add_am] = round(random.uniform(0.9 * process_time,
                                                                                    1.0 * process_time))
            # 一开始不能加工的机器，配上am可以加工
            for machine in machine_list:
                if machine.id not in origin_available_machine_id and random.random() > 0.6:
                    # 除 0 以外随机选flex个am
                    avail_ams_list = random.sample(range(1, am_num + 1), flex)
                    average_process_time = sum_process_time / len(origin_available_machine_id)
                    for avail_am in avail_ams_list:
                        op.available_machines_am[machine.id, avail_am] = round(
                            random.uniform(0.8 * average_process_time,
                                           1.0 * average_process_time))
    return auxiliary_module_list


def generate_reconfiguration_time(job_list, machine_list, auxiliary_module_list):
    p_max = generate_job_info(1.0, job_list)
    # 对应的号就是am几
    #  0 应该也得算一个 这里的am_num是算0的am的数量
    am_num = len(auxiliary_module_list)
    for i in range(1, am_num):
        for machine in machine_list:
            # 装时间
            a = int(random.uniform(p_max, 2 * p_max))
            # 拆时间
            b = int(random.uniform(0.8 * a, 1.2 * a))
            # 把am0的安装时间也写成字典
            auxiliary_module_list[0].assemble_time[machine.name] = 0
            auxiliary_module_list[0].disassemble_time[machine.name] = 0
            auxiliary_module_list[i].assemble_time[machine.name] = a
            auxiliary_module_list[i].disassemble_time[machine.name] = b


def calculate_job_weight(job_id, total_jobs):
    # 对于20%、60%和20%的工件延迟权重分别设置为1、2和4
    if job_id < 0.2 * total_jobs:
        return 1
    elif job_id > 0.8 * total_jobs:
        return 4
    else:
        return 2


def read_info(path=""):
    job_list, machine_list = readDataByFJS(path)
    # 加am进去 ，flex表示工序可以由一个机器两种不同的配置处理
    flex = 2
    auxiliary_module_list = generate_am_list(flex, job_list, machine_list)
    generate_reconfiguration_time(job_list, machine_list, auxiliary_module_list)
    return job_list, machine_list, auxiliary_module_list
