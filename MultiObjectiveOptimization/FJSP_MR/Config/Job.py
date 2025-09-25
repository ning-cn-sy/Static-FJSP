# -*- coding: utf-8 -*-
# @Time    : 2024/6/5 16:04
# @Author  : 宁诗铎
# @Site    : 
# @File    : Job.py
# @Software: PyCharm 
# @Comment : 工件类，这里表示每个工件
from MultiObjectiveOptimization.FJSP_MR.Config.Operation import Operation


class Job:
    """
    表示工件类，里面有两个属性
    1.id
    2.工件名称
    3.工序列表
    """

    def __init__(self, id, name = None, release_time = 0, delivery_time = 0, weight = 0, job_complete_time = 0, op_list: Operation = []):
        self.name = name
        self.id = id
        self.op_list = op_list
        self.release_time = release_time
        self.delivery_time = delivery_time
        self.weight = weight
        self.job_complete_time = job_complete_time