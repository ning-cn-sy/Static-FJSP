# -*- coding: utf-8 -*-
# @Time    : 2025/1/5 15:01
# @Author  : 宁诗铎
# @Site    : 
# @File    : Job.py
# @Software: PyCharm 
# @Comment : 工件类
from enum import Enum

from MultiObjectiveOptimization.FJSP.Config.Operation import Operation


def copy_job(job):
    ops = []
    for op in job.ops:
        op_ = Operation(op.job_id, op.op_id, op.available_machines)
        ops.append(op_)
    return Job(job.id, ops, job.release_time)


class Job:
    """
    Job 类表示一个工件对象，包含工件的基本信息和操作列表。

    Attributes:
        id (int): 工件的唯一标识。
        ops (list): 工件的操作列表，每个操作可以是加工或装配操作。
        release_time (int): 工件的释放时间，表示该工件最早可以开始加工的时间点。
    """

    def __init__(self, id, ops, release_time):
        """
        初始化 Job 实例。

        Args:
            id (int): 工件的唯一标识。
            ops (list): 工件的操作列表，包含加工和装配操作。
            release_time (int): 工件的释放时间。
        """
        self.id = id  # 工件的唯一标识
        self.ops = ops  # 工件的操作列表
        self.release_time = release_time  # 工件的释放时间

    def get_num_ops(self):
        """
        获取工件的操作数量。

        Returns:
            int: 工件操作的总数。
        """
        return len(self.ops)

    def is_complete(self, op_id):
        """
        判断指定的操作是否为工件的最后一个操作。

        Args:
            op_id (int): 操作的索引。

        Returns:
            bool: 如果是最后一个操作，返回 True；否则返回 False。
        """
        return op_id == self.get_num_ops() - 1

    def get_id_str(self):
        """
        获取工件ID的字符串表示形式。

        Returns:
            str: 工件ID的字符串形式。
        """
        return str(self.id)

    def clear_ops(self):
        for op in self.ops:
            op.clear()

    def __str__(self):
        return str(self.id)
