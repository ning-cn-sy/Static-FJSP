import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from networkx import circular_layout


class Disjunctive_graph:
    def __init__(self, nodes: [], edges: [], machine_edges: [], am_edges: []):
        self.nodes = nodes
        self.edges = edges
        self.machine_edges = machine_edges
        self.am_edges = am_edges

    def draw(self):
        edges = self.edges
        last_op = {}
        for node in self.nodes:
            job_id = node[1]
            op_id = node[2]
            if node[2] == "1":
                edges.append(("begin", node))
            if job_id not in last_op or op_id > last_op[job_id][0]:
                last_op[job_id] = (op_id, node)
        for last_node in last_op.values():
            edges.append((last_node[1], "end"))
        # 创建一个有向图
        G = nx.DiGraph()

        # 添加节点和边
        G.add_nodes_from(self.nodes)
        G.add_edges_from(edges + self.machine_edges + self.am_edges)

        # 定义自定义布局
        pos = {}
        pos['begin'] = (-1, 0)  # 左侧
        pos['end'] = (1, 0)  # 右侧

        # 将其他节点分组并排列
        grouped_nodes = {}
        for node in self.nodes:
            second_char = node[1]
            if second_char not in grouped_nodes:
                grouped_nodes[second_char] = []
            grouped_nodes[second_char].append(node)

        # 按照第二个字符进行分组，并按第三个字符排序
        y_positions = np.linspace(0.5, -0.5, len(grouped_nodes))  # y轴从上到下排列
        for i, (second_char, group) in enumerate(sorted(grouped_nodes.items())):
            group.sort(key=lambda x: x[2])  # 按第三个字符排序
            x_positions = np.linspace(-0.5, 0.5, len(group))  # x轴从左到右排列
            for x, node in zip(x_positions, group):
                pos[node] = (x, y_positions[i])

        edge_colors = []
        edge_styles = []
        for edge in G.edges():
            if edge in self.edges:
                edge_colors.append('blue')
                edge_styles.append('solid')
            elif edge in self.machine_edges:
                edge_colors.append('green')
                edge_styles.append('dotted')
            elif edge in self.am_edges:
                edge_colors.append('red')
                edge_styles.append('dashed')

        # 绘制图
        nx.draw(G, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=15, font_color='black',
                font_weight='bold', arrowsize=20, edge_color=edge_colors, style=edge_styles)

        # 显示图
        plt.title("Disjunctive graph")
        plt.show()


a = Disjunctive_graph(["o11", "o21", "o23", "o31", "o32", "o12", "o22", "o13"],
                      [("o11", "o12"), ("o12", "o13"), ("o21", "o22"), ("o22", "o23"), ("o31", "o32")],
                      [("o12", "o22")], [("o11", "o21")])
a.draw()
