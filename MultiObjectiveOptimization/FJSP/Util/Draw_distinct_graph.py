import random
import re
from copy import deepcopy
from enum import Enum
from typing import List, Dict

import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import FancyArrowPatch
from networkx import NetworkXError

from MultiObjectiveOptimization.FJSP.Config.Job import copy_job


class EdgeStyle(Enum):
    DISJUNCTIVE_ARC = "Disjunctive arc"
    CONNECTION_ARC = "Connection arc"


def select_node_by_random(path):
    filtered_nodes = [node for node in path if node.name != "Begin" and node.name != "End"]
    return random.choice(filtered_nodes)


def op_to_node(op, nodes):
    """
    根据操作（op）从节点列表中查找对应的节点。
    :param op: 操作对象，包含操作的名称信息。
    :param nodes: 节点列表。
    :return: 与操作名称匹配的节点对象，如果未找到，返回 None。
    """
    for node in nodes:
        if op.get_name() == node.name:  # 判断操作的名称是否与节点名称匹配
            return node


def get_nodes_edges(jobs):
    """
    根据作业调度信息生成节点和边的结构。
    :param jobs: 作业列表，每个作业包含多个操作（ops）。
    :return: 包含节点列表和边列表的元组。
    """
    nodes = []  # 存储所有节点
    edges = []  # 存储所有边
    # 创建起始节点和结束节点
    node_begin = Node(0, 'Begin', None)  # 起始节点
    node_end = Node(9999, 'End', None)  # 结束节点
    nodes.append(node_begin)  # 将起始节点加入节点列表

    machine_to_op: Dict[int, list] = {}  # 按机器编号分类操作
    i = 1  # 节点编号计数器

    # 遍历每个作业
    for job in jobs:
        for op in job.ops:
            # 创建节点并将其加入节点列表
            node_name = op.get_name()  # 获取操作名称
            edge_name = 'Connection arc'  # 设置边的名称
            nodes.append(Node(i, node_name, op))  # 创建节点对象并加入列表

            # 如果是第一道工序，与起始节点相连
            if op.op_id == 1:
                edges.append(Edge(node_begin, Node(i, node_name, op), job.release_time, edge_name))

            # 如果是中间工序，与上一道工序相连
            else:
                prev_op = job.ops[op.op_id - 2]  # 获取上一道工序
                edges.append(Edge(nodes[i - 1], Node(i, node_name, op),
                                  prev_op.end_time - prev_op.start_time, edge_name))

            # 如果是最后一道工序，与结束节点相连
            if op.op_id == len(job.ops):
                edges.append(
                    Edge(Node(i, node_name, op), node_end, op.end_time - op.start_time, edge_name))

            # 根据机器编号将操作分类存储
            if op.to_machine not in machine_to_op:
                machine_to_op[op.to_machine] = []  # 初始化机器编号对应的操作列表
            machine_to_op[op.to_machine].append(op)  # 将操作加入对应机器的列表
            i = i + 1  # 更新节点计数器

    # 为每台机器绘制弧（按操作开始时间排序）
    for machine in machine_to_op:
        # 获取当前机器的所有操作，并按开始时间排序
        ops_list = sorted(machine_to_op[machine], key=lambda op: op.start_time)
        node_name = f'M{machine} Disjunctive arc'  # 机器弧的名称

        # 起点连接到机器的第一个操作 0机器的最早可用时间
        edges.append(Edge(node_begin, op_to_node(ops_list[0], nodes), 0, node_name))

        # 依次连接操作
        for j in range(0, len(ops_list) - 1):
            edges.append(Edge(op_to_node(ops_list[j], nodes), op_to_node(ops_list[j + 1], nodes),
                              ops_list[j].end_time - ops_list[j].start_time,
                              node_name))

        # 最后一操作连接到结束节点
        machine_lastop = ops_list[len(ops_list) - 1]  # 获取机器的最后一个操作
        edges.append(
            Edge(op_to_node(machine_lastop, nodes), node_end,
                 machine_lastop.end_time - machine_lastop.start_time, node_name))

    # 将结束节点加入节点列表
    nodes.append(node_end)

    # 返回节点和边的列表
    return nodes, edges


