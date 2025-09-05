from typing import Dict

from MultiObjectiveOptimization.FJSP.Util.DrawDistinctGraph import Node, Edge


def op_to_node(op, nodes):
    for node in nodes:
        if f"O{op.job_id}{op.op_id}" == node.name:
            return node


def get_nodes_edges(jobs):
    nodes = []
    edges = []
    # 开始找节点
    node0 = Node(0, 'Begin')
    node99 = Node(99, 'End')
    nodes.append(node0)
    machine_to_op: Dict[int, list] = {}
    i = 1
    for job in jobs:
        for op in job.ops:
            nodes.append(Node(i, f"O{job.id}{op.op_id}"))
            # 第一道工序跟begin连
            if op.op_id == 1:
                edges.append(Edge(node0, Node(i, f"O{job.id}{op.op_id}"), job.release_time, 'Connection arc'))
            # 中间连
            else:
                prev_op = job.ops[op.op_id - 2]
                edges.append(Edge(nodes[i - 1], Node(i, f"O{job.id}{op.op_id}"), prev_op.end_time - prev_op.start_time,
                                  'Connection arc'))
            # 跟end连
            if op.op_id == len(job.ops):
                edges.append(
                    Edge(Node(i, f"O{job.id}{op.op_id}"), node99, op.end_time - op.start_time, 'Connection arc'))

            # 根据机器号分类
            if op.to_machine not in machine_to_op:
                machine_to_op[op.to_machine] = []
            machine_to_op[op.to_machine].append(op)
            i += 1
    # 根据工序的开始时间进行排序
    for machine, ops in machine_to_op.items():
        machine_to_op[machine] = sorted(ops, key=lambda op: op.start_time)
    # 画机器弧
    for machine in machine_to_op:
        ops_list = machine_to_op[machine]
        edges.append(Edge(node0, op_to_node(ops_list[0], nodes), 2, f'M{machine} Disjunctive arc'))
        for j in range(0, len(ops_list) - 1):
            edges.append(Edge(op_to_node(ops_list[j], nodes), op_to_node(ops_list[j + 1], nodes),
                              ops_list[j].end_time - ops_list[j].start_time,
                              f'M{machine} Disjunctive arc'))
        machine_lastop = ops_list[len(ops_list)-1]
        edges.append(
            Edge(op_to_node(machine_lastop, nodes), node99, machine_lastop.end_time - machine_lastop.start_time,
                 f'M{machine} Disjunctive arc'))
    nodes.append(node99)
    return nodes, edges
