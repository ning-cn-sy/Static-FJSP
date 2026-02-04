# -*- coding: utf-8 -*-
# @Time    : 2024/12/28 19:14
# @Author  : 宁诗铎
# @Site    : 
# @File    : Plot_Func.py
# @Software: PyCharm 
# @Comment : 画图公共类
import os
import uuid

from matplotlib import pyplot as plt

from MultiObjectiveOptimization.FJSP_AO.Algrithm.Decode import Decode
from MultiObjectiveOptimization.FJSP_AO.Config.Operation import Assembling_operation
# from MultiObjectiveOptimization.FJSP_AO.Util.Pareto_dominates import get_non_dominated_front
from MultiObjectiveOptimization.FJSP_AO.Util.Plot_util.Plot_point_Func import plot_points_and_connections_by_jobs

# 固定的颜色顺序 (RGB 转换为 0-1 范围的比例值)
# fixed_colors = [
#     (245 / 255, 99 / 255, 112 / 255),  # 平衡红色
#     (255 / 255, 165 / 255, 89 / 255),  # 平衡橙色
#     (255 / 255, 210 / 255, 120 / 255),  # 平衡金黄色
#     (195 / 255, 235 / 255, 100 / 255),  # 平衡黄绿色
#     (130 / 255, 200 / 255, 180 / 255),  # 平衡浅绿色
#     (90 / 255, 170 / 255, 220 / 255),  # 平衡天蓝色
#     (140 / 255, 115 / 255, 240 / 255),  # 平衡紫色
#     (220 / 255, 120 / 255, 200 / 255),  # 平衡粉紫色
#     (255 / 255, 115 / 255, 130 / 255),  # 平衡珊瑚红
#     (255 / 255, 175 / 255, 115 / 255),  # 平衡橙黄色
#     (255 / 255, 220 / 255, 145 / 255),  # 平衡浅金黄
#     (160 / 255, 220 / 255, 120 / 255),  # 平衡草绿色
#     (120 / 255, 215 / 255, 190 / 255),  # 平衡蓝绿色
#     (115 / 255, 200 / 255, 250 / 255),  # 平衡深天蓝
#     (125 / 255, 160 / 255, 250 / 255),  # 平衡蔚蓝色
#     (165 / 255, 130 / 255, 250 / 255),  # 平衡蓝紫色
#     (220 / 255, 130 / 255, 250 / 255),  # 平衡洋红色
#     (250 / 255, 130 / 255, 210 / 255),  # 平衡玫瑰红
#     (250 / 255, 130 / 255, 165 / 255),  # 平衡胭脂红
#     (250 / 255, 80 / 255, 100 / 255)  # 平衡亮红
# ]
import matplotlib.colors as mcolors

from MultiObjectiveOptimization.FJSP_AO1.Util.Instance.large_instance import large_Instance_paper1

# Create a set of 40 colors, adjusting RGB values for less vivid tones
fixed_colors = [
    (0.6, 0.2, 0.2), (0.6, 0.3, 0.1), (0.7, 0.5, 0.1), (0.6, 0.7, 0.2),
    (0.5, 0.7, 0.5), (0.4, 0.6, 0.7), (0.5, 0.4, 0.8), (0.6, 0.4, 0.7),
    (0.8, 0.4, 0.5), (0.9, 0.6, 0.2), (0.9, 0.8, 0.4), (0.7, 0.6, 0.2),
    (0.4, 0.5, 0.4), (0.4, 0.6, 0.5), (0.3, 0.7, 0.6), (0.6, 0.5, 0.7),
    (0.4, 0.3, 0.8), (0.7, 0.3, 0.7), (0.6, 0.2, 0.6), (0.8, 0.5, 0.7),
    (0.7, 0.6, 0.6), (0.9, 0.4, 0.6), (0.8, 0.5, 0.6), (0.9, 0.7, 0.7),
    (0.7, 0.4, 0.7), (0.7, 0.5, 0.9), (0.6, 0.6, 0.7), (0.5, 0.8, 0.8),
    (0.5, 0.7, 0.9), (0.6, 0.6, 0.5), (0.6, 0.7, 0.6), (0.6, 0.5, 0.6),
    (0.8, 0.7, 0.5), (0.9, 0.6, 0.4), (0.4, 0.5, 0.6), (0.5, 0.7, 0.4),
    (0.7, 0.5, 0.5), (0.6, 0.6, 0.6), (0.5, 0.5, 0.7), (0.7, 0.7, 0.8)
]

