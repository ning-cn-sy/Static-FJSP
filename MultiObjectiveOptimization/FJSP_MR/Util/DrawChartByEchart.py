# -*- coding: utf-8 -*-
# @Time    : 2024/6/20 18:38
# @Author  : 宁诗铎
# @Site    : 
# @File    : DrawChartByEchart.py
# @Software: PyCharm 
# @Comment :


from collections import defaultdict


def get_string(path):
    try:
        with open(path, "r", encoding="utf-8") as reader:
            return reader.read()
    except Exception as e:
        print(e)


def __init__(self):
    self.CONTENT_STRING = ""
    self.machine_map = {}
    self.produre_by_piece = defaultdict(list)
    self.procedure_list = []
    self.procedure_integer_map = {}
    self.machine_integer_map = {}


def replace_str(title, input_str, new_str):
    find_index = input_str.find(title)
    if find_index >= 0:
        return input_str[:find_index] + new_str + input_str[
                                                  find_index + len(title):]


def draw_echarts(op_list, machine_names, job_list, input_path, output_path):
    all_info = get_string(input_path)
    # print(all_info)
    # replace_categories(machine_names)

    categories_str = "'" + machine_names[0] + "'"
    for i, machine in enumerate(machine_names[1:], start=1):
        categories_str += f",'{machine}'"
    # print(categories_str)
    title = "NSD_CATEGORIES"
    all_info = replace_str(title, all_info, categories_str)

    # print(all_info)

    # replace_types()

    types_str = "{name: '工件" + str(job_list[0].id) + "', color: colours[0]}"
    for i, job in enumerate(job_list[1:], start=1):
        types_str += f",\n{{name:'工件{job.id}', color:colours[{i}]}}"

    title = "NSD_TYPES"
    all_info = replace_str(title, all_info, types_str)
    # print(all_info)

    # replace_data()

    alldatastr = ""
    for op in op_list:
        base_time = op.expected_start_time
        duration = op.proc_time
        piece_num = int(op.id)
        machine_id = op.work_center.id - 1
        type_item_index = op.job.id - 1
        alldatastr += f"""
        baseTime = {base_time};
        duration = {duration};
        typeItem = types[{type_item_index}];
        data.push({{
            name: typeItem.name,
            value: [
                {machine_id},
                baseTime,
                baseTime += duration,
                duration,
                '{op.id + op.job.id}'
            ],
            itemStyle: {{
                normal: {{
                    color: typeItem.color
                }}
            }}
        }});"""

    title = "NSD_DATA"
    all_info = replace_str(title, all_info, alldatastr)
    # print(all_info)

    title = "maxTime"
    # max_time = max(procedure.get_end_time() for procedure in op_list)
    max_time = max(op.expected_start_time + op.proc_time for procedure in op_list)
    all_info = replace_str(title, all_info, f"'{max_time}'")
    try:
        with open(output_path, "w", encoding="utf-8") as outweb:
            outweb.write(all_info)
    except Exception as e:
        print(e)
