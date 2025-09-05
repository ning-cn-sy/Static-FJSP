# -*- coding: utf-8 -*-
# @Time    : 2024/6/26 19:14
# @Author  : 宁诗铎
# @Site    : 
# @File    : Cplex_Solver.py
# @Software: PyCharm 
# @Comment : 用于Cplex求解

import cplex
# from cplex.exceptions import CplexError

from ExactAlgorithm.Config.Milp import milp_variable, milp_constraint
from ExactAlgorithm.Solver.Solver import Solver
# from MultiObjectiveOptimization.FJSP_AO.Util.Pub_func import check_duplicates_names, check_duplicates_values


class CplexError:
    pass


class cplex_solver(Solver):
    """
    自变量 约束 目标
    """

    def __init__(self, variables: [milp_variable], constraints: [milp_constraint], objs, obj_sense):
        # 目标、变量、约束
        super().__init__("CPLEX")
        self.prob = cplex.Cplex()
        self.prepare_variables(variables, objs)
        self.prepare_constraints(constraints)
        self.prepare_objectives(objs, obj_sense)
        self.prob.write("FJSP_AO_model_nsd_.lp")

    def run(self):
        try:
            # 实例化一个cplex优化器
            self.print_model()
            # 求解
            self.prob.solve()

            # 显示最优情况下的变量值
            x = self.prob.solution.get_values()
            print(x)

            # 显示最优情况下的目标值
            objective_value = self.prob.solution.get_objective_value()
            print(objective_value)
            solution_values = self.prob.solution.get_values()

            return [(self.prob.variables.get_names()[i], solution_values[i]) for i in range(len(solution_values))]
        except CplexError as exc:
            print(exc)

    def prepare_variables(self, variables: [milp_variable], objs):
        ub, lb, variables_name, types = [], [], [], ""
        for variable in variables:
            ub.append(variable.ub)
            lb.append(variable.lb)
            variables_name.append(variable.name)
            types += variable.type
        # 添加变量：变量在目标函数里的系数，变量的上下界，变量类型，名称
        self.prob.variables.add(obj=objs, lb=lb, ub=ub, types=types,
                                names=variables_name)

    def prepare_constraints(self, constraints: [milp_constraint]):
        rows, rhs, constraints_sense, constraints_names = [], [], [], []
        for row in constraints:
            rows.append([[name for name in row.variables_name], [weight for weight in row.weights]])
            rhs.append(row.rhs)
            constraints_sense += row.sense
            constraints_names.append(row.name)

        # aaaaa = check_duplicates_names(constraints_names)
        # bbbbb = check_duplicates_values(rows)
        print()
        # 添加约束：约束左值，等式/不等式符号，右值，名称
        self.prob.linear_constraints.add(lin_expr=rows, senses=constraints_sense,
                                         rhs=rhs, names=constraints_names)

    def prepare_objectives(self, objs, obj_sense):
        # 求解的目标为目标函数的最小值
        if obj_sense == "MAX":
            self.prob.objective.set_sense(self.prob.objective.sense.maximize)

        elif obj_sense == "MIN":
            self.prob.objective.set_sense(self.prob.objective.sense.minimize)
        else:
            print("MILP  OBJ   类型设置错啦！！！！！")

    def print_model(self):
        cpx = self.prob
        # 打印目标函数
        objective = cpx.objective.get_linear()
        variable_names = cpx.variables.get_names()

        print("Objective function:")
        for var_index, coef in enumerate(objective):
            print(f"{coef}*{variable_names[var_index]}", end=" + ")
        print("\n")

        # 打印约束
        constraints = cpx.linear_constraints.get_rows()
        sense = cpx.linear_constraints.get_senses()
        rhs = cpx.linear_constraints.get_rhs()
        constraint_names = cpx.linear_constraints.get_names()

        sense_map = {"L": "<=", "G": ">=", "E": "="}

        print("Constraints:")
        for i, row in enumerate(constraints):
            print(f"Constraint {constraint_names[i]}:")
            for var_index, coef in zip(row.ind, row.val):
                print(f"{coef}*{variable_names[var_index]}", end=" + ")
            print(f"{sense_map[sense[i]]} {rhs[i]}")
            print()