# You can now use this muted_colors list for plotting or other purposes.



def plot_gantt_chart(jobs, machines, group, line_filename, title="Gantt Chart"):
    """
    绘制更美观的甘特图，使用圆角矩形、阴影效果和更好的排版
    """
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from matplotlib.font_manager import FontProperties

    # 为每个工件分配颜色
    job_colors = {}
    unique_job_ids = sorted(job.id for job in jobs)
    for idx, job_id in enumerate(unique_job_ids):
        job_colors[job_id] = fixed_colors[idx % len(fixed_colors)]

    # 创建图形和轴
    fig, ax = plt.subplots(figsize=(16, 9), dpi=1200)  # 使用更宽的16:9比例

    # 设置全局样式
    # plt.style.use('seaborn-whitegrid')  # 使用更美观的seaborn样式

    # 调整机器的纵坐标位置间距
    machine_spacing = 2
    machine_positions = {machine.id: idx * machine_spacing for idx, machine in enumerate(machines)}
    bar_height = 1  # 增加条高度以获得更好的视觉效果

    # 最大结束时间
    max_end_time = max(op.end_time for job in jobs for op in job.ops)

    # 设置坐标范围
    ax.set_xlim(0, 15000)
    ax.set_ylim(-1, max(machine_positions.values()) + 2)

    # 绘制每个操作
    for job in jobs:
        job_id = job.id
        color = job_colors[job_id]

        for op in job.ops:
            machine = op.to_machine
            start = op.start_time
            end = op.end_time
            duration = end - start

            # 检查操作类型
            is_assembling = False
            rect_text = f""
            if isinstance(op, Assembling_operation) and op.assemble_jobs != []:
                is_assembling = True
                for group_id, group_jobs in group.items():
                    if job in group_jobs:
                        job_names = op.assemble_jobs[-1]
                        rect_text = f"{job_names[0]}\n{job_names[1]},{job_names[2]}"
                        break

            # 获取机器位置
            try:
                machine_pos = machine_positions[machine]
            except:
                machine_pos = 0

            y_bottom = machine_pos - bar_height / 2

            # 创建圆角矩形
            rect = patches.FancyBboxPatch(
                (start, y_bottom),
                duration,
                bar_height,
                boxstyle=patches.BoxStyle("Round", pad=0.1, rounding_size=0.3),
                linewidth=1,
                edgecolor='#555555' if not is_assembling else '#000000',
                facecolor='lightgray' if is_assembling else lighten_color(color, 0.7),
                alpha=0.95 if is_assembling else 0.85,
                zorder=3
            )
            ax.add_patch(rect)

            # 添加阴影效果 - 在矩形右下方创建一个深色矩形
            shadow = patches.FancyBboxPatch(
                (start + 0.1, y_bottom - 0.1),
                duration,
                bar_height,
                boxstyle=patches.BoxStyle("Round", pad=0.1, rounding_size=0.3),
                linewidth=0,
                facecolor='#00000020',
                zorder=2
            )
            ax.add_patch(shadow)

            # 添加文本
            text_x = start + duration / 2
            text_y = machine_pos
            text_color = '#333333' if not is_assembling else 'black'
            ax.text(text_x, text_y, rect_text,
                    ha='center', va='center', color=text_color,
                    fontsize=11, fontweight='bold', zorder=4)

    # 添加机器分隔线
    for machine in machines:
        machine_pos = machine_positions[machine.id]
        ax.axhline(y=machine_pos, color='#CCCCCC', linestyle='-', linewidth=1, alpha=0.7)

    # 设置轴标签和标题
    ax.set_xlabel("Time", fontsize=14, fontweight='bold')
    ax.set_ylabel("Machine", fontsize=14, fontweight='bold')
    ax.set_title(f"{title}\nMakespan: {max_end_time:.1f}", fontsize=14, fontweight='bold')

    # 绘制结束时间线
    ax.axvline(x=max_end_time, color='#FF5555', linestyle='--', linewidth=1.5, zorder=5)
    ax.text(max_end_time, max(machine_positions.values()) -7, f"Makespan: {max_end_time:.1f}",
            color='#FF5555', ha='right', va='bottom', fontsize=28, fontweight='bold')

    yticks = []
    yticklabels = []

    # 设置纵坐标
    for machine in machines:
        if machine.id < 11:
            yticks.append(machine_positions[machine.id])  # Position for machines with id < 11
            yticklabels.append(f"{machine.id}")  # Label with just the id
        else:
            yticks.append(machine_positions[machine.id])  # Position for machines with id >= 11
            yticklabels.append(f"A{machine.id - 10}")  # Label with 'A' and id adjusted by -10

    # Set the y-ticks and y-tick labels on the axis
    ax.set_yticks(yticks)
    ax.set_yticklabels(yticklabels, fontsize=14)

    # # 添加图例
    # from matplotlib.patches import Patch
    # legend_elements = [Patch(facecolor=job_colors[job_id], label=f'Job {job_id}')
    #                    for job_id in unique_job_ids]
    # legend_elements.append(Patch(facecolor='lightgray', label='Assembling'))
    #
    # ax.legend(handles=legend_elements, loc='lower right', framealpha=1.0,
    #           title="Job Colors", title_fontsize=12, fontsize=12, ncol=2)

    # 添加网格
    plt.grid(axis='x', linestyle='-', color='#F0F0F0', linewidth=0.8, alpha=0.7)
    plt.grid(axis='y', linestyle='-', color='#F0F0F0', linewidth=0.8, alpha=0.7)

    plt.tight_layout()

    target_folder = "D:\\pycharmproject\\MultiObjectiveOptimization\\FJSP_AO1\\gantt"
    filename = f"{title[:5]}-{max_end_time:.1f}-{line_filename}.png"
    full_path = os.path.join(target_folder, filename)
    plt.savefig(full_path, bbox_inches='tight', pad_inches=0.1)
    plt.close()