class Node:
    """节点"""

    def __init__(self, id, name, op):
        self.id = id
        self.name = name
        self.s = 0
        self.t = 0
        self.op = op

    def __repr__(self):
        # return f"Node({self.id})"
        return self.name

    def __eq__(self, other):
        return isinstance(other, Node) and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f'{self.name}'


class Edge:
    """边"""

    def __init__(self, node1: Node, node2: Node, weight, name):
        self.node1 = node1
        self.node2 = node2
        self.weight = weight
        self.name = name

    def __str__(self):
        return f'{self.node1.name}  {self.node2.name}'

    # def __eq__(self, other):
    #     if isinstance(other, Edge):
    #         return self.id == other.id
    def __eq__(self, other):
        return isinstance(other,
                          Edge) and self.node1 == other.node1 and self.node2 == other.node2 and self.name == other.name

    def has_node(self, node):
        return (self.node1 == node or self.node2 == node) and "Disjunctive arc" in self.name


class graph:
    """
    一个用于表示图的类，支持节点与边的添加、删除，以及基于图的各种操作，例如：
    - 最长路径计算
    - 最短路径计算
    - 环检测与处理
    - 图的绘制
    - 删除特定类型的边
    图是基于 NetworkX 的有向图实现的。
    """

    def __init__(self, nodes: List[Node], edges: List[Edge]):
        """
        初始化图对象。
        :param nodes: 图中的节点列表。
        :param edges: 图中的边列表。
        """
        self.nodes = nodes  # 节点列表
        self.edges = edges  # 边列表
        self.graph = self._get_graph()  # 构建 NetworkX 图

    def find_edge_index(self, u, v):
        """
        查找从节点 u 到节点 v 的边的索引。
        :param u: 起点节点。
        :param v: 终点节点。
        :return: 边的索引（如果找到），否则返回 None。
        """
        for index, edge in enumerate(self.edges):
            if edge.node1 == u and edge.node2 == v:
                return index
        return None

    def remove_edges(self, edges_to_remove):
        """
        从图中删除指定的边，根据节点和边的属性（如 'name'）。
        :param edges_to_remove: 要删除的边列表，边对象应包含节点和名称属性。
        """
        for edge1 in edges_to_remove:
            for key, edge_data in self.graph[edge1.node1][edge1.node2].items():  # 获取两节点间所有边
                # 检查边的节点和属性是否匹配
                if edge_data.get('name') == edge1.name:
                    self.graph.remove_edge(edge1.node1, edge1.node2, key=key)  # 仅删除匹配的边
                    print(f"Edge between {edge1.node1} and {edge1.node2} with name '{edge1.name}' removed.")
                    break  # 找到并删除匹配的边后跳出循环
            # 从边列表中移除边
            self.edges.remove(edge1)

    def add_edges(self, edges_to_remove):
        """
        删多了，在连一条
        在edge里删掉
        还要再graph图里删掉
        """
        edge1 = edges_to_remove[0]
        edge2 = edges_to_remove[1]
        new_edge = Edge(name=edge1.name, node1=edge1.node1, node2=edge2.node2, weight=edge1.weight)
        self.edges.append(new_edge)
        ### 下面这个可能有问题
        self.graph.add_edge(edge1.node1, edge2.node2, weight=edge1.weight, name=edge1.name)

    def _get_graph(self):
        """
        根据节点和边构建一个 NetworkX 有向图。
        :return: 构建的 NetworkX 图对象。
        """
        G = nx.MultiDiGraph()
        # G = nx.DiGraph()
        for node in self.nodes:
            G.add_node(node)  # 添加节点
        for edge in self.edges:
            G.add_edge(edge.node1, edge.node2, weight=edge.weight, name=edge.name)  # 添加带权重和名称的边
        return G

    def find_and_print_cycles(self):
        """
        检测图中的环并打印。
        如果没有环，则打印消息提示继续执行其他操作。
        """
        try:
            cycles = nx.find_cycle(self.graph, orientation="original")  # 检测环
            print("检测到的环：")
            for u, v, direction in cycles:
                edge_index = self.find_edge_index(u, v)
                print(f"{u} -> {v} (方向: {direction}, 索引: {edge_index})")
        except nx.NetworkXNoCycle:
            print("图中没有环，继续执行其他操作。")

    def remove_machine_arcs_by_node(self, selected_node, a, if_print=True):
        """
        随机从路径中选择一个节点，删除所有与该节点相关的 machine arc 类型的边。
        :param selected_node: 所选节点。
        :return: 更新后的图对象。
        @param if_print:
        """
        # new_graph = graph(nodes=self.nodes, edges=self.edges)
        new_graph = deepcopy(a)
        edges_to_remove = [edge for edge in new_graph.edges if edge.has_node(selected_node)]
        if if_print:
            print("----------------点----------------")
            print(selected_node)
            print("-----------删除了如下边-----------")
            print("\n".join(map(str, edges_to_remove)))
            print("---------------over---------------")
        new_graph.remove_edges(edges_to_remove)
        new_graph.add_edges(edges_to_remove)
        return new_graph

    def longest_path(self, if_print=False):
        """
        计算无环图的最长路径及其长度。
        :param if_print: 是否打印路径信息。
        :return: 最长路径的节点列表、路径上的边及长度。
        """
        try:
            # 计算最长路径
            path = nx.dag_longest_path(self.graph, weight="weight")
            length = nx.dag_longest_path_length(self.graph, weight="weight")

            # 获取路径上的边及其权重，注意要考虑多条边的情况
            edges_ = []
            for i in range(len(path) - 1):
                # 获取所有从path[i]到path[i+1]的边，并选取其中权重最大的边
                edges_data = self.graph[path[i]][path[i + 1]]
                max_edge = max(edges_data, key=lambda edge: edges_data[edge]["weight"])
                edges_.append((path[i], path[i + 1], edges_data[max_edge]["weight"]))

            # 如果需要打印
            if if_print:
                print("\n", path, "\n", edges_, "\n", length)

            return path, edges_, length

        except nx.NetworkXUnfeasible:
            self.find_and_print_cycles()
            raise ValueError("图中存在环，不能直接计算最长路径！")

    def longest_path_between_two_nodes(self, node1, node2):
        """
        计算从节点 node1 到节点 node2 的最长路径及其涉及的边。
        :param node1: 起点节点。
        :param node2: 终点节点。
        :return: 最长路径的节点列表、路径上的边及长度。
        """
        try:
            # 检查起点和终点是否存在于图中
            if node1 not in self.graph.nodes or node2 not in self.graph.nodes:
                raise ValueError("起点或终点不在图中！")

            # 检查是否存在从 node1 到 node2 的路径
            if not nx.has_path(self.graph, source=node1, target=node2):
                raise ValueError(f"从 {node1} 到 {node2} 没有路径！")

            # 使用自定义深度优先搜索找到从 node1 到 node2 的所有路径
            all_paths = list(nx.all_simple_paths(self.graph, source=node1, target=node2))
            if len(all_paths) == 0:
                return []

            # 计算每条路径的总权重，并找到权重最大的路径
            max_length = float('-inf')
            longest_path = None
            for path in all_paths:
                path_length = 0
                for i in range(len(path) - 1):
                    # 获取所有从path[i]到path[i+1]的边
                    edges_data = self.graph[path[i]][path[i + 1]]

                    # 确保每条边有 "weight" 属性
                    if not all("weight" in edge for edge in edges_data.values()):
                        raise ValueError(f"某些边从 {path[i]} 到 {path[i + 1]} 没有 'weight' 属性！")

                    # 选择权重最大的边
                    max_edge = max(edges_data.values(), key=lambda edge: edge["weight"])
                    path_length += max_edge["weight"]

                if path_length > max_length:
                    max_length = path_length
                    longest_path = path

            return max_length

        except Exception as e:
            raise ValueError(f"发生错误：{e}")

    def shortest_path(self, source: Node, target: Node):
        """
        计算从 source 到 target 的最短路径及其长度。
        :param source: 起点节点。
        :param target: 终点节点。
        :return: 最短路径及其长度。
        """
        path = nx.shortest_path(self.graph, source=source, target=target, weight="weight")
        length = nx.shortest_path_length(self.graph, source=source, target=target, weight="weight")
        return path, length

    def draw_network(self):
        """
        绘制图的可视化表示。
        - 节点分组布局（按节点名称分组）。
        - 使用不同颜色表示不同类型的边。
        - 在线的中点位置显示权重。
        """
        G = self.graph
        labels = {node: node.name for node in G.nodes()}  # 节点标签
        pos = {}
        pos[self.nodes[0]] = (-1, 0)  # 起始节点布局
        pos[self.nodes[-1]] = (1, 0)  # 结束节点布局

        # 分组节点，按名称的第二个字符分组
        grouped_nodes = {}
        for i in range(1, len(self.nodes) - 1):
            if len(self.nodes[i].name) == 3:  # 处理名称长度为 3 的节点
                second_char = self.nodes[i].name[1]
            else:
                second_char = self.nodes[i].name[1] + self.nodes[i].name[2]
            grouped_nodes.setdefault(second_char, []).append(self.nodes[i])

        # 为分组节点设置布局
        y_positions = np.linspace(0.5, -0.5, len(grouped_nodes))
        for i, (second_char, group) in enumerate(sorted(grouped_nodes.items())):
            group.sort(key=lambda x: x.name[-1])  # 按最后一个字符排序
            x_positions = np.linspace(-0.5, 0.5, len(group))
            for x, node in zip(x_positions, group):
                pos[node] = (x, y_positions[i])

        # 绘图
        fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
        nx.draw_networkx_nodes(G, pos, ax=ax, node_size=900, node_color='white', edgecolors='black')
        nx.draw_networkx_labels(G, pos, ax=ax, labels=labels, font_size=10, font_color='black', font_weight='bold')

        # 绘制边，按类型分颜色与样式，并显示权重
        colors = ['black', 'red', 'green', 'skyblue', 'magenta', 'orange', 'yellow', 'blue',
                  'pink', 'purple', 'brown', 'gray', 'white', 'beige', 'lavender', 'turquoise',
                  'violet', 'gold', 'silver', 'cyan']
        arc_names = []
        j = -1
        for edge in self.edges:
            u, v = edge.node1, edge.node2
            if edge.name not in arc_names:
                j += 1
                arc_names.append(edge.name)
                # color = colors[j % len(colors)]
                color = colors[j]
            else:
                color = colors[arc_names.index(edge.name)]
            style = 'solid' if edge.name == 'Connection arc' else 'dotted'
            rad = 0 if edge.name == 'Connection arc' else 0.2

            # 添加边的绘制
            arrow = FancyArrowPatch(
                posA=pos[u],
                posB=pos[v],
                connectionstyle=f'arc3,rad={rad}',
                color=color,
                linestyle=style,
                arrowstyle='-|>',
                mutation_scale=30,
                lw=2,
            )
            ax.add_patch(arrow)

            # 计算边标签的显示位置（中点 + 偏移）
            mid_x = (pos[u][0] + pos[v][0]) / 2
            mid_y = (pos[u][1] + pos[v][1]) / 2
            edge_vector = (pos[v][0] - pos[u][0], pos[v][1] - pos[u][1])  # 边的方向向量
            length = (edge_vector[0] ** 2 + edge_vector[1] ** 2) ** 0.5  # 边的长度
            direction_vector = (edge_vector[0] / length, edge_vector[1] / length)  # 单位方向向量
            offset_distance = 0.05  # 偏移距离，避免与边重叠
            label_pos_x = mid_x + offset_distance * direction_vector[1]  # 偏移到垂直方向
            label_pos_y = mid_y - offset_distance * direction_vector[0]

            # 显示权重和名称
            weight_text = f"{edge.weight}"
            ax.text(label_pos_x, label_pos_y, weight_text, fontsize=10, color=color)

        plt.title("Disjunctive graph")
        plt.axis('off')
        plt.show()

    def get_Rk_Lk(self, selected_node, select_machine, nodes):
        Qk_list = []
        for node in nodes:
            if node.op != None and node != selected_node:
                if node.op.to_machine == select_machine[0]:
                    Qk_list.append(node)
        Qk = sorted(Qk_list, key=lambda x: x.op.start_time)
        Rk = []
        Lk = []
        for node in Qk:
            if node.s + (node.op.end_time - node.op.start_time) > selected_node.s:
                Rk.append(node)
            if node.t + (node.op.end_time - node.op.start_time) > selected_node.t:
                Lk.append(node)

        return Rk, Lk, Qk

    def insert_op(self, selected_node, Rk, Lk, Qk, G_, select_machine, G):
        if set(Rk) & set(Lk):
            before_position = list(set(Rk) - set(Lk))
            after_position = list(set(Lk) - set(Rk))
        else:
            before_position = Rk
            after_position = Lk
        if len(before_position) != 0 and len(after_position) != 0:
            G_new = insert_(selected_node, before_position, after_position, Qk, G_, select_machine)
        else:
            # print("没有合适插入位置")
            G_new = deepcopy(G)
        return G_new


