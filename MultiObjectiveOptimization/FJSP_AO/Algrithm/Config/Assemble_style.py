# -*- coding: utf-8 -*-
# @Time    : 2024/12/28 20:21
# @Author  : 宁诗铎
# @Site    : 
# @File    : Assemble_style.py
# @Software: PyCharm 
# @Comment : 装配类型


class Assemble_style:
    """
    Assemble_style 类用于定义装配规则，描述两种工件类型如何通过装配生成新工件。

    Attributes:
        name (str): 装配规则的名称，用于标识该装配规则。
        param1 (Job_style or Assemble_style): 装配需求的第1种工件类型或装配规则。
        param2 (Job_style or Assemble_style): 装配需求的第2种工件类型或装配规则。
    """

    def __init__(self, name):
        """
        初始化 Assemble_style 实例。

        Args:
            name (str): 装配规则的名称。
        """
        self.name = name  # 装配规则的名称
        self.param1 = None  # 装配需求的第1种工件类型或装配规则，初始为 None
        self.param2 = None  # 装配需求的第2种工件类型或装配规则，初始为 None
        self.ops = []