def lighten_color(color, factor=0.3):
    """
    将颜色变浅，使其看起来更舒适
    """
    import matplotlib.colors as mc
    import colorsys
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], 1 - factor * (1 - c[1]), c[2])


def calculate_stats(nested_list):
    """
    计算嵌套列表中每个子列表的最小值、最大值和平均值。

    Args:
        nested_list (list of list): 一个嵌套列表，每个子列表可能为空或包含数字。

    Returns:
        tuple: 包含以下统计信息的元组：
            - min_values (list): 每个子列表的最小值列表。
            - max_values (list): 每个子列表的最大值列表。
            - avg_values (list): 每个子列表的平均值列表。
    """
    # 过滤空子列表，计算统计信息
    min_values = [min(sublist) for sublist in nested_list if sublist]
    max_values = [max(sublist) for sublist in nested_list if sublist]
    avg_values = [sum(sublist) / len(sublist) for sublist in nested_list if sublist]

    # 返回统计结果
    return min_values, max_values, avg_values


def plot_objective_progress(objectives, title="Fitness Improvement for Objectives"):
    """
    绘制优化过程中目标值的变化图，包括最小值、最大值和平均值随迭代的变化。

    参数:
    objectives (list): 每次迭代中所有解的目标值列表。应该是一个二维列表，其中每一行代表一代的所有解的目标值。
    title (str): 图表的标题，默认为 "Fitness Improvement for Objectives"。

    返回:
    None
    """
    import matplotlib.pyplot as plot_objective

    # 计算目标值的统计信息：最小值、最大值、平均值
    min_values, max_values, avg_values = calculate_stats(objectives)

    # 生成横坐标，即迭代次数列表
    heng = list(range(1, len(objectives) + 1))

    # 创建一个新图表，设置图表大小为 10x6
    plot_objective.figure(figsize=(10, 6))

    # 绘制最小值、最大值和平均值的变化曲线
    plot_objective.plot(heng, min_values, marker="o", linestyle="-", label="min")  # 最小值
    plot_objective.plot(heng, max_values, marker="o", linestyle="-", label="max")  # 最大值
    plot_objective.plot(heng, avg_values, marker="o", linestyle="-", label="avg")  # 平均值

    # 设置图表的标题
    plot_objective.title(title)

    # 设置 x 轴标签为 "Iteration"（迭代次数）
    plot_objective.xlabel("Iteration")

    # 设置 y 轴标签为 "Fitness"（适应度）
    plot_objective.ylabel("Fitness")

    # 添加网格以便于观察数据趋势
    plot_objective.grid()

    # 添加图例，标题为 "Objectives"
    plot_objective.legend(title="Objectives")

    # 调整布局以确保图表不被截断
    plot_objective.tight_layout()

    # 显示图表
    # plot_objective.show()


