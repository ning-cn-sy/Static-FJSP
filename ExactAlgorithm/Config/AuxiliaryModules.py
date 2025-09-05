# -*- coding: utf-8 -*-
# @Time    : 2024/6/6 14:33
# @Author  : 于程嘉
# @Site    : 
# @File    : AuxiliaryModules.py.py
# @Software: PyCharm 
# @Comment : 辅助模块定义auxiliary modules

class AuxiliaryModules:
    def __init__(self, id, name, assemble_time, disassemble_time):
        self.id = id  # 模块id
        self.name = name  # 模块名称
        self.assemble_time = assemble_time
        self.disassemble_time = disassemble_time

    def __eq__(self, other):
        return self.id == other