# -*- coding: utf-8 -*-
# @Time    : 2025/4/15 14:21
# @Author  : 宁诗铎
# @Site    : 
# @File    : MachineRules.py
# @Software: PyCharm 
# @Comment :

from MultiObjectiveOptimization.FJSP_AO.Algrithm.Rule.BaseRule import BaseMachineRule

from MultiObjectiveOptimization.FJSP_AO.Config.Operation import Operation


class SPT_MachineRule(BaseMachineRule):
    """最短处理时间优先（基于元组）"""

    def __init__(self):
        super().__init__("SPT_Machine")

    def calculate_priority(self, op: Operation, machine_info: tuple) -> float:
        # machine_info 是 (machine_id, processing_time)
        return machine_info[1]  # 直接返回处理时间作为优先级