def get_objs(solutions):
    result_objective1s = [solution.objectives[0] for solution in solutions]
    result_objective2s = [solution.objectives[1] for solution in solutions]
    result_objective3s = [solution.objectives[2] for solution in solutions]
    return result_objective1s, result_objective2s, result_objective3s


#
# def plot_pareto(solutions):
#     # 获取最终解集和pareto
#     pareto_front = get_non_dominated_front(solutions)
#     plot_pareto_frontier_3d(solutions, pareto_front)


def plot_pareto_frontier_3d(result, pareto_front, title="result pareto frontier", x_label="f_1", y_label="f_2",
                            z_label="f_3"):
    """
    绘制一个三维的帕累托前沿图，展示多目标优化问题中的解集。
    显示两个解集：一个是 **Pareto 前沿**（透明的蓝色小球），另一个是 **结果解集**（透明的红色圆球）。

    参数:
    result (list of solutions): 结果解集，每个解包含多个目标值。
    pareto_front (list of solutions): 帕累托前沿解集，每个解包含多个目标值。
    title (str): 图表标题，默认为 "3D Pareto Frontier"。
    x_label (str): x轴标签，默认为 "f_1"。
    y_label (str): y轴标签，默认为 "f_2"。
    z_label (str): z轴标签，默认为 "f_3"。

    返回:
    None: 该函数直接绘制图表，不返回任何值。
    """
    # 提取解集中每个解的目标值
    result_objective1s, result_objective2s, result_objective3s = get_objs(result)
    pareto_objective1s, pareto_objective2s, pareto_objective3s = get_objs(pareto_front)

    # 导入绘图所需的库
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    # 创建一个三维图表
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    # 绘制帕累托前沿（不那么透明的红色五角星）
    ax.scatter(pareto_objective1s, pareto_objective2s, pareto_objective3s, c='red', alpha=0.8, marker='*',
               label="Pareto Front")

    # 绘制结果解集（更透明的蓝色圆圈）
    if result_objective1s is not None and result_objective2s is not None and result_objective3s is not None:
        ax.scatter(result_objective1s, result_objective2s, result_objective3s, c='blue', alpha=0.3, marker='o',
                   label="Results (Transparent Spheres)")

    # 设置图表标题
    ax.set_title(title, fontsize=14)

    # 设置x轴、y轴和z轴的标签
    ax.set_xlabel(x_label, fontsize=12)
    ax.set_ylabel(y_label, fontsize=12)
    ax.set_zlabel(z_label, fontsize=12)

    # 调整视角以便更好地观察数据
    ax.view_init(elev=20, azim=135)

    # 添加图例
    ax.legend(title="Legend", fontsize=10)

    # 显示图表
    plt.tight_layout()
    # plt.show()


def plot_line(array1, flag1='First Elements of Array1', flag2='First Elements of Array2'):
    import matplotlib.pyplot as plt

    # 提取首元素数据
    data1 = [sub[0] for sub in array1]

    # 创建图形
    plt.figure(figsize=(10, 6))

    # 第一条线保持蓝色圆形
    plt.plot(data1,
             label=flag1,
             color='#2A5D8A',  # 深蓝色
             marker='o',
             markersize=8,
             linestyle='-',
             linewidth=2)

    # 样式增强
    plt.title('Trend Comparison',
              fontsize=14,
              fontweight='bold')
    plt.xlabel('Sequence Index',
               fontsize=12,
               labelpad=10)
    plt.ylabel('Element Value',
               fontsize=12,
               labelpad=10)

    # 高级图例设置
    plt.legend(
        loc='upper right',
        frameon=True,
        shadow=True,
        fontsize=10,
        title_fontsize='12'
    )

    # 专业网格样式
    plt.grid(
        True,
        linestyle=':',
        color='gray',
        alpha=0.6
    )

    # 自动调整边距
    plt.tight_layout()
    # plt.show()


