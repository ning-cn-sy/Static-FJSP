# -*- coding: utf-8 -*-
# @Time    : 2024/6/5 16:08
# @Author  : 宁诗铎
# @Site    : 
# @File    : Operation.py
# @Software: PyCharm 
# @Comment : 工序类


class Operation:
    def __init__(self, id, job_id, available_machines_am, job=None):
        """
        类注释
        """
        self.id = id  # 自身id
        self.job_id = job_id  # 工件种类
        self.available_machines_am = available_machines_am  # 工序的可用机器以及AM的组合的时间
        self.job = job
        self.name = job_id + id
        self.start_time = -1.3
        self.complete_time = 0

        # TODO：还有其他属性

    def __str__(self):
        return "工件id：" + str(self.job_id) + "   工序：" + str(self.id)
