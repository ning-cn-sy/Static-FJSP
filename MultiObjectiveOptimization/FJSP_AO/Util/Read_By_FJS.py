# -*- coding: utf-8 -*-
# @Time    : 2025/1/5 15:11
# @Author  : 宁诗铎
# @Site    : 
# @File    : Read_By_FJS.py
# @Software: PyCharm 
# @Comment : 读取MK系列的FJS文件
import random

from MultiObjectiveOptimization.FJSP_AO.Config.Job import Job
from MultiObjectiveOptimization.FJSP_AO.Config.Machine import Machine
from MultiObjectiveOptimization.FJSP_AO.Config.Operation import Op_style, Machining_operation


def readDataByFJS(fileNameFjs):
    file = open(fileNameFjs, "r")

    basicInformation = file.readline().strip().split("\t")
    num_jobs = basicInformation[0]
    num_machines = basicInformation[1]

    info_jobs = []
    info_machines = []
    for i in range(int(num_machines)):
        info_machines.append(Machine(i + 1, random.randint(1, 10), 2))

    for name in range(int(num_jobs)):
        result = file.readline().strip().split("  ")
        num_ops = result[0]
        code = result[1].strip().split(" ")
        job_id = name + 1
        job = Job(job_id, None, [], 0)
        for op_index in range(int(num_ops)):
            op = Machining_operation(job_id, op_index + 1, Op_style.machining, [])
            num_available_machines = code[0]
            del code[0]
            for i in range(int(num_available_machines)):
                op.available_machines.append((int(code[0]), int(code[1])))
                del code[0]
                del code[0]
            job.ops.append(op)

        info_jobs.append(job)
    # limited_jobs = []
    # for job in info_jobs[:10]:  # 遍历前五个工件
    #     # 提取每个工件的前五道工序
    #     limited_ops = job.ops[:10]  # 这里是访问 job 的 ops 属性
    #     # 创建一个新的 Job 对象，仅包含前五道工序
    #     limited_job = Job(job.id, job.style, limited_ops, job.release_time)
    #     limited_jobs.append(limited_job)

    return info_jobs, info_machines