def plot_iteration_process(filename1, filename2, filename3, filename4, filename5):
    import matplotlib.pyplot as plt
    # 读取文件（使用with语句自动关闭文件）
    with open(filename1, "r") as file1, \
            open(filename2, "r") as file2, \
            open(filename3, "r") as file3, \
            open(filename4, "r") as file4, \
            open(filename5, "r") as file5:
        # 读取所有行并提取第5行数据（索引4）
        data1 = file1.readlines()[4].strip().split(',')
        data2 = file2.readlines()[4].strip().split(',')
        data3 = file3.readlines()[4].strip().split(',')
        data4 = file4.readlines()[4].strip().split(',')
        data5 = file5.readlines()[4].strip().split(',')

    # 将字符串转换为浮点数列表
    y1 = [float(num) for num in data1]
    y2 = [float(num) for num in data2]
    y3 = [float(num) for num in data3]
    y4 = [float(num) for num in data4]
    y5 = [float(num) for num in data5]

    # 生成x轴坐标（取最长数据的长度）
    max_length = max(len(y1), len(y2))
    x = range(max_length)

    plt.figure(figsize=(8, 6), dpi=300)

    # 绘制所有数据（自动处理不同长度数据）
    plt.plot(x[:len(y1)], y1, label='MA', linewidth=2)
    plt.plot(x[:len(y2)], y2, label='MA-Alpha', linewidth=2)
    plt.plot(x[:len(y3)], y3, label='MA-Beta', linewidth=2)
    plt.plot(x[:len(y4)], y4, label='MA-Gamma', linewidth=2)
    plt.plot(x[:len(y5)], y5, label='EMA', linewidth=2)

    # 添加图表元素
    plt.xlabel('Index',
               fontsize=14,
               labelpad=10
               )
    plt.ylabel('Value',
               fontsize=14,
               labelpad=10
               )
    plt.title('Comparison of Data from Multiple Files',
              fontsize=14,
              fontweight='bold'
              )
    plt.legend(fontsize=12)
    plt.grid(True)

    # 显示图表
    plt.show()


