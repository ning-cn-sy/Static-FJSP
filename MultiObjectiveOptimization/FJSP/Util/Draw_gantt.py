# -*- coding: utf-8 -*-
# @Time    : 2025/1/5 15:55
# @Author  : 宁诗铎
# @Site    : 
# @File    : Draw_gantt.py
# @Software: PyCharm 
# @Comment : 画甘特图

from matplotlib import pyplot as plt
import matplotlib as mpl

# 设置中文字体配置（新增部分）
mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 微软雅黑
mpl.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 固定的颜色顺序 (RGB 转换为 0-1 范围的比例值)
fixed_colors = [
    (245 / 255, 99 / 255, 112 / 255),  # 平衡红色
    (255 / 255, 165 / 255, 89 / 255),  # 平衡橙色
    (255 / 255, 210 / 255, 120 / 255),  # 平衡金黄色
    (195 / 255, 235 / 255, 100 / 255),  # 平衡黄绿色
    (130 / 255, 200 / 255, 180 / 255),  # 平衡浅绿色
    (90 / 255, 170 / 255, 220 / 255),  # 平衡天蓝色
    (140 / 255, 115 / 255, 240 / 255),  # 平衡紫色
    (220 / 255, 120 / 255, 200 / 255),  # 平衡粉紫色
    (255 / 255, 115 / 255, 130 / 255),  # 平衡珊瑚红
    (255 / 255, 175 / 255, 115 / 255),  # 平衡橙黄色
    (255 / 255, 220 / 255, 145 / 255),  # 平衡浅金黄
    (160 / 255, 220 / 255, 120 / 255),  # 平衡草绿色
    (120 / 255, 215 / 255, 190 / 255),  # 平衡蓝绿色
    (115 / 255, 200 / 255, 250 / 255),  # 平衡深天蓝
    (125 / 255, 160 / 255, 250 / 255),  # 平衡蔚蓝色
    (165 / 255, 130 / 255, 250 / 255),  # 平衡蓝紫色
    (220 / 255, 130 / 255, 250 / 255),  # 平衡洋红色
    (250 / 255, 130 / 255, 210 / 255),  # 平衡玫瑰红
    (250 / 255, 130 / 255, 165 / 255),  # 平衡胭脂红
    (250 / 255, 80 / 255, 100 / 255)  # 平衡亮红
]


# def plot_gantt_chart(jobs, machines, title="生产甘特图"):
#     """
#     绘制甘特图，显示每台机器的操作时间段，每个相同工件的颜色一致。
#     矩形块上显示工件号、工序号和时长。对于装配操作，用黑色表示。
#
#     :param jobs: 工件列表，每个工件是一个对象，包含以下属性：
#                  - 'id': 工件编号
#                  - 'ops': 操作列表，每个操作是一个对象，包含：
#                      - 'to_machine': 分配的机器编号
#                      - 'start_time': 操作开始时间
#                      - 'end_time': 操作结束时间
#                      - 'op_id': 工序编号
#     :param machines: 机器对象列表，每个对象包含以下属性：
#                      - 'id': 机器编号
#     """
#
#     # 为每个工件分配颜色
#     job_colors = {}
#     unique_job_ids = sorted(job.id for job in jobs)  # 保证顺序一致
#     for idx, job_id in enumerate(unique_job_ids):
#         job_colors[job_id] = fixed_colors[idx % len(fixed_colors)]  # 循环使用颜色
#
#     total_height = 10
#     total_width = 7
#     # 创建甘特图，并仅修改 dpi 提高分辨率-------小规模是5，2-------中、大规模是10，6
#     fig, ax = plt.subplots(figsize=(total_height, total_width), dpi=120)  # 设置分辨率为 300 dpi
#
#     # 调整机器的纵坐标位置间距
#     machine_spacing = 100  # 间距大小
#     machine_positions = {machine.id: idx * machine_spacing for idx, machine in enumerate(machines)}
#
#     for job in jobs:
#         job_id = job.id
#         color = job_colors[job_id]  # 获取当前工件的颜色
#
#         for op in job.ops:
#             machine = op.to_machine
#             start = op.start_time
#             duration = op.end_time - start
#
#             # 如果操作是 Assembling_operation 类型，使用黑色
#             rect_color = color
#             text_color = 'black'
#
#             rect_text = f"{job_id} - {op.op_id}\n{duration}"
#             edge_color = 'black'
#
#             # 使用新的纵坐标位置
#             try:
#                 machine_pos = machine_positions[machine]
#             except:
#                 machine_pos = 0
#             ax.barh(y=machine_pos, width=duration, left=start,
#                     height=(total_height / len(machines) * machine_spacing / 2),
#                     color=rect_color,
#                     edgecolor=edge_color,
#                     label=f"Job {job_id}")
#
#             # 在矩形块中显示工件号、工序号、时长
#             text_x = start + duration / 2  # 文本的X位置居中
#             text_y = machine_pos  # 文本的Y位置与机器对齐
#             ax.text(text_x, text_y, rect_text,
#                     ha='center', va='center', color=text_color, fontsize=9)
#
#     # 设置轴标签和标题
#     ax.set_xlabel("时间", fontsize=14)
#     ax.set_ylabel("工位", fontsize=14)
#     ax.set_title(title, fontsize=16)
#
#     # 更新纵坐标
#     ax.set_yticks([machine_positions[machine.id] for machine in machines])
#     ax.set_yticklabels([f"M {machine.id}" for machine in machines])
#
#     # 计算 x 轴的最大值，即 makespan
#     makespan = max(op.end_time for job in jobs for op in job.ops)
#
#     # 绘制 makespan 的垂直线
#     ax.axvline(x=makespan, color='red', linestyle='--', linewidth=1.5, label="Makespan")
#
#     # 在垂直线顶部标注 makespan 值
#     ax.text(makespan, ax.get_ylim()[1], f"{makespan}",
#             ha='center', va='bottom', color='red', fontsize=10)
#     plt.grid(axis='x', linestyle='--', alpha=0.7)
#     plt.tight_layout()
#     plt.show()