def insert_(selected_node, before_position, after_position, Qk, G_, select_machine):
    G_new = deepcopy(G_)
    index = random.randint(len(after_position) - 1, len(Qk) - len(before_position) - 1)
    # print(f"{selected_node.name}插入到{Qk[index].name}和{Qk[index + 1].name}之间")
    edge_name = f'M{Qk[index].op.to_machine} Disjunctive arc'
    to_remove_edge = Edge(Qk[index], Qk[index + 1], Qk[index].op.end_time - Qk[index].op.start_time, edge_name)
    G_new.edges.remove(to_remove_edge)
    # tuple_dict = dict(selected_node.op.available_machines)
    # duration = tuple_dict.get(Qk[index].op.to_machine, None)
    duration = select_machine[1]
    G_new.edges.append(Edge(Qk[index], selected_node, Qk[index].op.end_time - Qk[index].op.start_time, edge_name))
    G_new.edges.append(Edge(selected_node, Qk[index + 1], duration, edge_name))
    # 接下来从graph里删边，加边
    for key, edge_data in G_new.graph[Qk[index]][Qk[index + 1]].items():  # 获取两节点间所有边
        # 检查边的节点和属性是否匹配
        if edge_data.get('name') == to_remove_edge.name:
            G_new.graph.remove_edge(to_remove_edge.node1, to_remove_edge.node2, key=key)  # 仅删除匹配的边
            # print(
            #     f"Edge between {to_remove_edge.node1} and {to_remove_edge.node2} with name '{to_remove_edge.name}' removed.")
            break  # 找到并删除匹配的边后跳出循环
    G_new.graph.add_edge(Qk[index], selected_node, weight=Qk[index].op.end_time - Qk[index].op.start_time,
                         name=edge_name)
    G_new.graph.add_edge(selected_node, Qk[index + 1], weight=duration, name=edge_name)
    return G_new


def get_new_jobs(jobs, G_new):
    new_jobs = []
    for job in jobs:
        new_jobs.append(copy_job(job))
    for job in new_jobs:
        for op in job.ops:
            # 对应的边
            op.start_time, op.end_time, op.to_machine = find_edge(op, G_new)
    return new_jobs


def find_edge(op, G_new):
    start_time = 0
    duration = 0
    to_machine = 0
    for edge in G_new.edges:
        if edge.node1.op == op:
            # 此时的头长度还没更新，不能用 .s
            # start_time_list.append(edge.node1.s)
            start_time = G_new.longest_path_between_two_nodes(Node(0, 'Begin', None), edge.node1)
            if edge.name == 'Connection arc':
                duration = edge.weight
            else:
                to_machine = int(edge.name[1])
    return start_time, start_time + duration, to_machine

# def copy_gragh(a):
#     b.deepcopy()
#     return b
