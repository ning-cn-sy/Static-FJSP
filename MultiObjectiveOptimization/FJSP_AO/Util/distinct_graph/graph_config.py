from copy import deepcopy
from typing import List

import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import FancyArrowPatch


class Node:
    """节点"""

    def __init__(self, id, name, op):
        self.id = id
        self.name = name
        self.s = 0
        self.t = 0
        self.op = op
        # self.style = style # 0:begin 1: 加工 2：装配


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

    def __init__(self, node1: Node, node2: Node, weight=0, name=None):
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
            ## 这里只考虑了 01_1,010_1这种情况，可能还会有O1_10这种，算例变大可能会有问题
            if len(self.nodes[i].name) == 4:  # 处理名称长度为 3 的节点
                second_char = self.nodes[i].name[1]
            else:
                second_char = self.nodes[i].name[1] + self.nodes[i].name[2]
            grouped_nodes.setdefault(second_char, []).append(self.nodes[i])

        # 为分组节点设置布局
        y_positions = np.linspace(0.5, -0.5, len(grouped_nodes))
        for i, (second_char, group) in enumerate(sorted(grouped_nodes.items())):
            group.sort(key=lambda x: x.name[-1])  # 按最后一个字符排序
            x_positions = np.linspace(-0.7,0.7, len(group))
            for x, node in zip(x_positions, group):
                pos[node] = (x, y_positions[i])

        # 绘图
        fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
        nx.draw_networkx_nodes(G, pos, ax=ax, node_size=900, node_color='white', edgecolors='black')
        nx.draw_networkx_labels(G, pos, ax=ax, labels=labels, font_size=10, font_color='black', font_weight='bold')

        # 绘制边，按类型分颜色与样式，并显示权重
        colors = ['black', 'red', 'green', 'skyblue', 'magenta', 'orange', 'gold', 'beige','blue',
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