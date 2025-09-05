# -*- coding: utf-8 -*-
# @Time    : 2024/6/21 15:10
# @Author  : 宁诗铎
# @Site    : 
# @File    : draw_util.py
# @Software: PyCharm 
# @Comment : 作图工具类

import matplotlib.pyplot as plt
from pylab import mpl

# 设置显示中文字体
mpl.rcParams["font.sans-serif"] = ["SimHei"]
# 设置正常显示符号
mpl.rcParams["axes.unicode_minus"] = False

# 有点问题，跟problem里的不一样，这里是按照初始的顺序，那个是加工的顺序
# 我先按开始的时间排个序
def draw_gantt_chart(tasks, machine_list, auxiliary_module_list):
    fig, ax = plt.subplots()
    # 创建机器到y轴位置的映射
    machine_to_y = {}
    y_base = 10
    for a in machine_list:
        machine_to_y[a.id] = len(machine_to_y) * y_base
    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray',
              'tab:olive', 'tab:cyan']

    job_to_color = {}
    # 添加矩形块
    color_index = 0
    # 字典1 存机器id  现在机器上对应的am块的id
    # 字典2 存am id  对应am 现在在的机器id
    current_machine_am = {machine.id: 0 for machine in machine_list}
    current_am_machine = {am.id: 0 for am in auxiliary_module_list}
    machine = []
    am = []
    for b in range(len(tasks)):
        machine.append(tasks[b].machine)
        am.append(tasks[b].am)
    for b in range(len(tasks)):
        task = tasks[b]
        job_id = task.op.job_id
        op_id = task.op.id
        if job_id not in job_to_color:
            job_to_color[job_id] = colors[color_index % len(colors)]
            color_index += 1

        start_time = tasks[b].start_time
        duration = tasks[b].duration
        assemble_time = tasks[b].am.assemble_time
        disassemble_time = tasks[b].am.disassemble_time
        y_position = machine_to_y[tasks[b].machine.id]
        color = job_to_color[job_id]
        complete_time = tasks[b].complete_time
        # 工序块
        ax.broken_barh([(start_time, duration)], (y_position, y_base - 1), facecolors=color, edgecolors='black')
        # 在矩形块上添加文本
        ax.text(start_time + duration / 2, y_position + (y_base - 1) / 2, str(job_id) + "_" + str(op_id),
                ha='center', va='center', color='white', fontsize=8)
        # 画am块
        #  当前机器使用的模块
        k = [k for k, v in current_machine_am.items() if v == tasks[b].am.id]
        # 1. 当前机器machine[b]上的am 和现在 要用的am不一样  2.k 是 用了当前am的机器列表，现在的机器和上一个用am的机器不一样。那也不应该是K-1这里边也没有顺序
        if tasks[b].am.id != 0:
            if (current_machine_am[tasks[b].machine.id] is not tasks[b].am.id) or (
                    current_am_machine[tasks[b].am.id] is not tasks[b].machine.id):
                ax.broken_barh([(start_time - assemble_time, assemble_time)], (y_position, y_base - 1),
                               facecolors='lightgray', edgecolors='black')
                ax.text(start_time - assemble_time / 2, y_position + (y_base - 1) / 2,
                        "A" + str(tasks[b].am.id) + "\nup",
                        ha='center', va='center', color='black', fontsize=8)
                current_machine_am[tasks[b].machine.id] = tasks[b].am.id
                current_am_machine[tasks[b].am.id] = tasks[b].machine.id
            # 判断要不要画拆卸   1. 同一机器 am换了  2. 相同的am在不同机器
            # index 当前的am所在的机器索引
            # 原版
            # try:
            #     index_am = am[b + 1:].index(am[b].id) + b + 1
            # except ValueError:
            #     index_am = b
            #     # 下一次用这个机器时的索引 ，找他所对应的am
            # try:
            #     index_machine = machine[b + 1:].index(machine[b].id) + b + 1
            # except ValueError:
            #     index_machine = b

            try:
                index_am = am[b + 1:].index(am[b].id) + b + 1
            except ValueError:
                index_am = b
            # 下一次用这个机器时的索引 ，找他所对应的am
            try:
                index_machine = machine[b + 1:].index(machine[b].id) + b + 1
            except ValueError:
                index_machine = b
            # 这个机器下一次用的am 和现在的am是否相等  2. 这个am所在的下一个机器  与现在的机器是否相等
            if (tasks[index_machine].am.id is not tasks[b].am.id) or (
                    tasks[index_am].machine.id is not tasks[b].machine.id):
                ax.broken_barh([(complete_time, disassemble_time)], (y_position, y_base - 1),
                               facecolors='lightgray', edgecolors='black')
                ax.text(complete_time + disassemble_time / 2, y_position + (y_base - 1) / 2,
                        "A" + str(tasks[b].am.id) + "\ndown",
                        ha='center', va='center', color='black', fontsize=8)

    # 设置y轴
    yticks = [pos + y_base / 2 for pos in machine_to_y.values()]
    yticklabels = list(machine_to_y.keys())
    ax.set_yticks(yticks)
    ax.set_yticklabels(yticklabels)
    ax.set_xlim(left=0)

    ax.set_xlabel('Time')
    ax.set_ylabel('Machines')
    ax.grid(True)

    plt.show()


def draw_line_chart(y_data, x_data=[], title='折线图', x_label='X', y_label='Y'):
    if len(x_data) == 0:
        x_data = range(len(y_data))
    plt.plot(x_data, y_data, marker='o')
    # 添加标题和标签
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    # 显示图表
    plt.show()
