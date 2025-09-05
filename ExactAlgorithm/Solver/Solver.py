# -*- coding: utf-8 -*-
# @Time    : 2024/6/26 20:43
# @Author  : 宁诗铎
# @Site    : 
# @File    : Solver.py
# @Software: PyCharm 
# @Comment : 求解器类
from abc import ABC, abstractmethod

from ExactAlgorithm.Config.Milp import milp_variable, milp_constraint


class Solver(ABC):
    def __init__(self, name):
        self.name = name
        self.prob = None

    @abstractmethod
    def run(self):
        print("去具体类里面改写")

    @abstractmethod
    def prepare_variables(self, variables: [milp_variable]):
        print("去具体类里面改写")

    @abstractmethod
    def prepare_constraints(self, constraints: [milp_constraint]):
        print("去具体类里面改写")

    @abstractmethod
    def prepare_objectives(self, objs, obj_sense):
        print("去具体类里面改写")

    def print_model(self):
        print("小于来改写")
