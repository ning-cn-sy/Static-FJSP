# -*- coding: utf-8 -*-
# @Time    : 2024/6/26 21:12
# @Author  : 宁诗铎
# @Site    : 
# @File    : copt_solver.py
# @Software: PyCharm 
# @Comment : 杉树科技求解器
from abc import ABC

import coptpy as copt

from ExactAlgorithm.Config.Milp import milp_variable, milp_constraint
from ExactAlgorithm.Solver.Solver import Solver


class copt_solver(Solver, ABC):
    def __init__(self, variables: [milp_variable], constraints: [milp_constraint], objs, obj_sense):
        super().__init__("COPT", variables, constraints, objs, obj_sense)
        self.prob = copt.Envr().createModel()
        self.prepare_data()

    def prepare_data(self):
        self.copt_variables = [self.prob.addVar(variable.lb, ub=variable.ub, name=variable.name) for variable in
                          self.variables]
        objective = copt.LinExpr()
        for var, coeff in zip(self.copt_variables, self.objs):
            objective += coeff * var
        self.prob.setObjective(objective, sense=self.obj_sense)

    def run(self):
        model = self.prob
        model.solve()

        # 输出结果
        if model.status == copt.COPT.OPTIMAL:
            print(f'Optimal objective value: {model.objval}')
            for variable in self.copt_variables:
                print(f'x = {x.x}')
        else:
            print('No optimal solution found.')
