# -*- coding: utf-8 -*-
# @Time    : 2025/1/10 20:11
# @Author  : 宁诗铎
# @Site    : 
# @File    : Instance_read_generator.py
# @Software: PyCharm 
# @Comment : 案
import random

from MultiObjectiveOptimization.FJSP_AO.Config.Assemble_style import Assemble_style
from MultiObjectiveOptimization.FJSP_AO.Config.Job import Job_style
from MultiObjectiveOptimization.FJSP_AO.Config.Machine import Machine
from MultiObjectiveOptimization.FJSP_AO.Config.Operation import Op_style, Assembling_operation
from MultiObjectiveOptimization.FJSP_AO.Util.Read_By_FJS import readDataByFJS


def create_assemble_style(name, param1, param2):
    """简化装配规则的创建"""
    astyle = Assemble_style(name)
    astyle.param1 = param1
    astyle.param2 = param2
    return astyle


# 定义装配规则
astyle1 = create_assemble_style("A11", Job_style.style1, Job_style.style2)
astyle2 = create_assemble_style("A12", astyle1, Job_style.style3)
astyle3 = create_assemble_style("A21", Job_style.style4, Job_style.style5)
astyle4 = create_assemble_style("A22", astyle3, Job_style.style6)
astyle5 = create_assemble_style("A3", Job_style.style7, Job_style.style8)
astyle6 = create_assemble_style("A4", astyle5, Job_style.style9)
astyle7 = create_assemble_style("A5", Job_style.style10, Job_style.style11)
astyle8 = create_assemble_style("A6", Job_style.style12, Job_style.style13)
astyle9 = create_assemble_style("A7", Job_style.style14, Job_style.style15)
astyle10 = create_assemble_style("A8", Job_style.style16, Job_style.style17)
astyle11 = create_assemble_style("A9", Job_style.style18, Job_style.style19)
astyle12 = create_assemble_style("A9", Job_style.style20, Job_style.style21)
astyle13 = create_assemble_style("A9", Job_style.style22, Job_style.style23)
astyle14 = create_assemble_style("A11", Job_style.style24, Job_style.style25)
astyle15 = create_assemble_style("A12", astyle14, Job_style.style26)


class jobs_config:
    def __init__(self, jobs, machines):
        self.jobs = jobs
        self.machines = machines

    def set_release_time(self, release_times):
        for i, job in enumerate(release_times):
            self.jobs[i].release_time = release_times[i]

    def set_jobs_styles(self, jobs_styles):
        for i, job in enumerate(self.jobs):
            self.jobs[i].style = Job_style.from_value(jobs_styles[i])

    def set_op_styles(self, op_styles):
        for i, job in enumerate(self.jobs):
            op_id = job.ops[-1].op_id + 1
            for op_style in op_styles[i]:
                try:
                    op = Assembling_operation(job.id, op_id, Op_style.assembling, op_style[1], op_style[0])
                except:
                    print()
                self.jobs[i].ops.append(op)
                op_id = op_id + 1


