# -*- coding: utf-8 -*-
# @Time    : 2024/12/28 14:11
# @Author  : 宁诗铎
# @Site    : 
# @File    : Job.py
# @Software: PyCharm 
# @Comment : 工件类，存储工件类型的各种数据
import copy
from enum import Enum

from MultiObjectiveOptimization.FJSP_AO.Config.Operation import Assembling_operation, Machining_operation


class Job_style(Enum):
    """
    定义工件类型的枚举，用于标识工件的分类。

    Attributes:
        style1 (int): 工件类型1。
        style2 (int): 工件类型2。
        style3 (int): 工件类型3。

    TODO:
        如果需要更多的工件类型，可以在此扩展。
    """
    style1 = 1
    style2 = 2
    style3 = 3
    style4 = 4
    style5 = 5
    style6 = 6
    style7 = 7


from enum import Enum


class Job_style(Enum):
    """
    定义工件类型的枚举，用于标识工件的分类。

    Attributes:
        style1 (int): 工件类型1。
        style2 (int): 工件类型2。
        style3 (int): 工件类型3。
        style4 (int): 工件类型4。
        style5 (int): 工件类型5。
        style6 (int): 工件类型6。
        style7 (int): 工件类型7。
    """
    style1 = 1
    style2 = 2
    style3 = 3
    style4 = 4
    style5 = 5
    style6 = 6
    style7 = 7
    style8 = 8
    style9 = 9
    style10 = 10
    style11 = 11
    style12 = 12
    style13 = 13
    style14 = 14
    style15 = 15
    style16 = 16
    style17 = 17
    style18 = 18
    style19 = 19
    style20 = 20
    style21 = 21
    style22 = 22
    style23 = 23
    style24 = 24
    style25 = 25
    style26 = 26

    @classmethod
    def from_value(cls, value):
        """
        根据数值返回对应的枚举成员。

        参数:
        value (int): 枚举成员的数值。

        返回:
        Job_style: 对应的枚举成员。

        如果数值不合法，抛出 ValueError。
        """
        try:
            return cls(value)
        except ValueError:
            raise ValueError(f"无效的工件类型值：{value}")


# # 示例使用：
# job_type = Job_style.from_value(3)
# print(job_type)  # 输出：Job_style.style3


def copy_job(job):
    ops = []
    for op in job.ops:
        if isinstance(op, Assembling_operation):
            op_ = Assembling_operation(op.job_id, op.op_id, op.style, op.available_machines, op.assemble_style)
        else:
            op_ = Machining_operation(op.job_id, op.op_id, op.style, op.available_machines)
        ops.append(op_)
    return Job(job.id, job.style, ops, job.release_time)


class Job:
    """
    Job 类表示一个工件对象，包含工件的基本信息和操作列表。

    Attributes:
        id (int): 工件的唯一标识。
        style (Job_style): 工件的类型，使用 Job_style 枚举表示。
        ops (list): 工件的操作列表，每个操作可以是加工或装配操作。
        release_time (int): 工件的释放时间，表示该工件最早可以开始加工的时间点。
    """

    def __init__(self, id, style: Job_style, ops, release_time=-1):
        """
        初始化 Job 实例。

        Args:
            id (int): 工件的唯一标识。
            style (Job_style): 工件的类型。
            ops (list): 工件的操作列表，包含加工和装配操作。
            release_time (int): 工件的释放时间。
        """
        self.id = id  # 工件的唯一标识
        self.style = style  # 工件的类型
        self.ops = ops  # 工件的操作列表
        self.release_time = release_time  # 工件的释放时间
        self.origin_style = style
        self.assembly_jobs = set()

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

    def get_end_style(self):
        return self.ops[-1].assemble_style

    def __str__(self):
        return str(self.id)

    # def __eq__(self, other):
    #     return self.id == other.id

    def get_assembly_op_num(self) -> int:
        num = 0
        for op in reversed(self.ops):
            if isinstance(op, Assembling_operation):
                num += 1
            else:
                return num
        return -1
