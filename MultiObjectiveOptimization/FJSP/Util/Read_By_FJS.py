# -*- coding: utf-8 -*-
# @Time    : 2025/1/5 15:11
# @Author  : 宁诗铎
# @Site    : 
# @File    : Read_By_FJS.py
# @Software: PyCharm 
# @Comment : 读取MK系列的FJS文件
from MultiObjectiveOptimization.FJSP.Config.Job import Job
from MultiObjectiveOptimization.FJSP.Config.Machine import Machine
from MultiObjectiveOptimization.FJSP.Config.Operation import Operation


def readDataByFJS(fileNameFjs):
    file = open(fileNameFjs, "r")

    basicInformation = file.readline().strip().split("\t")
    num_jobs = basicInformation[0]
    num_machines = basicInformation[1]

    info_jobs = []
    info_machines = []
    for i in range(int(num_machines)):
        info_machines.append(Machine(i))

    for name in range(int(num_jobs)):
        result = file.readline().strip().split("  ")
        num_ops = result[0]
        code = result[1].strip().split(" ")
        job_id = name + 1
        job = Job(job_id, [], 0.0)
        for op_index in range(int(num_ops)):
            op = Operation(job_id, op_index + 1, [])
            num_available_machines = code[0]
            del code[0]
            for i in range(int(num_available_machines)):
                op.available_machines.append((int(code[0]), int(code[1])))
                del code[0]
                del code[0]
            job.ops.append(op)

        info_jobs.append(job)

    return info_jobs, info_machines


def read_info(path):
    workpieceInfo, = readDataByFJS(path)

    return workpieceInfo


if __name__ == '__main__':
    readDataByFJS("D:\pythonProject\MultiObjectiveOptimization\FJSP_MT\Example\Mk01.fjs")
