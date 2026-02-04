# -*- coding: utf-8 -*-
# @Time    : 2024/12/28 19:53
# @Author  : 宁诗铎
# @Site    : 
# @File    : Pub_func.py
# @Software: PyCharm 
# @Comment : 公共函数类

from datetime import datetime
# from MultiObjectiveOptimization.FJSP_AO.Util.Plot_util.Plot_Func import plot_gantt_chart
from MultiObjectiveOptimization.FJSP_AO.Util.Plot_util.Plot_point_Func import plot_points_and_connections_by_jobs


def get_time_delta(start_time, end_time):
    return end_time - start_time


def time_format(time):
    return time.strftime("%Y-%m-%d %H:%M:%S")


def get_cur_time():
    return datetime.now()


def is_type(obj, type_name):
    """
    判断一个变量是否是某种类型。

    :param obj: 要检查的变量
    :param type_name: 要比较的类型
    :return: 如果是该类型返回 True，否则返回 False
    """
    return isinstance(obj, type_name)


def decode_(solution, jobs, machines, astyles, need_styles, filename, if_draw=False):
    from MultiObjectiveOptimization.FJSP_AO.Algrithm.Decode import Decode
    temp_sequence = solution.variables[0].variables[:]
    machine_selection = solution.variables[1].variables
    assembly_selection = solution.variables[2].variables
    decode = Decode(jobs, machines, astyles, need_styles)
    example = filename[-10:-4]
    if if_draw:
        decode.run_active_schedule(temp_sequence, machine_selection, assembly_selection)
        group = plot_points_and_connections_by_jobs(decode.jobs)
        plot_gantt_chart(decode.jobs, decode.machines, group, example + "-active")
    else:
        decode.run_semi_active_schedule(temp_sequence, machine_selection, assembly_selection)
        group = plot_points_and_connections_by_jobs(decode.jobs)
        plot_gantt_chart(decode.jobs, decode.machines, group, example + "-semi_active")
