import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os
import uuid

from MultiObjectiveOptimization.FJSP_AO.Config.Job import Job
from MultiObjectiveOptimization.FJSP_AO.Config.Operation import Machining_operation


# 定义 Point 类
class Point:
    def __init__(self, name, type, row, top="", bottom=""):
        """
        初始化 Point 对象。

        Args:
            name (str): 点的名称，用于唯一标识。
            type (str): 点的类型，例如 "circle" 或 "triangle"。
            row (int): 点所在的行号。
            top (str): 点上方的文字。
            bottom (str): 点下方的文字。
        """
        self.name = name
        self.type = type
        self.row = row
        self.top = top
        self.bottom = bottom
        self.connections = []  # 存储与其他点的连接关系

    def connect_to(self, other):
        """
        添加与其他点的连线关系。

        Args:
            other (Point): 要连接的目标点。
        """
        self.connections.append(other)

    def __eq__(self, other):
        return self.name == other.name


def plot_points_and_connections_with_labels(points, row_labels, start_y=90, y_gap=5.5, x_gap=40, radius=0.7):
    fig, ax = plt.subplots(figsize=(16, 9))

    # 1. 为每个点生成唯一ID
    point_id_map = {}
    for idx, point in enumerate(points):
        unique_id = f"{point.name}_{point.row}_{idx}"
        point.unique_id = unique_id
        point_id_map[point.name] = unique_id  # 保留名称映射

    # 2. 按行组织点
    rows = {}
    for point in points:
        if point.row not in rows:
            rows[point.row] = []
        rows[point.row].append(point)

    # 3. 计算坐标 (修复点坐标被覆盖的问题)
    # 3. 计算坐标 - 修改为左端对齐
    points_pos = {}
    max_points_in_row = max(len(row_points) for row_points in rows.values())

    # 计算最大宽度（用于设置图形边界）
    max_width = max_points_in_row * x_gap

    for row, row_points in rows.items():
        y = start_y - (row - 1) * y_gap

        # 添加行左侧标注（保持不变）
        if row in row_labels:
            ax.text(-5, y, row_labels[row], ha="right", va="center", fontsize=10, color="black")

        # 关键修改：所有行都从0开始绘制（左对齐）
        start_x = 0

        for i, point in enumerate(row_points):
            x = start_x + i * x_gap
            points_pos[point.unique_id] = (x, y)

    # 4. 绘制点
    for point in points:
        pos = points_pos[point.unique_id]
        if point.type == "circle":
            circle = patches.Circle(pos, radius=radius, edgecolor='black', facecolor='white', lw=2)
            ax.add_patch(circle)
        elif point.type == "triangle":
            x, y = pos
            triangle = patches.Polygon(
                [(x, y + 0.6), (x - 0.5, y - 0.6), (x + 0.5, y - 0.6)],
                edgecolor='black', facecolor='white', lw=2
            )
            ax.add_patch(triangle)

        # 添加文字
        if point.top:
            ax.text(pos[0], pos[1] + 2, point.top, ha="center", va="center", fontsize=8)
        if point.bottom:
            ax.text(pos[0], pos[1] - 2, point.bottom, ha="center", va="center", fontsize=8)

    # 5. 绘制连线（修复连线问题）
    for point in points:
        for connected_point in point.connections:
            # 通过名称映射找到正确的唯一ID
            target_id = point_id_map.get(connected_point.name)

            if not target_id or target_id not in points_pos:
                print(f"警告：无法找到点 {connected_point.name} 的坐标")
                continue

            start_pos = points_pos[point.unique_id]
            end_pos = points_pos[target_id]

            # 直接连接中心点（简化逻辑）
            ax.plot([start_pos[0], end_pos[0]], [start_pos[1], end_pos[1]],
                    color='black', lw=2)

    # 6. 设置坐标系范围 - 修改边界设置
    ax.set_xlim(-10, max_width + 10)
    min_y = min(pos[1] for pos in points_pos.values())
    ax.set_ylim(min_y - 10, start_y + 10)
    ax.axis('off')


def plot_points_and_connections_by_jobs(jobs: [Job]):
    # 1. 在绘图前设置字体嵌入配置（防止中文乱码）
    plt.rcParams['font.family'] = 'SimHei'  # Windows中文字体
    plt.rcParams['pdf.fonttype'] = 42  # 嵌入TrueType字体
    plt.rcParams['ps.fonttype'] = 42  # 嵌入TrueType字体

    points = []
    row_labels = {}
    row = 1

    # 定义装配分组
    assembly_groups = {
        1: [1, 2, 3],  # 分组1：style 1, 2, 3
        2: [4, 5],  # 分组2：style 4, 5
        3: [6, 7]  # 分组3：style 6, 7
    }

    # 用于记录特殊节点
    nodes_by_job = {}

    # 分组工件
    grouped_jobs = {}
    # 保存每个组的工件
    index = 1
    for job in jobs:
        Flag = False
        for key in grouped_jobs:
            if job in grouped_jobs[key]:
                Flag = True
                continue
        if Flag:
            continue
        grouped_jobs[index] = job.assembly_jobs
        index += 1

    # # print(grouped_jobs[1][0].id)
    # for group_id, group_styles in assembly_groups.items():
    #     grouped_jobs[group_id] = [job for job in jobs if job.origin_style.value in group_styles]

    # 按分组绘制工件
    for group_id, group_jobs in grouped_jobs.items():
        job_style = []
        # group_jobs_ = sorted(
        #     group_jobs,
        #     key=lambda job: (job.get_assembly_op_num(), len(job.ops))
        # )
        group_jobs_ = sorted(
            group_jobs, key=lambda job: int(job.origin_style.name.replace('style', ''))
        )
        for job in group_jobs_:
            # i = 0
            job_style.append(job.origin_style.value)

            job_points = []  # 当前工件的所有点
            for op in job.ops:
                # 根据操作类型确定节点类型
                type_ = "circle" if isinstance(op, Machining_operation) else "triangle"
                if type_ == "circle":
                    name = f"O{job.id},{op.op_id}"
                else:
                    # i += 1
                    name = f"{op.assemble_style.name} {group_id}"

                # 创建节点
                point = Point(name=name, type=type_, row=row, top=name)

                # if op.to_machine < 0:
                #     continue  # 跳过无效机器

                job_points.append(point)  # 添加当前工件点
                if point not in points:
                    points.append(point)  # 添加到全局点列表

            # 连接工件内部的点
            for x in range(len(job_points) - 1):
                job_points[x].connect_to(job_points[x + 1])

                # 保存当前工件的点信息
            nodes_by_job[job.id] = job_points
            # 保存当前工件的点信息
            nodes_by_job[job.id] = job_points
            # 添加行标签
            row_labels[row] = f"job{job.id}  {job.origin_style.name}"
            row += 1
            # plot_points_and_connections_with_labels(points=points, row_labels=row_labels)
            # print()
        # 每个分组绘制完后插入分隔符
        # row_labels[row] = f"Group {group_id} Separator"
        row += 1

    # 绘制图形
    plot_points_and_connections_with_labels(points=points, row_labels=row_labels)
    target_folder = r"D:\pycharmproject\MultiObjectiveOptimization\FJSP_AO1\line"
    unique_id = uuid.uuid1()

    # 2. 保存为矢量图（PDF或SVG）
    # 选项1: 保存为PDF
    filename = f"large-{unique_id}.pdf"
    full_path = os.path.join(target_folder, filename)
    plt.savefig(full_path, format='pdf', bbox_inches='tight')
    plt.close()
    return grouped_jobs, filename