def plot_gantt_chart(jobs, machines, title="Gantt Chart"):
    """
    绘制甘特图，显示每台机器的操作时间段，每个相同工件的颜色一致。
    矩形块上显示工件号、工序号和时长。对于装配操作，用黑色表示。

    :param jobs: 工件列表，每个工件是一个对象，包含以下属性：
                 - 'id': 工件编号
                 - 'ops': 操作列表，每个操作是一个对象，包含：
                     - 'to_machine': 分配的机器编号
                     - 'start_time': 操作开始时间
                     - 'end_time': 操作结束时间
                     - 'op_id': 工序编号
    :param machines: 机器对象列表，每个对象包含以下属性：
                     - 'id': 机器编号
    """

    # 为每个工件分配颜色
    job_colors = {}
    unique_job_ids = sorted(job.id for job in jobs)  # 保证顺序一致
    for idx, job_id in enumerate(unique_job_ids):
        job_colors[job_id] = fixed_colors[idx % len(fixed_colors)]  # 循环使用颜色

    total_height = 10
    total_width = 6
    # 创建甘特图，并仅修改 dpi 提高分辨率
    fig, ax = plt.subplots(figsize=(total_height, total_width), dpi=300)  # 设置分辨率为 300 dpi

    # 调整机器的纵坐标位置间距
    machine_spacing = 100  # 间距大小
    machine_positions = {machine.id: idx * machine_spacing for idx, machine in enumerate(machines)}

    for job in jobs:
        job_id = job.id
        color = job_colors[job_id]  # 获取当前工件的颜色

        for op in job.ops:
            machine = op.to_machine
            start = op.start_time
            duration = op.end_time - start
            op_id = op.op_id
            # 如果操作是 Assembling_operation 类型，使用黑色
            rect_color = color
            text_color = 'black'

            rect_text = f"{job_id} - {op.op_id}\n{duration}"
            edge_color = 'black'

            # 使用新的纵坐标位置
            try:
                machine_pos = machine_positions[machine]
            except:
                machine_pos = -1
            ax.barh(y=machine_pos, width=duration, left=start,
                    height=(total_height / len(machines) * machine_spacing / 2),
                    color=rect_color,
                    edgecolor=edge_color,
                    label=f"Job {job_id}")

            # 在矩形块中显示工件号、工序号、时长
            text_x = start + duration / 2  # 文本的X位置居中
            text_y = machine_pos  # 文本的Y位置与机器对齐
            ax.text(text_x, text_y, rect_text,
                    ha='center', va='center', color=text_color, fontsize=8)

    # 设置轴标签和标题
    ax.set_xlabel("Time")
    ax.set_ylabel("Machine")
    ax.set_title(title)

    # 更新纵坐标
    ax.set_yticks([machine_positions[machine.id] for machine in machines])
    ax.set_yticklabels([f"Machine {machine.id}" for machine in machines])

    # 计算 x 轴的最大值，即 makespan
    makespan = max(op.end_time for job in jobs for op in job.ops)

    # 绘制 makespan 的垂直线
    ax.axvline(x=makespan, color='red', linestyle='--', linewidth=1.5, label="Makespan")

    # 在垂直线顶部标注 makespan 值
    ax.text(makespan, ax.get_ylim()[1], f"{makespan}",
            ha='center', va='bottom', color='red', fontsize=10)
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

