import random

from jmetal.core.operator import Mutation
from jmetal.core.solution import Solution, CompositeSolution
from jmetal.util.ckecking import Check

from MultiObjectiveOptimization.FJSP.Algorithm.Decode import Decode
from MultiObjectiveOptimization.FJSP.Util.Draw_distinct_graph import get_nodes_edges, graph, select_node_by_random, \
    get_new_jobs
from MultiObjectiveOptimization.FJSP.Util.Draw_gantt import plot_gantt_chart


class ycjMutation(Mutation[Solution]):
    def __init__(self, mutation_probability, jobs, machines):
        super(ycjMutation, self).__init__(probability=1.0)
        self.probability = mutation_probability
        self.jobs = jobs
        self.machines = machines

    def execute(self, solution: CompositeSolution) -> CompositeSolution:
        Check.that(type(solution) is CompositeSolution, "Solution type invalid")

        rand = random.random()
        if rand <= self.probability:
            # 提取当前解中的作业顺序
            temp_sequence = solution.variables[0].variables
            # 提取机器分配方案
            machine_selection = solution.variables[1].variables
            decode = Decode(self.jobs, self.machines)
            # 运行解码器，计算调度方案
            decode.run_semi_active_schedule(temp_sequence, machine_selection)
            # ️开始析取图
            nodes, edges = get_nodes_edges(decode.jobs)
            # 准备析取图
            G = graph(nodes=nodes, edges=edges)
            # G.draw_network()
            path, edges_, length = G.longest_path(False)
            #  删减了析取图
            # plot_gantt_chart(decode.jobs, decode.machines, f"{path}, {length}")
            # 现在是随机选节点
            selected_node = select_node_by_random(path)
            G_ = G.remove_machine_arcs_by_node(selected_node, G, False)
            # G_.draw_network()
            for node in G_.nodes:
                node.s = G_.longest_path_between_two_nodes(G_.nodes[0], node)
                #  尾长度不对，因为我们设置的点后边一条线的长度是边，需要再减掉节点的加工时间
                if node.op != None:
                    node.t = G_.longest_path_between_two_nodes(node, G_.nodes[len(G_.nodes) - 1]) - (
                            node.op.end_time - node.op.start_time)
                if node.name == selected_node.name:
                    selected_node.s = node.s
                    selected_node.t = node.t

            select_machine = random.choice(selected_node.op.available_machines)
            Rk, Lk, Qk = G_.get_Rk_Lk(selected_node, select_machine, G_.nodes)
            G_new = G_.insert_op(selected_node, Rk, Lk, Qk, G_, select_machine, G)
            # a, b, c = G_new.longest_path(False)
            # G_new.draw_network()
            # plot_gantt_chart(get_new_jobs(decode.jobs, G_new.edges), decode.machines, f"{a}, {c}")
            new_jobs = get_new_jobs(decode.jobs, G_new)
            solution.variables[0].variables, solution.variables[1].variables = get_new_sequence(new_jobs)
            # if -1 in solution.variables[1].variables:
            #     print(1111111)
        return solution

    def get_name(self):
        return "ycj neighborhood mutation"


def get_new_sequence(new_jobs):
    temp_sequence = []
    machine_selection = []
    # 按时间排序的op列表
    op_sequence = []
    # 按顺序排列的工序列表
    op_list = []
    for job in new_jobs:
        for op in job.ops:
            op_sequence.append(op)
            op_list.append(op)
            # if next((i for i, item in enumerate(op.available_machines) if item[0] == op.to_machine), -1)==-1:
            #     print()
            machine_selection.append(
                next((i for i, item in enumerate(op.available_machines) if item[0] == op.to_machine), -1))
    op_sequence.sort(key=lambda x: x.start_time)
    job_id_list = []
    for op in op_sequence:
        job_id_list.append(op.job_id)
        temp_sequence.append(get_op_index(op_list, op))
    return temp_sequence, machine_selection


def get_op_index(op_list, op):
    return op_list.index(op)
