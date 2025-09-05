# -*- coding: utf-8 -*-
# @Time    : 2024/6/5 16:12
# @Author  : 宁诗铎
# @Site    : 
# @File    : Machine.py
# @Software: PyCharm 
# @Comment : 机器名称


class Machine:
    """
    机器类
    1. id
    2. 机器名称
    """

    def __init__(self, id, name = None):
        self.id = id  # 机器id
        self.name = name  # 机器名称

    def __eq__(self, other):
        return self.id == other