if __name__ == '__main__':
    # filename1 = "D:\pycharmproject\MultiObjectiveOptimization\FJSP_AO1\Outcome\Outcome\BJS10_2195_NAGA-II_False-two-semi_active-100-0.7-0.2-111.21415185928345_c86b7214-311d-11f0-9e3d-b118d56b38fb.csv"
    # filename2 = "D:\pycharmproject\MultiObjectiveOptimization\FJSP_AO1\Outcome\Outcome\BJS10_2065_NAGA-II_False-two-active-100-0.7-0.2-123.30253171920776_9cfc2081-35fd-11f0-a2c4-82a4a3e1ac50.csv"
    # filename3 = "D:\pycharmproject\MultiObjectiveOptimization\FJSP_AO1\Outcome\Outcome\BJS10_2129_NAGA-II_True-two-semi_active-100-0.7-0.2-110.79968738555908_0d652e9a-3500-11f0-bc4c-82a4a3e1ac50.csv"
    # filename4 = "D:\pycharmproject\MultiObjectiveOptimization\FJSP_AO1\Outcome\Outcome\BJS10_2016_NAGA-II_True-two-active-100-0.7-0.2-118.19308471679688_3191a14c-3588-11f0-816e-82a4a3e1ac50.csv"
    # filename5 = "D:\pycharmproject\MultiObjectiveOptimization\FJSP_AO1\Outcome\Outcome\BJS10_2007_NAGA-II_True-two-active-100-0.7-0.2-116.93481683731079_daea17ed-3486-11f0-82f1-82a4a3e1ac50.csv"
    #
    # plot_iteration_process(filename1, filename2, filename3, filename4, filename5)
    temp_sequence = [211, 395, 70, 139, 91, 29, 417, 440, 58, 34, 247, 361, 276, 357, 243, 153, 25, 355, 239, 1, 309,
                     375, 451, 68, 435, 195, 102, 37, 169, 48, 316, 198, 36, 356, 418, 40, 138, 46, 52, 209, 363, 72,
                     207, 108, 129, 470, 485, 21, 187, 203, 90, 438, 39, 168, 494, 212, 317, 407, 264, 66, 109, 349,
                     373, 468, 399, 45, 130, 347, 302, 251, 179, 67, 157, 118, 255, 374, 189, 416, 409, 113, 328, 496,
                     119, 458, 86, 103, 383, 44, 125, 252, 358, 19, 80, 503, 314, 369, 163, 476, 87, 336, 181, 53, 49,
                     262, 31, 59, 194, 266, 406, 237, 413, 43, 446, 15, 359, 219, 74, 332, 17, 191, 436, 32, 465, 415,
                     241, 104, 429, 160, 271, 216, 54, 116, 51, 205, 448, 159, 174, 487, 26, 386, 152, 444, 283, 422,
                     430, 98, 162, 38, 392, 215, 180, 145, 197, 137, 326, 170, 245, 193, 437, 214, 223, 35, 206, 242,
                     300, 479, 61, 360, 24, 489, 466, 362, 165, 50, 261, 343, 493, 22, 6, 208, 62, 433, 344, 97, 439,
                     331, 419, 384, 30, 47, 353, 377, 492, 456, 442, 292, 3, 75, 41, 228, 23, 291, 454, 73, 412, 134,
                     321, 411, 10, 210, 171, 202, 89, 381, 185, 414, 57, 123, 431, 176, 350, 77, 11, 460, 234, 482, 389,
                     2, 155, 443, 405, 188, 65, 472, 114, 333, 93, 106, 110, 450, 449, 232, 452, 397, 338, 135, 495, 95,
                     76, 127, 256, 490, 270, 500, 258, 305, 346, 318, 28, 396, 20, 13, 14, 240, 505, 299, 478, 334, 55,
                     425, 339, 282, 281, 183, 71, 154, 388, 306, 250, 364, 111, 221, 428, 287, 167, 367, 131, 308, 4,
                     370, 307, 227, 289, 504, 382, 278, 126, 229, 192, 352, 161, 280, 136, 33, 297, 342, 447, 268, 184,
                     457, 337, 473, 310, 477, 178, 421, 105, 107, 8, 420, 378, 393, 96, 177, 394, 132, 368, 277, 408,
                     267, 225, 182, 60, 459, 201, 330, 273, 303, 288, 218, 294, 390, 231, 385, 133, 398, 238, 63, 380,
                     474, 81, 483, 269, 144, 235, 213, 204, 124, 296, 226, 263, 279, 259, 173, 79, 148, 455, 313, 272,
                     402, 122, 366, 424, 27, 324, 498, 293, 85, 400, 285, 469, 329, 84, 249, 445, 434, 453, 304, 112,
                     312, 323, 502, 284, 441, 335, 480, 18, 322, 16, 92, 481, 340, 172, 88, 423, 12, 220, 150, 371, 354,
                     461, 156, 376, 379, 175, 200, 257, 274, 463, 372, 391, 244, 69, 147, 224, 236, 141, 265, 121, 295,
                     471, 497, 199, 254, 115, 233, 499, 143, 99, 327, 151, 426, 82, 0, 56, 64, 230, 410, 186, 501, 7,
                     348, 164, 142, 100, 401, 387, 146, 491, 101, 248, 315, 246, 290, 462, 403, 149, 311, 404, 432, 319,
                     9, 365, 488, 345, 140, 196, 320, 158, 222, 286, 128, 260, 117, 166, 351, 83, 486, 484, 275, 325,
                     341, 78, 464, 217, 301, 467, 42, 253, 506, 475, 94, 298, 5, 190, 427, 120]

    machine_selection = [0, 0, 0, 3, 0, 3, 2, 3, 3, 1, 1, 0, 2, 0, 0, 0, 0, 3, 0, 3, 1, 0, 1, 2, 1, 0, 0, 1, 0, 2, 0, 3,
                         0, 1, 0, 0, 1, 1, 1, 0, 0, 2, 0, 1, 0, 4, 0, 0, 2, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 1, 0,
                         1, 3, 0, 0, 0, 1, 3, 2, 0, 0, 3, 2, 0, 1, 0, 1, 0, 0, 3, 1, 0, 0, 2, 3, 0, 0, 1, 0, 2, 0, 1, 1,
                         2, 2, 2, 1, 2, 4, 0, 1, 0, 0, 1, 0, 2, 0, 2, 1, 0, 3, 1, 0, 1, 0, 0, 0, 0, 0, 0, 2, 1, 1, 2, 1,
                         0, 0, 0, 2, 1, 2, 2, 2, 3, 0, 0, 2, 1, 1, 1, 0, 2, 0, 0, 1, 4, 1, 0, 2, 0, 0, 0, 1, 1, 0, 0, 1,
                         0, 1, 0, 2, 2, 0, 0, 0, 2, 0, 3, 1, 3, 3, 0, 1, 2, 1, 1, 0, 0, 0, 1, 0, 3, 2, 0, 1, 1, 0, 1, 2,
                         1, 1, 1, 1, 3, 0, 0, 0, 2, 1, 1, 0, 2, 0, 1, 0, 1, 1, 0, 3, 4, 1, 2, 2, 1, 0, 2, 1, 0, 0, 0, 3,
                         0, 3, 2, 1, 4, 0, 2, 1, 0, 1, 0, 0, 0, 0, 2, 2, 2, 3, 2, 0, 0, 0, 0, 1, 0, 2, 1, 3, 2, 1, 1, 0,
                         0, 1, 2, 1, 0, 0, 2, 0, 0, 0, 3, 1, 2, 0, 0, 0, 3, 0, 0, 2, 0, 0, 0, 2, 1, 1, 1, 2, 1, 0, 1, 3,
                         0, 0, 2, 3, 2, 0, 1, 1, 0, 0, 0, 3, 0, 2, 2, 3, 4, 1, 0, 1, 0, 0, 0, 0, 1, 1, 2, 1, 4, 1, 2, 0,
                         1, 0, 2, 1, 1, 0, 2, 2, 0, 3, 1, 2, 1, 2, 0, 1, 1, 2, 2, 1, 0, 0, 4, 0, 0, 1, 1, 0, 0, 0, 1, 2,
                         2, 4, 2, 0, 0, 2, 0, 1, 1, 0, 3, 0, 2, 1, 4, 1, 2, 1, 1, 0, 3, 0, 0, 0, 2, 4, 0, 2, 1, 2, 0, 0,
                         0, 1, 0, 0, 2, 4, 2, 0, 0, 0, 0, 2, 0, 0, 0, 3, 1, 0, 2, 2, 1, 1, 0, 0, 0, 0, 0, 2, 0, 2, 3, 0,
                         0, 0, 0, 1, 0, 1, 0, 3, 0, 2, 1, 1, 4, 2, 2, 1, 0, 1, 0, 1, 0, 0, 1, 3, 3, 0, 2, 2, 1, 2, 0, 3,
                         0, 1, 0, 1, 3, 2, 2, 0, 0, 0, 2, 1, 1, 0, 0, 0, 0, 1, 0, 0, 2, 2, 0, 0, 2, 0, 1, 0, 0, 0, 2, 1,
                         4, 4, 1, 0, 1, 1, 0, 3, 1, 2, 0, 2, 1, 1, 0, 0, 0, 1, 1, 2, 1, 1, 0, 0, 1, 0, 1]

    assembly_selection = [19, 18, 3, 34, 37, 21, 28, 29, 39, 20, 25, 0, 31, 4, 12, 36, 16, 5, 14, 7, 2, 33, 10, 11, 24,
                          6, 22, 38, 32, 30, 35, 27, 1, 17, 15, 26, 8, 23, 9, 13]

    jobs, machines, astyles, need_style, filename = large_Instance_paper1()
    decode = Decode(jobs, machines, astyles, need_style)
    decode.run_active_schedule(temp_sequence, machine_selection, assembly_selection)
    group, line_filename = plot_points_and_connections_by_jobs(decode.jobs)

    plot_gantt_chart(decode.jobs, decode.machines, group, 'large1', 'gantt chart')
    plt.show()