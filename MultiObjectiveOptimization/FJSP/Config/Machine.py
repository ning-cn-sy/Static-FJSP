# -*- coding: utf-8 -*-
# @Time    : 2025/1/5 15:03
# @Author  : 宁诗铎
# @Site    : 
# @File    : Machine.py
# @Software: PyCharm 
# @Comment : 机器类


class Machine:
    """
    Machine 类表示调度问题中的机器资源。

    Attributes:
        id (int): 机器的唯一标识。
    """

    def __init__(self, id):
        """
        初始化 Machine 实例。

        Args:
            id (int): 机器的唯一标识。
        """
        self.id = id  # 机器的唯一标识