def generate_jobs_config(jobs, machines, num_machine, fjs_name, y, type):
    jobs_styles = []  # 初始化空列表
    n = len(jobs)
    p = int(n / 3)
    x = y

    base = [1, 2, 3, 4, 5, 6, 7, 8, 9, 24, 25, 26]
    remaining_length = n - x * 3
    if type == 'AB':
        if remaining_length < 3:
            x = x - 1
            remaining_length = n - x * 3
            if remaining_length < 3:
                x = x - 1
                remaining_length = n - x * 3
            if remaining_length % 2 == 0:
                remaining = [10 if i % 2 == 0 else 11 for i in range(remaining_length)]
                jobs_styles = remaining + [base[0], base[1], base[2]] * x
                Judgment = x
            else:
                remaining = [10 if i % 2 == 0 else 11 for i in range(remaining_length - 3)]
                jobs_styles = remaining + [base[0], base[1], base[2]] * (x + 1)
                Judgment = x + 1
        else:
            if remaining_length % 2 == 0:
                remaining = [10 if i % 2 == 0 else 11 for i in range(remaining_length)]
                jobs_styles = remaining + [base[0], base[1], base[2]] * x
                Judgment = x
            else:
                remaining = [10 if i % 2 == 0 else 11 for i in range(remaining_length - 3)]
                jobs_styles = remaining + [base[0], base[1], base[2]] * (x + 1)
                Judgment = x + 1
    else:
        if remaining_length < 3:
            x = x - 1
            remaining_length = n - x * 3
            if remaining_length < 3:
                x = x - 1
                remaining_length = n - x * 3
            if remaining_length % 2 == 0:
                a = list(range(10, 24))
                ramaining = [a[i] for i in range(remaining_length)]
                jobs_styles = ramaining + [base[i] for i in range(x * 3)]
                Judgment = x
            else:
                a = list(range(10, 24))
                ramaining = [a[i] for i in range(remaining_length - 3)]
                jobs_styles = ramaining + [base[i] for i in range((x + 1) * 3)]
                Judgment = x + 1
        else:
            if remaining_length % 2 == 0:
                a = list(range(10, 24))
                ramaining = [a[i] for i in range(remaining_length)]
                jobs_styles = ramaining + [base[i] for i in range(x * 3)]
                Judgment = x
            else:
                a = list(range(10, 24))
                ramaining = [a[i] for i in range(remaining_length - 3)]
                jobs_styles = ramaining + [base[i] for i in range((x + 1) * 3)]
                Judgment = x + 1

    config_ = jobs_config(jobs, machines)
    config_.set_jobs_styles(jobs_styles)
    op_style = []
    if type == 'AB':
        if y == 1:
            if fjs_name[0:4] == 'MFJS':
                for index, job in enumerate(config_.jobs):
                    if index > len(config_.jobs) - Judgment * 3 - 1:
                        if job.style.value == 1 or job.style.value == 2:
                            op_styles = [
                                (astyle1, [(num_machine + 1, 119), (num_machine + 2, 95), (num_machine + 3, 104)]),
                                (astyle2, [(num_machine + 1, 110), (num_machine + 2, 141), (num_machine + 3, 147)])]
                            op_style.append(op_styles)
                        else:
                            op_styles = [
                                (astyle2, [(num_machine + 1, 110), (num_machine + 2, 141), (num_machine + 3, 147)])]
                            op_style.append(op_styles)
                    else:
                        op_styles = [
                            (astyle7, [(num_machine + 1, 135), (num_machine + 2, 156), (num_machine + 3, 159)])]
                        op_style.append(op_styles)
            else:
                for index, job in enumerate(config_.jobs):
                    if index > len(config_.jobs) - Judgment * 3 - 1:
                        if job.style.value == 1 or job.style.value == 2:
                            op_styles = [
                                (astyle1, [(num_machine + 1, 12), (num_machine + 2, 15), (num_machine + 3, 16)]),
                                (astyle2, [(num_machine + 1, 26), (num_machine + 2, 27), (num_machine + 3, 23)])]
                            op_style.append(op_styles)
                        else:
                            op_styles = [
                                (astyle2, [(num_machine + 1, 26), (num_machine + 2, 27), (num_machine + 3, 23)])]
                            op_style.append(op_styles)
                    else:
                        op_styles = [(astyle7, [(num_machine + 1, 17), (num_machine + 2, 12), (num_machine + 3, 15)])]
                        op_style.append(op_styles)
        else:
            if fjs_name[0:4] == 'MFJS':
                for index, job in enumerate(config_.jobs):
                    if index > len(config_.jobs) - Judgment * 3 - 1:
                        if job.style.value == 1 or job.style.value == 2:
                            op_styles = [
                                (astyle1, [(num_machine + 1, 465), (num_machine + 2, 328), (num_machine + 3, 446)]),
                                (astyle2, [(num_machine + 1, 249), (num_machine + 2, 657), (num_machine + 3, 650)])]
                            op_style.append(op_styles)
                        else:
                            op_styles = [
                                (astyle2, [(num_machine + 1, 249), (num_machine + 2, 657), (num_machine + 3, 650)])]
                            op_style.append(op_styles)
                    else:
                        op_styles = [
                            (astyle7, [(num_machine + 1, 765), (num_machine + 2, 649), (num_machine + 3, 625)])]
                        op_style.append(op_styles)
            else:
                for index, job in enumerate(config_.jobs):
                    if index > len(config_.jobs) - Judgment * 3 - 1:
                        if job.style.value == 1 or job.style.value == 2:
                            op_styles = [
                                (astyle1, [(num_machine + 1, 57), (num_machine + 2, 59), (num_machine + 3, 45)]),
                                (astyle2, [(num_machine + 1, 66), (num_machine + 2, 79), (num_machine + 3, 65)])]
                            op_style.append(op_styles)
                        else:
                            op_styles = [
                                (astyle2, [(num_machine + 1, 66), (num_machine + 2, 79), (num_machine + 3, 65)])]
                            op_style.append(op_styles)
                    else:
                        op_styles = [
                            (astyle7, [(num_machine + 1, 68), (num_machine + 2, 67), (num_machine + 3, 55)])]
                        op_style.append(op_styles)
    else:
        if y == 1:
            if fjs_name[0:4] == 'MFJS':
                for index, job in enumerate(config_.jobs):
                    if index > len(config_.jobs) - Judgment * 3 - 1:
                        if job.style.value == 1 or job.style.value == 2:
                            op_styles = [
                                (astyle1, [(num_machine + 1, 95), (num_machine + 2, 150), (num_machine + 3, 182)]),
                                (astyle2, [(num_machine + 1, 160), (num_machine + 2, 125), (num_machine + 3, 175)])]
                            op_style.append(op_styles)
                        elif job.style.value == 3:
                            op_styles = [
                                (astyle2, [(num_machine + 1, 160), (num_machine + 2, 125), (num_machine + 3, 175)])]
                            op_style.append(op_styles)
                        elif job.style.value == 4 or job.style.value == 5:
                            op_styles = [
                                (astyle3, [(num_machine + 1, 145), (num_machine + 2, 110), (num_machine + 3, 120)]),
                                (astyle4, [(num_machine + 1, 175), (num_machine + 2, 130), (num_machine + 3, 130)])]
                            op_style.append(op_styles)
                        elif job.style.value == 6:
                            op_styles = [
                                (astyle4, [(num_machine + 1, 175), (num_machine + 2, 130), (num_machine + 3, 130)])]
                            op_style.append(op_styles)
                        elif job.style.value == 7 or job.style.value == 8:
                            op_styles = [
                                (astyle5, [(num_machine + 1, 105), (num_machine + 2, 167), (num_machine + 3, 166)]),
                                (astyle6, [(num_machine + 1, 158), (num_machine + 2, 120), (num_machine + 3, 176)])]
                            op_style.append(op_styles)
                        elif job.style.value == 9:
                            op_styles = [
                                (astyle6, [(num_machine + 1, 158), (num_machine + 2, 120), (num_machine + 3, 176)])]
                            op_style.append(op_styles)
                        elif job.style.value == 24 or job.style.value == 25:
                            op_styles = [
                                (astyle14, [(num_machine + 1, 153), (num_machine + 2, 155), (num_machine + 3, 115)]),
                                (astyle15, [(num_machine + 1, 135), (num_machine + 2, 139), (num_machine + 3, 175)])]
                            op_style.append(op_styles)
                        elif job.style.value == 26:
                            op_styles = [
                                (astyle15, [(num_machine + 1, 135), (num_machine + 2, 139), (num_machine + 3, 175)])]
                            op_style.append(op_styles)
                    else:

                        if job.style.value == 10 or job.style.value == 11:
                            op_styles = [
                                (astyle7, [(num_machine + 1, 140), (num_machine + 2, 247), (num_machine + 3, 261)])]
                            op_style.append(op_styles)
                        if job.style.value == 12 or job.style.value == 13:
                            op_styles = [
                                (astyle8, [(num_machine + 1, 129), (num_machine + 2, 122), (num_machine + 3, 152)])]
                            op_style.append(op_styles)
                        if job.style.value == 14 or job.style.value == 15:
                            op_styles = [
                                (astyle9, [(num_machine + 1, 118), (num_machine + 2, 161), (num_machine + 3, 123)])]
                            op_style.append(op_styles)
                        if job.style.value == 16 or job.style.value == 17:
                            op_styles = [
                                (astyle10, [(num_machine + 1, 135), (num_machine + 2, 190), (num_machine + 3, 128)])]
                            op_style.append(op_styles)
                        if job.style.value == 18 or job.style.value == 19:
                            op_styles = [
                                (astyle11, [(num_machine + 1, 102), (num_machine + 2, 110), (num_machine + 3, 155)])]
                            op_style.append(op_styles)
                        if job.style.value == 20 or job.style.value == 21:
                            op_styles = [
                                (astyle12, [(num_machine + 1, 190), (num_machine + 2, 100), (num_machine + 3, 232)])]
                            op_style.append(op_styles)
                        if job.style.value == 22 or job.style.value == 23:
                            op_styles = [
                                (astyle13, [(num_machine + 1, 83), (num_machine + 2, 173), (num_machine + 3, 150)])]
                            op_style.append(op_styles)
            else:
                for index, job in enumerate(config_.jobs):
                    if index > len(config_.jobs) - Judgment * 3 - 1:
                        if job.style.value == 1 or job.style.value == 2:
                            op_styles = [
                                (astyle1, [(num_machine + 1, 18), (num_machine + 2, 12), (num_machine + 3, 17)]),
                                (astyle2, [(num_machine + 1, 23), (num_machine + 2, 27), (num_machine + 3, 25)])]
                            op_style.append(op_styles)
                        if job.style.value == 3:
                            op_styles = [
                                (astyle2, [(num_machine + 1, 23), (num_machine + 2, 27), (num_machine + 3, 25)])]
                            op_style.append(op_styles)
                        if job.style.value == 4 or job.style.value == 5:
                            op_styles = [
                                (astyle3, [(num_machine + 1, 12), (num_machine + 2, 19), (num_machine + 3, 21)]),
                                (astyle4, [(num_machine + 1, 43), (num_machine + 2, 47), (num_machine + 3, 42)])]
                            op_style.append(op_styles)
                        if job.style.value == 6:
                            op_styles = [
                                (astyle4, [(num_machine + 1, 43), (num_machine + 2, 47), (num_machine + 3, 42)])]
                            op_style.append(op_styles)
                        if job.style.value == 7 or job.style.value == 8:
                            op_styles = [
                                (astyle5, [(num_machine + 1, 34), (num_machine + 2, 31), (num_machine + 3, 33)]),
                                (astyle6, [(num_machine + 1, 30), (num_machine + 2, 35), (num_machine + 3, 36)])]
                            op_style.append(op_styles)
                        if job.style.value == 9:
                            op_styles = [
                                (astyle6, [(num_machine + 1, 30), (num_machine + 2, 35), (num_machine + 3, 36)])]
                            op_style.append(op_styles)
                        if job.style.value == 24 or job.style.value == 25:
                            op_styles = [
                                (astyle14, [(num_machine + 1, 53), (num_machine + 2, 59), (num_machine + 3, 56)]),
                                (astyle15, [(num_machine + 1, 30), (num_machine + 2, 27), (num_machine + 3, 34)])]
                            op_style.append(op_styles)
                        if job.style.value == 26:
                            op_styles = [
                                (astyle15, [(num_machine + 1, 30), (num_machine + 2, 27), (num_machine + 3, 34)])]
                            op_style.append(op_styles)
                    else:

                        if job.style.value == 10 or job.style.value == 11:
                            op_styles = [
                                (astyle7, [(num_machine + 1, 69), (num_machine + 2, 64), (num_machine + 3, 57)])]
                            op_style.append(op_styles)
                        if job.style.value == 12 or job.style.value == 13:
                            op_styles = [
                                (astyle8, [(num_machine + 1, 23), (num_machine + 2, 24), (num_machine + 3, 27)])]
                            op_style.append(op_styles)
                        if job.style.value == 14 or job.style.value == 15:
                            op_styles = [
                                (astyle9, [(num_machine + 1, 36), (num_machine + 2, 44), (num_machine + 3, 40)])]
                            op_style.append(op_styles)
                        if job.style.value == 16 or job.style.value == 17:
                            op_styles = [
                                (astyle10, [(num_machine + 1, 52), (num_machine + 2, 44), (num_machine + 3, 57)])]
                            op_style.append(op_styles)
                        if job.style.value == 18 or job.style.value == 19:
                            op_styles = [
                                (astyle11, [(num_machine + 1, 23), (num_machine + 2, 25), (num_machine + 3, 29)])]
                            op_style.append(op_styles)
                        if job.style.value == 20 or job.style.value == 21:
                            op_styles = [
                                (astyle12, [(num_machine + 1, 48), (num_machine + 2, 46), (num_machine + 3, 37)])]
                            op_style.append(op_styles)
                        if job.style.value == 22 or job.style.value == 23:
                            op_styles = [
                                (astyle13, [(num_machine + 1, 41), (num_machine + 2, 54), (num_machine + 3, 55)])]
                            op_style.append(op_styles)
        else:
            if fjs_name[0:4] == 'MFJS':
                for index, job in enumerate(config_.jobs):
                    if index > len(config_.jobs) - Judgment * 3 - 1:
                        if job.style.value == 1 or job.style.value == 2:
                            op_styles = [
                                (astyle1, [(num_machine + 1, 453), (num_machine + 2, 428), (num_machine + 3, 403)]),
                                (astyle2, [(num_machine + 1, 478), (num_machine + 2, 465), (num_machine + 3, 265)])]
                            op_style.append(op_styles)
                        elif job.style.value == 3:
                            op_styles = [
                                (astyle2, [(num_machine + 1, 478), (num_machine + 2, 465), (num_machine + 3, 265)])]
                            op_style.append(op_styles)
                        elif job.style.value == 4 or job.style.value == 5:
                            op_styles = [
                                (astyle3, [(num_machine + 1, 449), (num_machine + 2, 458), (num_machine + 3, 477)]),
                                (astyle4, [(num_machine + 1, 514), (num_machine + 2, 482), (num_machine + 3, 555)])]
                            op_style.append(op_styles)
                        elif job.style.value == 6:
                            op_styles = [
                                (astyle4, [(num_machine + 1, 514), (num_machine + 2, 482), (num_machine + 3, 555)])]
                            op_style.append(op_styles)
                        elif job.style.value == 7 or job.style.value == 8:
                            op_styles = [
                                (astyle5, [(num_machine + 1, 530), (num_machine + 2, 467), (num_machine + 3, 437)]),
                                (astyle6, [(num_machine + 1, 457), (num_machine + 2, 490), (num_machine + 3, 476)])]
                            op_style.append(op_styles)
                        elif job.style.value == 9:
                            op_styles = [
                                (astyle6, [(num_machine + 1, 457), (num_machine + 2, 490), (num_machine + 3, 476)])]
                            op_style.append(op_styles)
                        elif job.style.value == 24 or job.style.value == 25:
                            op_styles = [
                                (astyle14, [(num_machine + 1, 553), (num_machine + 2, 474), (num_machine + 3, 529)]),
                                (astyle15, [(num_machine + 1, 526), (num_machine + 2, 443), (num_machine + 3, 500)])]
                            op_style.append(op_styles)
                        elif job.style.value == 26:
                            op_styles = [
                                (astyle15, [(num_machine + 1, 526), (num_machine + 2, 443), (num_machine + 3, 500)])]
                            op_style.append(op_styles)
                    else:

                        if job.style.value == 10 or job.style.value == 11:
                            op_styles = [
                                (astyle7, [(num_machine + 1, 562), (num_machine + 2, 647), (num_machine + 3, 661)])]
                            op_style.append(op_styles)
                        if job.style.value == 12 or job.style.value == 13:
                            op_styles = [
                                (astyle8, [(num_machine + 1, 453), (num_machine + 2, 684), (num_machine + 3, 552)])]
                            op_style.append(op_styles)
                        if job.style.value == 14 or job.style.value == 15:
                            op_styles = [
                                (astyle9, [(num_machine + 1, 558), (num_machine + 2, 561), (num_machine + 3, 468)])]
                            op_style.append(op_styles)
                        if job.style.value == 16 or job.style.value == 17:
                            op_styles = [
                                (astyle10, [(num_machine + 1, 440), (num_machine + 2, 434), (num_machine + 3, 484)])]
                            op_style.append(op_styles)
                        if job.style.value == 18 or job.style.value == 19:
                            op_styles = [
                                (astyle11, [(num_machine + 1, 495), (num_machine + 2, 446), (num_machine + 3, 522)])]
                            op_style.append(op_styles)
                        if job.style.value == 20 or job.style.value == 21:
                            op_styles = [
                                (astyle12, [(num_machine + 1, 590), (num_machine + 2, 566), (num_machine + 3, 476)])]
                            op_style.append(op_styles)
                        if job.style.value == 22 or job.style.value == 23:
                            op_styles = [
                                (astyle13, [(num_machine + 1, 483), (num_machine + 2, 473), (num_machine + 3, 418)])]
                            op_style.append(op_styles)
            else:
                for index, job in enumerate(config_.jobs):
                    if index > len(config_.jobs) - Judgment * 3 - 1:
                        if job.style.value == 1 or job.style.value == 2:
                            op_styles = [
                                (astyle1, [(num_machine + 1, 91), (num_machine + 2, 55), (num_machine + 3, 86)]),
                                (astyle2, [(num_machine + 1, 89), (num_machine + 2, 85), (num_machine + 3, 74)])]
                            op_style.append(op_styles)
                        if job.style.value == 3:
                            op_styles = [
                                (astyle2, [(num_machine + 1, 89), (num_machine + 2, 85), (num_machine + 3, 74)])]
                            op_style.append(op_styles)
                        if job.style.value == 4 or job.style.value == 5:
                            op_styles = [
                                (astyle3, [(num_machine + 1, 65), (num_machine + 2, 76), (num_machine + 3, 75)]),
                                (astyle4, [(num_machine + 1, 87), (num_machine + 2, 86), (num_machine + 3, 77)])]
                            op_style.append(op_styles)
                        if job.style.value == 6:
                            op_styles = [
                                (astyle4, [(num_machine + 1, 87), (num_machine + 2, 86), (num_machine + 3, 77)])]
                            op_style.append(op_styles)
                        if job.style.value == 7 or job.style.value == 8:
                            op_styles = [
                                (astyle5, [(num_machine + 1, 86), (num_machine + 2, 76), (num_machine + 3, 85)]),
                                (astyle6, [(num_machine + 1, 61), (num_machine + 2, 77), (num_machine + 3, 66)])]
                            op_style.append(op_styles)
                        if job.style.value == 9:
                            op_styles = [
                                (astyle6, [(num_machine + 1, 61), (num_machine + 2, 77), (num_machine + 3, 66)])]
                            op_style.append(op_styles)
                        if job.style.value == 24 or job.style.value == 25:
                            op_styles = [
                                (astyle14, [(num_machine + 1, 61), (num_machine + 2, 77), (num_machine + 3, 86)]),
                                (astyle15, [(num_machine + 1, 58), (num_machine + 2, 136), (num_machine + 3, 74)])]
                            op_style.append(op_styles)
                        if job.style.value == 26:
                            op_styles = [
                                (astyle15, [(num_machine + 1, 58), (num_machine + 2, 136), (num_machine + 3, 74)])]
                            op_style.append(op_styles)
                    else:

                        if job.style.value == 10 or job.style.value == 11:
                            op_styles = [
                                (astyle7, [(num_machine + 1, 99), (num_machine + 2, 76), (num_machine + 3, 57)])]
                            op_style.append(op_styles)
                        if job.style.value == 12 or job.style.value == 13:
                            op_styles = [
                                (astyle8, [(num_machine + 1, 58), (num_machine + 2, 56), (num_machine + 3, 59)])]
                            op_style.append(op_styles)
                        if job.style.value == 14 or job.style.value == 15:
                            op_styles = [
                                (astyle9, [(num_machine + 1, 82), (num_machine + 2, 72), (num_machine + 3, 68)])]
                            op_style.append(op_styles)
                        if job.style.value == 16 or job.style.value == 17:
                            op_styles = [
                                (astyle10, [(num_machine + 1, 75), (num_machine + 2, 71), (num_machine + 3, 88)])]
                            op_style.append(op_styles)
                        if job.style.value == 18 or job.style.value == 19:
                            op_styles = [
                                (astyle11, [(num_machine + 1, 83), (num_machine + 2, 79), (num_machine + 3, 72)])]
                            op_style.append(op_styles)
                        if job.style.value == 20 or job.style.value == 21:
                            op_styles = [
                                (astyle12, [(num_machine + 1, 95), (num_machine + 2, 86), (num_machine + 3, 73)])]
                            op_style.append(op_styles)
                        if job.style.value == 22 or job.style.value == 23:
                            op_styles = [
                                (astyle13, [(num_machine + 1, 88), (num_machine + 2, 122), (num_machine + 3, 78)])]
                            op_style.append(op_styles)

    style1 = 0
    style2 = 0
    style3 = 0
    style4 = 0
    style5 = 0
    style6 = 0
    style7 = 0
    style8 = 0
    style9 = 0
    style10 = 0
    style11 = 0
    style12 = 0
    style13 = 0
    style14 = 0
    style15 = 0
    style16 = 0
    style17 = 0
    style18 = 0
    style19 = 0
    style20 = 0
    style21 = 0
    style22 = 0
    style23 = 0
    style24 = 0
    style25 = 0
    style26 = 0

    for job in config_.jobs:
        if job.style.value == 1:
            style1 = len(job.ops)
        if job.style.value == 2:
            style2 = len(job.ops)
        if job.style.value == 3:
            style3 = len(job.ops)
        if job.style.value == 4:
            style4 = len(job.ops)
        if job.style.value == 5:
            style5 = len(job.ops)
        if job.style.value == 6:
            style6 = len(job.ops)
        if job.style.value == 7:
            style7 = len(job.ops)
        if job.style.value == 8:
            style8 = len(job.ops)
        if job.style.value == 9:
            style9 = len(job.ops)
        if job.style.value == 10:
            style10 = len(job.ops)
        if job.style.value == 11:
            style11 = len(job.ops)
        if job.style.value == 12:
            style12 = len(job.ops)
        if job.style.value == 13:
            style13 = len(job.ops)
        if job.style.value == 14:
            style14 = len(job.ops)
        if job.style.value == 15:
            style15 = len(job.ops)
        if job.style.value == 16:
            style16 = len(job.ops)
        if job.style.value == 17:
            style17 = len(job.ops)
        if job.style.value == 18:
            style18 = len(job.ops)
        if job.style.value == 19:
            style19 = len(job.ops)
        if job.style.value == 20:
            style20 = len(job.ops)
        if job.style.value == 21:
            style21 = len(job.ops)
        if job.style.value == 22:
            style22 = len(job.ops)
        if job.style.value == 23:
            style23 = len(job.ops)
        if job.style.value == 24:
            style24 = len(job.ops)
        if job.style.value == 25:
            style25 = len(job.ops)
        if job.style.value == 26:
            style26 = len(job.ops)

    astyle1.ops = [style1 + 1, style2 + 1]
    astyle2.ops = [style1 + 2, style2 + 2, style3 + 1]
    astyle3.ops = [style4 + 1, style5 + 1]
    astyle4.ops = [style4 + 2, style5 + 2, style6 + 1]
    astyle5.ops = [style7 + 1, style8 + 1]
    astyle6.ops = [style7 + 2, style8 + 2, style9 + 1]
    astyle7.ops = [style10 + 1, style11 + 1]
    astyle8.ops = [style12 + 1, style13 + 1]
    astyle9.ops = [style14 + 1, style15 + 1]
    astyle10.ops = [style16 + 1, style17 + 1]
    astyle11.ops = [style18 + 1, style19 + 1]
    astyle12.ops = [style20 + 1, style21 + 1]
    astyle13.ops = [style22 + 1, style23 + 1]
    astyle14.ops = [style24 + 1, style25 + 1]
    astyle15.ops = [style24 + 2, style25 + 2, style26 + 1]

    if fjs_name[0:4] == 'MFJS':
        release_time = [295, 90, 342, 63, 132, 350, 270, 188, 83, 184, 157, 88, 236, 270, 97, 303, 254, 32, 349, 313]
    else:
        release_time = [11, 3, 17, 19, 17, 2, 16, 0, 6, 2, 6, 12, 15, 10, 9, 7, 7, 16, 17, 11, 11, 3, 17, 19, 17, 2, 16,
                        0, 6, 2, 6, 12, 15, 10, 9, 7, 7, 16, 17, 11]

    config_.set_op_styles(op_style)
    config_.set_release_time([release_time[i] for i in range(len(jobs))])

    op_ass_mch_time = []
    for i in range(len(op_style)):
        # op_ass_mch.append(op_style[i][0][1])
        op_ass_mch = []
        for j in range(len(op_style[i][0][1])):
            op_ass_mch.append(op_style[i][0][1][j][1])
        op_ass_mch_time.append(op_ass_mch)

    return jobs_styles, op_ass_mch_time


