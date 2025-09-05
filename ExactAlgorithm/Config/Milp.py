# -*- coding: utf-8 -*-
# @Time    : 2024/6/26 19:18
# @Author  : 宁诗铎
# @Site    : 
# @File    : Milp.py
# @Software: PyCharm 
# @Comment : Milp相关属性
from ExactAlgorithm.Util.pub_data import infinity


class milp_variable:
    """
    自变量
    名称、上界、下界、类型
    """

    def __init__(self, name, ub=infinity, lb=0.0, type="C"):
        self.name = name
        self.ub = ub
        self.lb = lb
        self.type = type

    def __str__(self):
        return self.name


class milp_constraint:
    """
    约束
    名称、自变量名称、系数、右侧常数项、大于小于符号
    """

    def __init__(self, name, variables_name, weights, rhs, sense):
        self.name = name
        self.variables_name = variables_name
        self.weights = weights
        self.rhs = rhs
        self.sense = sense

    def __str__(self):
        return self.name
