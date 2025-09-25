# -*- coding: utf-8 -*-
# @Time    : 2024/6/22 15:11
# @Author  : 于程嘉
# @Site    :
# @File    : Tasks.py
# @Software: PyCharm
# @Comment : 加工工序类
from Operation import Operation


class Task1:
    # 加工的工序序列信息

    def __init__(self, op: Operation = None, machine=None, am=None, start_time=-3.3, duration=-3.3, complete_time=-3.4):
        self.op = op
        self.machine = machine
        self.am = am
        self.start_time = start_time
        self.duration = duration
        self.complete_time = complete_time

    def set_start_time_automatic(self):
        self.start_time = self.complete_time - self.duration
