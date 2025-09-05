# -*- coding: utf-8 -*-
# @Time    : 2025/1/5 15:03
# @Author  : 宁诗铎
# @Site    : 
# @File    : Operation.py
# @Software: PyCharm 
# @Comment : 工序类


class Operation:
    """
    表示一个操作，包含操作的作业ID、操作ID、操作类型及相关属性。

    Attributes:
        job_id (int): 此操作所属作业的唯一标识符。
        op_id (int): 此操作在作业中的唯一标识符。
        available_machines (list): 可用机器及对应加工时间的列表，每个元素为 (machine_id, processing_time)。
        to_machine (int): 此操作被分配的机器编号，初始为 -1 表示未分配。
        start_time (int): 此操作的开始时间，初始为 -1 表示未分配。
        end_time (int): 此操作的结束时间，初始为 -1 表示未分配。
        is_completed (bool): 标识此操作是否已完成，初始为 False。
    """

    def __init__(self, job_id, op_id, available_machines):
        """
        初始化一个操作实例。

        Args:
            job_id (int): 此操作所属作业的唯一标识符。
            op_id (int): 此操作在作业中的唯一标识符。
            available_machines (list): 可用机器及对应加工时间的列表。
        """
        self.job_id = job_id
        self.op_id = op_id
        self.available_machines = available_machines
        self.to_machine = -1  # 未分配机器时为 -1
        self.start_time = -1  # 未分配开始时间时为 -1
        self.end_time = -1  # 未分配结束时间时为 -1
        self.is_completed = False  # 操作初始化时未完成
        self.realease_time = -1

    def get_name(self):
        return f"O{self.job_id}_{self.op_id}"

    def __str__(self):
        return self.get_name()

    def __eq__(self, other):
        if isinstance(other, Operation):
            return (self.job_id, self.op_id) == (other.job_id, other.op_id)
        return False

    def clear(self):
        self.to_machine = -1  # 未分配机器时为 -1
        self.start_time = -1  # 未分配开始时间时为 -1
        self.end_time = -1  # 未分配结束时间时为 -1
        self.is_completed = False  # 操作初始化时未完成

    def get_processing_time_by_machine(self, machine_index):
        """
        根据机器索引获取加工时间。

        Args:
            machine_index (int): 机器的索引。

        Returns:
            int: 该机器对应的加工时间，如果机器不存在则返回 -1。
        """
        # 查找指定机器的加工时间，若未找到则返回 -1
        return next((time for m_index, time in self.available_machines if m_index == machine_index), -1)

    def assigned_to_machine(self, machine_index):
        """
        将当前操作分配给指定的机器。

        Args:
            machine_index (int): 机器的索引，用于标识分配的目标机器。
        """
        self.to_machine = machine_index

    def assigned_start_time(self, start_time):
        """
        设置当前操作的开始时间。

        Args:
            start_time (int): 工序的开始时间。
        """
        self.start_time = start_time

    def assigned_end_time(self, end_time):
        """
        设置当前操作的结束时间。

        Args:
            end_time (int): 工序的结束时间。
        """
        self.end_time = end_time

    def assigned_end_time_by_start(self):
        if self.start_time > -1 and int(self.to_machine) > -1:
            for tuple in self.available_machines:
                if tuple[0] == int(self.to_machine):
                    self.end_time = self.start_time + tuple[1]
                    break
        else:
            print("不能在这时赋值end_time")

    def assigned_time(self, start_time, end_time):
        """
        同时设置当前操作的开始时间和结束时间。

        Args:
            start_time (int): 工序的开始时间。
            end_time (int): 工序的结束时间。
        """
        self.assigned_start_time(start_time)
        self.assigned_end_time(end_time)

    def update(self, machine_index, start_time, end_time):
        """
        更新操作的分配信息，包括分配机器、开始时间、结束时间以及完成状态。

        Args:
            machine_index (int): 分配的机器编号。
            start_time (int): 工序的开始时间。
            end_time (int): 工序的结束时间。
        """
        self.assigned_to_machine(machine_index)
        self.assigned_time(start_time, end_time)
        self.is_completed = True  # 标记操作为已完成
