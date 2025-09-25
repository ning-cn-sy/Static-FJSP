# -*- coding: utf-8 -*-
# @Time    : 2024/6/5 16:08
# @Author  : 宁诗铎
# @Site    : 
# @File    : Operation.py
# @Software: PyCharm 
# @Comment : 工序类
import copy


class Operation:
    def __init__(self, id, job_id, available_machines_am, machine=None, am=None, job=None):
        """
        类注释
        """
        self.id = id  # 自身id
        self.job_id = job_id  # 工件种类
        self.available_machines_am = available_machines_am  # 工序的可用机器以及AM的组合的时间
        self.job = job
        self.machine = machine
        self.am = am
        self.name = job_id + id
        self.start_time = 0
        self.complete_time = 0
        self.duration = 0
        self.ROij = self.start_time
        self.QOij = 0
        # TODO：还有其他属性

    def __str__(self):
        return "O" + str(self.job_id) + "-" + str(self.id)

    def __repr__(self):
        return self.__str__()

    # def __eq__(self, other):
    #     return self.id == other.id and self.job_id == other.job_id

    def __eq__(self, other):
        if isinstance(other, Operation):
            return (self.job_id, self.id) == (other.job_id, other.id)
        return False

    def __hash__(self):
        return hash((self.job_id, self.id))

    # def copy(self):
    #     object = type(self)(self.id, self.job_id, self.available_machines_am, self.machine, self.am, self.job)
    #     # 手动添加其他属性
    #
    #     # 添加属性之后不好使了，又说找不到
    #     object.name = self.name
    #     object.start_time = self.start_time
    #     object.duration = self.duration
    #     object.ROij = self.ROij
    #     object.QOij = self.QOij
    #     object.complete_time = self.complete_time
    #     return object

    def copy(self):
        # 创建一个新的实例
        copied_object = type(self).__new__(self.__class__)

        # 深度复制所有属性
        copied_object.__dict__ = copy.deepcopy(self.__dict__)

        return copied_object
