# -*- coding: utf-8 -*-
# @Time    : 2025/3/4 22:37
# @Author  : 宁诗铎
# @Site    : 
# @File    : SequencingRules.py
# @Software: PyCharm 
# @Comment : 调度排序规则rule


from typing import List

from MultiObjectiveOptimization.FJSP.Algorithm.Rule.BaseRule import BaseSequencingRule
from MultiObjectiveOptimization.FJSP.Config.Job import Job
from MultiObjectiveOptimization.FJSP.Config.Operation import Operation


# File: SequencingRules.py
class SPT_SequencingRule(BaseSequencingRule):
    """最短处理时间优先（基于 available_machines）"""

    def __init__(self):
        super().__init__("SPT_Sequencing")

    def calculate_priority(self, job: Job, op: Operation, global_idx: int) -> float:
        # 获取所有机器的加工时间并计算平均值
        processing_times = [time for (machine_id, time) in op.available_machines]
        return sum(processing_times) / len(processing_times) if processing_times else 0.0


class LPT_SequencingRule(BaseSequencingRule):
    """最长处理时间优先（基于 available_machines）"""

    def __init__(self):
        super().__init__("LPT_Sequencing")

    def calculate_priority(self, job: Job, op: Operation, global_idx: int) -> float:
        # 获取所有机器的加工时间并计算平均值
        processing_times = [time for (machine_id, time) in op.available_machines]
        return -sum(processing_times) / len(processing_times) if processing_times else 0.0