def Instance_read_generator_by_fjs(filename, x, type):
    jobs, machines = readDataByFJS(filename)
    a = len(machines)
    n = len(jobs)

    job_style, op_ass_mch_time = generate_jobs_config(jobs, machines, a, filename[-10:-4], x, type)
    if type == 'AB':
        astyles = [astyle1, astyle2, astyle7]
    else:
        astyles = [astyle1, astyle2, astyle3, astyle4, astyle5, astyle6, astyle7, astyle8, astyle9, astyle10, astyle11,
                   astyle12, astyle13, astyle14, astyle15]

    machines.append(Machine(a + 1, random.randint(1, 10), 2))
    machines.append(Machine(a + 2, random.randint(1, 10), 2))
    machines.append(Machine(a + 3, random.randint(1, 10), 2))

    remaining = int((n - x * 3) / 2)
    remaining_length = n - x * 3
    b = [[Job_style.style10, Job_style.style11], [Job_style.style13, Job_style.style12],
         [Job_style.style15, Job_style.style14],
         [Job_style.style17, Job_style.style16], [Job_style.style19, Job_style.style18],
         [Job_style.style20, Job_style.style21], [Job_style.style23, Job_style.style22]]

    c = [[Job_style.style1, Job_style.style2, Job_style.style3], [Job_style.style4, Job_style.style5, Job_style.style6],
         [Job_style.style7, Job_style.style8, Job_style.style9],
         [Job_style.style24, Job_style.style25, Job_style.style26]]

    if type == 'AB':
        if remaining_length < 3:
            x = x - 1
            remaining_length = n - x * 3
            if remaining_length < 3:
                x = x - 1
                remaining_length = n - x * 3
            remaining = int((n - x * 3) / 2)
            if remaining_length % 2 == 0:
                need_styles = [[Job_style.style10, Job_style.style11] for _ in range(remaining)] + [c[0]] * x
            else:
                need_styles = [[Job_style.style10, Job_style.style11] for _ in range(remaining - 1)] + [c[0]] * (
                        x + 1)
        else:
            if remaining_length % 2 == 0:
                need_styles = [[Job_style.style10, Job_style.style11] for _ in range(remaining)] + [c[0]] * x
            else:
                need_styles = [[Job_style.style10, Job_style.style11] for _ in range(remaining - 1)] + [c[0]] * (x + 1)
    else:
        if remaining_length < 3:
            x = x - 1
            remaining_length = n - x * 3
            if remaining_length < 3:
                x = x - 1
                remaining_length = n - x * 3
            remaining = int((n - x * 3) / 2)
            if remaining_length % 2 == 0:
                need_styles = [b[i] for i in range(remaining)] + [c[i] for i in range(x)]
            else:
                need_styles = [b[i] for i in range(remaining - 1)] + [c[i] for i in range(x + 1)]
        else:
            if remaining_length % 2 == 0:
                need_styles = [b[i] for i in range(remaining)] + [c[i] for i in range(x)]
            else:
                need_styles = [b[i] for i in range(remaining - 1)] + [c[i] for i in range(x + 1)]

    need_style_array = []

    for i in range(len(need_styles)):
        need_sty_list = []
        for j in range(len(need_styles[i])):
            need_sty_list.append(need_styles[i][j].value)
        need_style_array.append(need_sty_list)

    return jobs, machines, astyles, need_styles, filename
