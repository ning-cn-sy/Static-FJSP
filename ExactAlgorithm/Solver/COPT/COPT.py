# -*- coding: utf-8 -*-
# @Time    : 2024/6/26 18:24
# @Author  : 宁诗铎
# @Site    : 
# @File    : COPT.py
# @Software: PyCharm 
# @Comment : 调用杉树求解器

import coptpy as copt

# 创建COPT环境和模型
env = copt.Envr()
model = env.createModel()

# 添加变量
x = model.addVar(lb=0.0, ub=copt.COPT.INFINITY, name='x')
y = model.addVar(lb=0.0, ub=copt.COPT.INFINITY, name='y')

# 设置目标函数
model.setObjective(3*x + 4*y, sense=copt.COPT.MAXIMIZE)

# 添加约束
model.addConstr(x + 2*y <= 4, name='c1')
model.addConstr(2*x + y <= 3, name='c2')

# 优化模型
model.solve()

# 输出结果
if model.status == copt.COPT.OPTIMAL:
    print(f'Optimal objective value: {model.objval}')
    print(f'x = {x.x}')
    print(f'y = {y.x}')
else:
    print('No optimal solution found.')
