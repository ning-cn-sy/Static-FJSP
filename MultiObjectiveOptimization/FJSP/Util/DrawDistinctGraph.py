from typing import List

import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import FancyArrowPatch


class Node:
    """节点"""

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        # return f"Node({self.id})"
        return self.name

    def __eq__(self, other):
        return isinstance(other, Node) and self.id == other.id

    def __hash__(self):
        return hash(self.id)


class Edge:
    """边"""

    def __init__(self, node1: Node, node2: Node, weight, name):
        self.node1 = node1
        self.node2 = node2
        self.weight = weight
        self.name = name

    # def __eq__(self, other):
    #     if isinstance(other, Edge):
    #         return self.id == other.id


class graph:
    def __init__(self, nodes: List[Node], edges: List[Edge]):
        self.nodes = nodes
        self.edges = edges
        self.graph = self._get_graph()

    def _get_graph(self):
        G = nx.DiGraph()
        for node in self.nodes:
            G.add_node(node)
        for edge in self.edges:
            G.add_edge(edge.node1, edge.node2, weight=edge.weight)
        return G

    def draw_network(self):
        G = self.graph
        labels = {node: node.name for node in G.nodes()}
        pos = {}
        pos[self.nodes[0]] = (-1, 0)
        pos[self.nodes[len(self.nodes) - 1]] = (1, 0)

        # 将其他节点分组并排列 这里也得考虑有的o101多一位的name
        grouped_nodes = {}
        # 遍历除begin end的节点
        # 根据name的第二个字符分组，第二个字符就是job id - O11 - 1
        for i in range(1, len(self.nodes) - 1):
            if len(self.nodes[i].name) == 3:
                second_char = self.nodes[i].name[1]
                if second_char not in grouped_nodes:
                    grouped_nodes[second_char] = []
                grouped_nodes[second_char].append(self.nodes[i])
            else:
                second_char = self.nodes[i].name[1] + self.nodes[i].name[2]
                if second_char not in grouped_nodes:
                    grouped_nodes[second_char] = []
                grouped_nodes[second_char].append(self.nodes[i])
        # 按照第二个字符进行分组后，按第三个字符排序
        y_positions = np.linspace(0.5, -0.5, len(grouped_nodes))  # y轴从上到下排列
        for i, (second_char, group) in enumerate(sorted(grouped_nodes.items())):
            group.sort(key=lambda x: x.name[len(x.name) - 1])  # 按第三个字符排序 按最后一个排序
            x_positions = np.linspace(-0.5, 0.5, len(group))  # x方向从左到右排列
            for x, node in zip(x_positions, group):
                pos[node] = (x, y_positions[i])

        fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
        nx.draw_networkx_nodes(G, pos, ax=ax, node_size=900, node_color='white', edgecolors='black')
        nx.draw_networkx_labels(G, pos, ax=ax, labels=labels, font_size=10, font_color='black', font_weight='bold')
        colors = ['black', 'red', 'green', 'skyblue', 'magenta', 'orange', 'pink', 'pink', 'purple', 'brown', 'lime',
                  'olive', 'navy', 'teal', 'gold', 'salmon']
        arc_names = []
        j = -1
        for i in range(len(self.edges)):
            u = self.edges[i].node1
            v = self.edges[i].node2
            # color = 'black' if edge.name == 'Connection arc' else 'red'
            if self.edges[i].name not in arc_names:
                j += 1
                color = colors[j]
                arc_names.append(self.edges[i].name)
            style = 'solid' if self.edges[i].name == 'Connection arc' else 'dotted'
            # 这个是画弧，还可以画角度
            rad = 0 if self.edges[i].name == 'Connection arc' else 0.2
            # arrowstyles = ['-', '-|', '-|>', '<-', '<|-', '<|-|>', '|-|>', '->', 'fancy', 'simple', 'wedge', '[', ']']
            arrow = FancyArrowPatch(posA=pos[u], posB=pos[v],
                                    connectionstyle=f'arc3,rad={rad}',
                                    # connectionstyle='angle3, angleA=89, angleB=90',
                                    color=color,
                                    linestyle=style,
                                    arrowstyle='-|>',
                                    mutation_scale=30,
                                    lw=2)
            ax.add_patch(arrow)

            # 边上标签的位置 怎么放
            mid_x = (pos[u][0] + pos[v][0]) / 2
            mid_y = (pos[u][1] + pos[v][1]) / 2
            # 计算边的方向向量
            edge_vector = (pos[v][0] - pos[u][0], pos[v][1] - pos[u][1])
            length = (edge_vector[0] ** 2 + edge_vector[1] ** 2) ** 0.5
            direction_vector = (edge_vector[0] / length, edge_vector[1] / length)
            offset_distance = 0.05  # 调整偏移距离，避免与边重叠
            label_pos_x = mid_x + offset_distance * direction_vector[1]  # 偏移到垂直方向
            label_pos_y = mid_y - offset_distance * direction_vector[0]

            if self.edges[i].name == 'Connection arc':
                ax.text(label_pos_x, label_pos_y, f"{self.edges[i].weight}", fontsize=12,
                        color=color)
            else:
                ax.text(label_pos_x, label_pos_y, f"{self.edges[i].weight} M{self.edges[i].name[1]}", fontsize=12,
                        color=color)
        plt.title("Disjunctive graph")
        plt.axis('off')
        plt.show()

    def longest_path(self):
        """计算无环图的最长路径及其长度，同时返回路径上的边"""
        try:
            # 获取最长路径的节点序列
            path = nx.dag_longest_path(self.graph, weight="weight")
            # 计算路径的总长度
            length = nx.dag_longest_path_length(self.graph, weight="weight")
            # 提取路径上的边及其权重
            edges_ = [
                (path[i], path[i + 1], self.graph[path[i]][path[i + 1]]["weight"])
                for i in range(len(path) - 1)
            ]
            return path, edges_, length
        except nx.NetworkXUnfeasible:
            raise ValueError("图中存在环，不能直接计算最长路径！")

    def shortest_path(self, source: Node, target: Node):
        """计算从 source 到 target 的最短路径及其长度"""
        path = nx.shortest_path(self.graph, source=source, target=target, weight="weight")
        length = nx.shortest_path_length(self.graph, source=source, target=target, weight="weight")
        return path, length
