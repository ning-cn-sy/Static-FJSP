import copy
import uuid

from jmetal.core.solution import CompositeSolution

from MultiObjectiveOptimization.FJSP_MR.Config.AuxiliaryModules import AuxiliaryModules
from MultiObjectiveOptimization.FJSP_MR.Config.Machine import Machine
from MultiObjectiveOptimization.FJSP_MR.Config.Operation import Operation


def get_uuid():
    return uuid.uuid4()


def split_every_element(group=[[]]):
    return [element for group_element in group for element in group_element]


def find_op(node_name, tasks):
    #  这里可能出现o1 11 和 o11 1 又加了个elif
    for task in tasks:
        if len(node_name) == 3:
            if task.job_id == int(node_name[1]) and task.id == int(node_name[2]):
                return task
        elif task.job_id == int(node_name[1] + node_name[2]) and task.id == int(node_name[3]):
            return task
        elif task.job_id == int(node_name[1]) and task.id == int(node_name[2] + node_name[3]):
            return task
        # 因为有的可能超过三位了  O 101


def find_node(op, nodes):
    for node in nodes:
        if op.job_id < 10:
            if op.job_id == int(node.name[1]) and op.id == int(node.name[2]):
                return node
        elif op.job_id == int(node.name[1]) and op.id == int(node.name[2] + node.name[3]):
            return node
        elif op.job_id == int(node.name[1] + node.name[2]) and op.id == int(node.name[3]):
            return node


def t_name(name):
    return f"t{name}"


def c_name(name1, name2):
    return f"C{name1, name2}"


def x_name(name1, name2, name3):
    return f"x{name1, name2, name3}"


def y_name(name1, name2, name3, name4):
    return f"y{name1, name2, name3, name4}"


def h_name(name1, name2, name3, name4):
    return f"η{name1, name2, name3, name4}"


def s_name(name1, name2, name3, name4):
    return f"σ{name1, name2, name3, name4}"


# 约束11、12 name8不一样 约束11 的name8是q'  约束12 k'
def constraint_name(name1, name2, name3="", name4="", name5="", name6="", name7="", name8="", flag=10):
    ret = "C" + str(name1) + "-i" + str(name2)
    if name3 != "":
        ret = ret + "-j" + str(name3)
    if name4 != "":
        ret = ret + "-k" + str(name4)
    if name5 != "":
        ret = ret + "-q" + str(name5)
    if name6 != "":
        ret = ret + "-i'" + str(name6)
    if name7 != "":
        ret = ret + "-j'" + str(name7)
    if name8 != "":
        if flag == 0:
            ret = ret + "-q'" + str(name8)
        elif flag == 1:
            ret = ret + "-k'" + str(name8)

    return ret


def if_p(op: Operation, machine: Machine):
    for key in op.available_machines_am:
        if key[0] == machine.id:
            return 1.0
    return 0.0


def if_processed(op: Operation, machine: Machine, am: AuxiliaryModules = AuxiliaryModules(0, "", 0, 0)):
    for key in op.available_machines_am:
        # 这么写得要求一定有机器不装am能加工
        if key[0] == machine.id and key[1] == am.id:
            return 1.0
    return 0.0


def get_process_time(op: Operation, machine: Machine, am: AuxiliaryModules):
    return 0.0 if (machine.id, am.id) not in op.available_machines_am else float(
        op.available_machines_am[(machine.id, am.id)])


def get_y_factor(is_assemble, op, machine_list, auxiliary_module_list):
    return [-(get_process_time(op, machine, am) + (is_assemble * am.assemble_time)) for machine in machine_list
            for am in auxiliary_module_list]


# γ
def get_reconfigure_time_γ(am: AuxiliaryModules, _am: AuxiliaryModules):
    return 0.0 if am == _am else float(am.assemble_time + _am.disassemble_time)


def get_reconfigure_time_τ(machine: Machine, _machine: Machine, am: AuxiliaryModules):
    return 0.0 if machine == _machine else float(am.disassemble_time + am.assemble_time)


def spilt_variable_name(result, i):
    return list(result[i][0].replace("(", "").replace(")", "").replace(",", "").replace(" ", ""))


def get_task_by_id(job_id, op_id, task_list):
    for task in task_list:
        if task.op.job_id == int(job_id) and task.op.id == int(op_id):
            return task
    return None


def print_model(cpx):
    # 打印目标函数
    objective = cpx.objective.get_linear()
    variable_names = cpx.variables.get_names()

    print("Objective function:")
    for var_index, coef in enumerate(objective):
        print(f"{coef}*{variable_names[var_index]}", end=" + ")
    print("\n")

    # 打印约束
    constraints = cpx.linear_constraints.get_rows()
    sense = cpx.linear_constraints.get_senses()
    rhs = cpx.linear_constraints.get_rhs()
    constraint_names = cpx.linear_constraints.get_names()

    sense_map = {"L": "<=", "G": ">=", "E": "="}

    print("Constraints:")
    for i, row in enumerate(constraints):
        print(f"Constraint {constraint_names[i]}:")
        for var_index, coef in zip(row.ind, row.val):
            print(f"{coef}*{variable_names[var_index]}", end=" + ")
        print(f"{sense_map[sense[i]]} {rhs[i]}")
        print()


def copy_list(op_list: list):
    ret = []
    for op in op_list:
        ret.append(op.copy())
    return ret


def copy_map(op_map: dict):
    ret = {}
    for key, value in op_map.items():
        ret[key] = copy_list(value)
    return ret


def copy_solution(solution: CompositeSolution):
    new_solution = CompositeSolution(copy.deepcopy(solution.variables))
    new_solution.objectives = copy.deepcopy(solution.objectives)
    new_solution.constraints = copy.deepcopy(solution.constraints)
    new_solution.attributes = copy.deepcopy(solution.attributes)
    return new_solution


def check(map, check_logo=""):
    for key in map.keys():
        ops = map[key]
        for op in ops:
            if check_logo == "机器":
                if op.machine.id != key:
                    # print("——机器错啦——机器错啦——机器错啦——机器错啦——机器错啦——机器错啦——机器错啦——机器错啦——机器错啦")
                    raise ValueError(
                        "——机器错啦——机器错啦——机器错啦——机器错啦——机器错啦——机器错啦——机器错啦——机器错啦——机器错啦")
            if check_logo == "am":
                if op.am.id != key:
                    # print("——am错啦——am错啦——am错啦——am错啦——am错啦——am错啦——am错啦——am错啦——am错啦——am错啦——am错啦")
                    raise ValueError(
                        "——am错啦——am错啦——am错啦——am错啦——am错啦——am错啦——am错啦——am错啦——am错啦——am错啦——am错啦")


def check_2map(machine2ops_map, am2ops_map):
    check(machine2ops_map, "机器")
    check(am2ops_map, "am")
