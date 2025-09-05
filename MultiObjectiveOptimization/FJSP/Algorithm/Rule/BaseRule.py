# -*- coding: utf-8 -*-
# @Time    : 2025/3/4 22:31
# @Author  : 宁诗铎
# @Site    : 
# @File    : BaseRule.py
# @Software: PyCharm 
# @Comment : 用于存放规则基类


from abc import ABC, abstractmethod
from typing import List

from MultiObjectiveOptimization.FJSP.Config.Job import Job
from MultiObjectiveOptimization.FJSP.Config.Machine import Machine
from MultiObjectiveOptimization.FJSP.Config.Operation import Operation

from abc import ABC, abstractmethod


class BaseRule(ABC):
    """规则抽象基类（统一方法名）"""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def execute(self, *args, **kwargs):  # 关键修改：方法名改为 execute
        pass


class BaseSequencingRule(BaseRule):
    """顺序编排规则基类（继承修正后的 BaseRule）"""

    def execute(self, jobs: List[Job]) -> List[int]:  # 方法名统一为 execute
        priority_list = []
        global_idx = 0
        for job in jobs:
            for op in job.ops:
                priority = self.calculate_priority(job, op, global_idx)
                priority_list.append((priority, global_idx))
                global_idx += 1
        sorted_ops = sorted(priority_list, key=lambda x: x[0])
        return [idx for (_, idx) in sorted_ops]

    @abstractmethod
    def calculate_priority(self, job: Job, op: Operation, global_idx: int) -> float:
        pass


class BaseMachineRule(BaseRule):
    def execute(self, op: Operation, machines: List[tuple]) -> int:
        """基类统一执行逻辑（直接处理 (machine_id, processing_time) 元组）"""
        priorities = []
        for machine_info in machines:  # machine_info 是 (machine_id, processing_time)
            priority = self.calculate_priority(op, machine_info)
            priorities.append((priority, machine_info[0]))  # 使用 machine_id 作为标识
        # 按优先级升序排列（数值越小优先级越高）
        sorted_machines = sorted(priorities, key=lambda x: x[0])
        # 直接返回元组在列表中的索引
        return machines.index((sorted_machines[0][1], next(t for _, t in machines if _ == sorted_machines[0][1])))

    @abstractmethod
    def calculate_priority(self, op: Operation, machine: Machine) -> float:
        pass

