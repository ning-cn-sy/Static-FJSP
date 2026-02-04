# -*- coding: utf-8 -*-
# @Time    : 2024/12/29 19:21
# @Author  : 宁诗铎
# @Site    : 
# @File    : Decode.py
# @Software: PyCharm 
# @Comment : 用于解码的一系列函数
import time
from collections import deque

from MultiObjectiveOptimization.FJSP_AO.Config.Job import Job, copy_job
from MultiObjectiveOptimization.FJSP_AO.Config.Operation import Assembling_operation
from MultiObjectiveOptimization.FJSP_AO.Util.Pub_func import is_type


def get_machine_available_time(if_allow_forward, machine_finished_times, prev_time_job, prev_time_assembly,
                               processing_time):
    """
    计算机器的可用时间。

    功能：
    - 根据机器的使用时间片段，判断当前操作可以在哪个时间段开始。
    - 如果是主动调度（`if_allow_forward=True`），通过查找机器空闲时间片实现操作的前移优化。
    - 如果是半主动调度（`if_allow_forward=False`），则直接使用机器的最近结束时间作为可用时间。

    调度逻辑：
    1. 如果是主动调度：
        - 调用 `get_idle_times` 方法获取机器的空闲时间片段列表。
        - 遍历空闲时间片段，找到一个满足操作开始条件的时间段。
        - 检查空闲时间片段是否有足够的处理时间容纳当前操作：
            - 计算空闲时间段的实际可用时间，并判断是否满足 `processing_time`。
            - 如果满足，则返回操作的可用开始时间。
        - 如果没有合适的时间片，则返回机器的最后结束时间。
    2. 如果是半主动调度：
        - 直接返回机器的最后结束时间，表示从此时间点开始操作。

    Args:
        if_allow_forward (bool): 是否为主动调度（True 表示主动调度，允许前移优化）。
        machine_finished_times (list of tuple): 机器的使用时间片段列表，每个元素为 (start, end)，表示机器的占用时间段。
        prev_time_job (int): 当前工件前序操作的完成时间，当前操作不能早于此时间开始。
        processing_time (int): 当前操作的处理时间。

    Returns:
        int: 当前操作可以开始的时间。
    """
    if if_allow_forward:
        # 🎈 获取机器的空闲时间片段
        idle_times = get_idle_times(machine_finished_times)
        # 🎈 遍历所有空闲时间片段
        for idle_time in idle_times:
            # 🎈 计算当前时间片段的可用开始时间
            # 操作必须满足前序操作的完成时间
            available_start_time = max(idle_time[0], prev_time_job, prev_time_assembly)
            # 🎈 计算当前时间片段的剩余可用时间
            available_time = idle_time[1] - available_start_time
            # 🎈 如果当前空闲时间片段可以容纳操作，则返回操作的可用开始时间
            if available_time > processing_time:
                return available_start_time
        # 🎈 如果没有合适的空闲时间片，返回机器的最后结束时间
        return machine_finished_times[-1][1]
    else:
        # 🎈 半主动调度，直接返回机器的最后结束时间
        return machine_finished_times[-1][1]


def get_idle_times(machine_finished_times):
    """
    获取机器的空闲时间段。

    功能：
    - 根据机器的已用时间片段，计算所有的空闲时间段。
    - 假设输入的时间片段是有序的，并且表示机器的实际占用时间。

    调度逻辑：
    1. 初始化一个空列表 `idle_times`，用于存储空闲时间段。
    2. 遍历机器的使用时间片段：
        - 如果当前时间片段的开始时间大于前一个时间片段的结束时间，说明有空闲时间段。
        - 将空闲时间段 (prev_end, start) 添加到列表中。
    3. 返回计算得到的空闲时间段列表。

    Args:
        machine_finished_times (list of tuple): 已用时间段列表，每个元素为 (start, end)，
                                                表示某段时间内机器被占用。
                                                假设输入的时间段是有序的。

    Returns:
        list of tuple: 空闲时间段列表，每个元素为 (start, end)，表示机器空闲的时间段。
    """
    # 初始化空闲时间段列表
    idle_times = []

    # 假设机器从时间 0 开始，记录上一个任务的结束时间
    prev_end = 0

    # 遍历已用时间段
    for start, end in machine_finished_times:
        # 🎈 如果当前任务的开始时间大于上一个任务的结束时间，说明有空闲
        if start > prev_end:
            idle_times.append((prev_end, start))  # 添加空闲时间段
        # 🎈 更新上一个任务的结束时间
        prev_end = max(prev_end, end)

    # 🎈 返回所有计算出的空闲时间段
    return idle_times


def get_whole_machine_idle_times(machines_finished_times):
    """
    获取机器的空闲时间段。

    功能：
    - 根据机器的已用时间片段，计算所有的空闲时间段。
    - 假设输入的时间片段是有序的，并且表示机器的实际占用时间。

    调度逻辑：
    1. 初始化一个空列表 `idle_times`，用于存储空闲时间段。
    2. 遍历机器的使用时间片段：
        - 如果当前时间片段的开始时间大于前一个时间片段的结束时间，说明有空闲时间段。
        - 将空闲时间段 (prev_end, start) 添加到列表中。
    3. 返回计算得到的空闲时间段列表。

    Args:
        machine_finished_times (list of tuple): 已用时间段列表，每个元素为 (start, end)，
                                                表示某段时间内机器被占用。
                                                假设输入的时间段是有序的。

    Returns:
        list of tuple: 空闲时间段列表，每个元素为 (start, end)，表示机器空闲的时间段。
    """
    # 初始化空闲时间段列表
    idle_times = [[] for _ in machines_finished_times]

    # 遍历已用时间段
    for i, machine in enumerate(machines_finished_times):
        prev_end = 0
        for start, end in machine:
            # 🎈 如果当前任务的开始时间大于上一个任务的结束时间，说明有空闲
            if start > prev_end:
                idle_times[i].append((prev_end, start))  # 添加空闲时间段
            # 🎈 更新上一个任务的结束时间
            prev_end = max(prev_end, end)

    # 🎈 返回所有计算出的空闲时间段
    return idle_times


def get_job_delay_times(job_finished_times):
    """
    计算每个作业的空闲时间段。

    功能：
    - 根据作业的完成时间段，计算每个作业的空闲时间段。
    - 假设输入的时间段是有序的，并且表示作业的实际占用时间。

    计算逻辑：
    1. 初始化一个空列表 `idle_times`，用于存储每个作业的空闲时间段。
    2. 遍历每个作业的完成时间段：
        - 如果当前时间段的开始时间大于上一个时间段的结束时间，说明有空闲时间段。
        - 将空闲时间段 (prev_end, start) 添加到对应作业的空闲时间列表中。
        - 更新上一个时间段的结束时间。
    3. 返回所有作业的空闲时间段列表。

    参数:
        job_finished_times (list of list of tuple):
            每个作业的完成时间段列表，外层列表包含多个作业，每个作业的时间段为一个列表。
            时间段的格式为 (start, end)，表示作业在某段时间内的运行时间。
            假设输入的时间段是有序的。

    返回值:
        list of list of tuple:
            每个作业的空闲时间段列表，外层列表包含多个作业，每个作业的空闲时间段为一个列表。
            每个空闲时间段的格式为 (start, end)，表示该作业的空闲时间段。
    """
    # 初始化空闲时间段列表
    idle_times = [[] for _ in job_finished_times]

    # 遍历每个作业的完成时间段
    for i, job in enumerate(job_finished_times):
        prev_end = 0  # 初始化上一个时间段的结束时间
        for start, end in job:
            # 如果当前时间段的开始时间大于上一个时间段的结束时间，计算空闲时间段
            if start > prev_end:
                idle_times[i].append((prev_end, start))  # 添加空闲时间段
            # 更新上一个时间段的结束时间
            prev_end = max(prev_end, end)

    # 返回所有作业的空闲时间段列表
    return idle_times


class Decode:
    """
    Decode类用于生成柔性作业车间调度方案，支持三种调度方式：
    1. 半主动调度（Semi-active scheduling）：按照给定顺序和机器选择，尽早安排操作。
    2. 主动调度（Active scheduling）：调整冲突，优化调度。
    3. 全主动调度（Fully active scheduling）：动态选择操作和机器，实现全局优化。
    """

    def __init__(self, jobs, machines, assemble_styles, need_styles):
        """
        初始化Decode类实例。

        功能：
        - 将传入的工件列表、机器列表和装配规则列表初始化到类实例中。
        - 深拷贝工件列表，避免直接修改传入的工件对象。
        - 初始化机器信息和装配规则，分别作为类的属性保存。
        - 清空每个工件的操作队列，为后续调度操作做准备。

        Args:
            jobs (list): 工件对象列表，表示待调度的所有工件，每个工件包含多个操作（operations）。
            machines (list): 机器对象列表，表示可用的所有机器，每台机器可以执行不同的操作。
            assemble_styles (list): 装配规则列表，定义了装配操作所需的规则，比如需要的工件类型和匹配条件。

        变量初始化过程：
        - `self.jobs`：将传入的工件对象列表深拷贝后存储，确保操作过程中不会修改原始数据。
        - `self.machines`：简单复制传入的机器列表，用于调度时的机器分配。
        - `self.assemble_styles`：复制传入的装配规则列表，用于装配操作的匹配逻辑。

        细节说明：
        - 使用 `copy_job(job)` 方法对每个工件对象进行深拷贝，确保每个工件在调度中的状态变化互不影响。
        - 调用每个工件对象的 `clear_ops()` 方法，清空其操作队列，为新的调度过程重新初始化操作。
        """
        self.jobs = []  # 🎈 初始化工件列表，用于存储所有待调度的工件
        for job in jobs:
            self.jobs.append(copy_job(job))  # 🎈 深拷贝每个工件对象，确保调度过程中的独立性
        # 🎈 清空每个工件的操作队列，为调度过程做准备
        for job in self.jobs:
            job.clear_ops()
        # 🎈 初始化机器列表，存储所有可用机器的信息
        self.machines = machines.copy()
        self.assemble_styles = assemble_styles.copy()  # 🎈 初始化装配规则列表，用于装配操作的规则匹配
        self.need_styles = need_styles.copy()
        self.job_finished_times = [[] for _ in jobs]
        self.machines_energy_usage = [0 for _ in machines]
        self.machines_idle_energy_usage = [0 for _ in machines]
        self.job_delay_time = []
        self.assemble_jobs = []

    def run_semi_active_schedule(self, temp_sequence, machine_selection, assembly_selection):
        """
        半主动调度：按照给定顺序尽早安排操作（不进行前移优化）。

        调度逻辑：
        - 使用 `run_schedule` 方法完成半主动调度。
        - 设置 `if_allow_forward=False`，表示不进行前移优化。

        Args:
            temp_sequence (list): 操作顺序列表，表示全局操作的执行顺序。
                                  每个元素为全局操作索引，定义了解码顺序。
            machine_selection (list): 每个操作对应的机器选择策略列表。
                                      每个元素为机器索引，表示该操作分配的机器。

        Returns:
            None
        """
        self.run_schedule(temp_sequence, machine_selection, assembly_selection, False)

    def run_active_schedule(self, temp_sequence, machine_selection, assembly_selection):
        """
        主动调度：通过前移优化等待时间。

        调度逻辑：
        - 使用 `run_schedule` 方法完成主动调度。
        - 设置 `if_allow_forward=True`，表示执行前移优化。

        Args:
            temp_sequence (list): 操作顺序列表，表示全局操作的执行顺序。
                                  每个元素为全局操作索引，定义了解码顺序。
            machine_selection (list): 每个操作对应的机器选择策略列表。
                                      每个元素为机器索引，表示该操作分配的机器。

        Returns:
            None
        """
        self.run_schedule(temp_sequence, machine_selection, assembly_selection, True)

    def run_schedule(self, temp_sequence, machine_selection, assembly_selection, if_allow_forward):
        """
        核心调度方法：支持半主动调度和主动调度。

        根据 `if_allow_forward` 参数决定是否进行主动调度（即前移优化）。
        - 当 `if_allow_forward=False` 时，执行半主动调度：
            - 按照固定的操作顺序和机器分配，尽早安排操作。
        - 当 `if_allow_forward=True` 时，执行主动调度：
            - 在尽早安排操作的基础上，动态前移任务，优化等待时间。

        调度逻辑：
        1. 初始化所需的工件、机器完成时间记录和装配队列。
        2. 遍历给定的操作顺序（temp_sequence），逐步调度每个操作。
        3. 对于每个操作：
            - 检查装配操作是否满足条件（如有）。
            - 如果是主动调度（if_allow_forward=True），执行前移逻辑。
            - 调用 `_schedule_operation` 方法安排操作，更新完成时间记录。
        4. 通过动态优化减少等待时间，提高资源利用率。

        Args:
            temp_sequence (list): 操作顺序列表，表示全局操作的执行顺序。
                                  每个元素为全局操作索引，定义了解码顺序。
            machine_selection (list): 每个操作对应的机器选择策略列表。
                                      每个元素为机器索引，表示该操作分配的机器。
            if_allow_forward (bool): 是否进行主动调度（前移优化）。
                               - False：执行半主动调度。
                               - True：执行主动调度。

        Returns:
            None
            @param if_allow_forward:
            @param temp_sequence:
            @param machine_selection:
            @param assembly_selection:
        """
        # --------------- ✌️准备所需数据(begin)✌️ ---------------
        # 🎈 工件的完成时间记录
        # 每个工件有一个完成时间记录列表，以工件的释放时间（release_time）初始化。
        # 例如：job_finished_times[job_id - 1] 会存储该工件每个操作的完成时间。
        self.job_finished_times = [[(0, job.release_time)] for job in self.jobs]

        # 🎈 每台机器的完成时间记录
        # 每台机器有一个完成时间记录列表，初始化为0，表示机器最早从时间0开始可用。
        # 例如：machines_finished_times[machine_id - 1] 存储每台机器的完成时间。
        machines_finished_times = [[(0, 0)] for _ in self.machines]
        self.assemble_jobs = self.get_assembly_jobs(assembly_selection)
        # 🎈 装配队列
        # 用于管理装配操作时的工件等待队列。根据装配规则中的工件类型进行分组。
        # 每种工件类型都有一个队列，记录需要装配的工件。
        assembly_queue = self._initialize_assembly_queue()

        # 🎈 根据作业顺序（temp_sequence）生成实际的操作调度顺序。
        # `temp_sequence` 是全局操作索引，将其转换为工件ID列表，便于逐工件处理。
        # 例如：[3, 2, 1] -> [工件3的操作, 工件2的操作, 工件1的操作]。
        operation_sequencing = self.sequence_operations_by_job(temp_sequence)
        # --------------- ✌️准备所需数据(end)✌️ ---------------

        # --------------- ✌️调度所有工序(begin)✌️ ---------------
        # 遍历调度顺序，依次调度每个操作。
        for op_index in range(len(operation_sequencing)):
            # 🎈 获取当前操作对应的工件ID。
            job_id = operation_sequencing[op_index]
            # if job_id == 10 or job_id == 12:
            #     print()

            # 🎈 通过工件完成时间列表的长度推导当前操作ID。

            op_id = len(self.job_finished_times[job_id - 1])

            # 🎈 获取当前工件和操作对象。
            job = self.jobs[job_id - 1]

            # 相当于这个工序已经完成了
            if op_id > len(job.ops):
                continue

            op = job.ops[op_id - 1]

            # 🎈 初始化装配完成时间。
            prev_time_assembly = -1  # 默认为 -1，表示无需装配。
            job_need = None
            # 🎈 检查当前操作是否为装配操作。
            if is_type(op, Assembling_operation):
                # 检查是否可以进行装配操作。
                prev_time_assembly, job_need = self._can_assemble(job, op, assembly_queue, self.job_finished_times)

                if prev_time_assembly < 0:
                    # 如果装配条件未满足, 记录该工件最新的完成时间, 并跳过。
                    # job_finished_times[job_id - 1].append(job_finished_times[job_id - 1][-1])
                    continue

            # 🎈 调度当前操作。
            # 调度的核心逻辑：包括计算开始时间、结束时间，更新机器和工件完成时间。
            self._schedule_operation(
                job_id,  # 当前操作所属的工件ID。
                job_need,
                op_id,  # 当前操作在工件中的操作ID。
                op,  # 当前操作对象。
                self.job_finished_times,  # 工件完成时间记录。
                machines_finished_times,  # 机器完成时间记录。
                prev_time_assembly,  # 装配操作的依赖完成时间。
                machine_selection,  # 机器选择策略。
                if_allow_forward  # 是否前移，主动或者全主动会用
            )
            # if op_index > 115:
            #     plot_gantt_chart(self.jobs, self.machines, "active")
            #     print()
        idle_list = get_whole_machine_idle_times(machines_finished_times)
        # 🎈 计算每台机器的空闲时间总长度
        # 获取每台机器的空闲时间段（start, end）列表，遍历计算总的空闲时间。
        idle_durations = []
        for i, machine in enumerate(idle_list):
            total_idle_time = 0
            for start, end in machine:
                total_idle_time += end - start  # 计算每个空闲时间段的持续时间
            idle_durations.append(total_idle_time)

        # # 🎈 计算空闲能耗
        # # 遍历每台机器，根据其空闲时间长度和空闲功率，计算空闲能耗。
        # for i in range(len(idle_durations)):
        #     idle_power = self.get_idle_power_by_machine(i + 1)  # 获取第 i+1 台机器的空闲功率
        #     idle_energy = idle_power * idle_durations[i]  # 空闲能耗 = 空闲功率 * 空闲时间
        #     self.machines_idle_energy_usage[i] = idle_energy  # 更新对应机器的空闲能耗记录
        # # 获取每个作业的延迟时间
        # job_delay_time = get_job_delay_times(self.job_finished_times)
        #
        # # 遍历每个作业的延迟时间
        # for i, job in enumerate(job_delay_time):
        #     total_idle_time = 0  # 初始化当前作业的总空闲时间
        #     # 遍历作业的每个空闲时间段
        #     for start, end in job:
        #         total_idle_time += end - start  # 计算每个空闲时间段的持续时间，并累加到总空闲时间
        #     # 将当前作业的总空闲时间添加到延迟时间列表中
        #     self.job_delay_time.append(total_idle_time)
        # # print()

    def get_assembly_jobs(self, assembly_selection):
        """
        根据给定的装配任务选择，更新并返回一个新的二维数组，表示每个样式的任务编号。

        :param assembly_selection: 一个列表，包含选择的任务索引，表示将要分配的任务。
        :return: 一个二维列表，包含任务编号的分配情况。每个位置如果找到匹配的任务，
                 则存储任务的索引；否则为 -1，表示没有任务匹配该位置的样式需求。
        """
        # 创建一个与 self.need_styles 结构相同的二维数组，初始值为 -1
        ret = [[-1 for _ in row] for row in self.need_styles]

        # 遍历装配选择的任务
        for job_index in assembly_selection:
            job = self.jobs[job_index]  # 获取当前任务对象
            flag = False  # 标志位，用于标记任务是否已经成功匹配

            # 遍历所有样式需求的二维数组
            for i, styles in enumerate(self.need_styles):
                for j, style in enumerate(styles):
                    # 如果当前需要的位置还没有被填充，并且该样式与当前任务样式匹配
                    if ret[i][j] == -1 and self.need_styles[i][j] == job.style:
                        ret[i][j] = job_index + 1  # 将该位置更新为任务的索引
                        flag = True  # 设置标志位，表示任务已经匹配成功
                        break  # 跳出内层循环，继续检查下一个任务
                if flag:
                    break  # 如果任务匹配成功，跳出外层循环，继续处理下一个任务

        return ret  # 返回更新后的任务分配情况

    # 目标函数计算
    def calculate_makespan(self):
        """
        计算 fitness function（最后一道工序的结束时间）。
        """
        if not self.job_finished_times:
            raise ValueError("调度尚未运行，job_finished_times 为空。请先运行调度方法。")

        # 获取每个工件的最后完成时间
        last_time = max(times[-1][1] for times in self.job_finished_times if times)
        return last_time

    def calculate_running_energy_usage(self):
        """
        计算所有机器的总能量消耗。

        Returns:
            list: 每台机器的总能量消耗。
        """
        return self.machines_energy_usage

    def calculate_idle_energy_usage(self):
        """
        计算所有机器在空闲状态下的总能耗。

        该方法从 `machines_idle_energy_usage` 属性中获取机器在空闲状态下的能耗指标，
        并返回总的空闲能耗。

        返回值:
            float: 所有机器在空闲时间的总能耗。
        """
        return self.machines_idle_energy_usage

    def calculate_job_delay_time(self):
        """
        计算所有作业的总延迟时间。

        该方法基于 `job_delay_time` 属性，返回所有作业的累计延迟时间。

        返回值:
            float: 所有作业的总延迟时间。
        """
        return self.job_delay_time

    def run_fully_active_schedule(self):
        """
        全主动调度：动态选择操作和机器，进行全局优化。
        """
        pass

    def _initialize_assembly_queue(self):
        """
        🛠️ 初始化装配队列 🛠️

        功能：
        - 创建一个装配队列字典，用于管理装配操作的工件等待队列。
        - 装配队列的每个键是工件类型（由装配规则定义），
          值是一个双端队列（deque），用于存储等待装配的工件。

        设计目的：
        - 支持装配操作时不同工件类型的管理和配对需求。
        - 保证每种工件类型在装配队列中都有对应的队列，即使初始为空。

        Returns:
            dict: 包含所有工件类型及其等待队列的装配队列字典。
        """

        # 🎈 创建一个空字典，用于存储装配队列
        # 键（key）：工件类型（如param1或param2）
        # 值（value）：该工件类型的双端队列（deque）
        assembly_queue = {}

        # 🎈 遍历装配规则，依次处理每个装配需求
        # - 每个装配规则定义了两种需要配对的工件类型：param1 和 param2
        for style in self.assemble_styles:
            # 💙 确保字典中存在param1、2对应的队列，如果不存在则创建一个空队列
            assembly_queue.setdefault(style.param1, deque())
            assembly_queue.setdefault(style.param2, deque())

        return assembly_queue

    def _schedule_operation(self, job_id, job_need, op_id, op, job_finished_times, machines_finished_times,
                            prev_time_assembly,
                            machine_selection, if_allow_forward):
        """
        🛠️ 调度单个操作 🛠️

        功能：
        - 负责调度单个操作（operation），计算其开始时间和结束时间。
        - 根据工件和机器的完成时间更新操作的调度状态。
        - 更新工件和机器的完成时间列表，确保下一操作能够正确推导。

        调度逻辑：
        1. 获取当前操作的全局索引，确定其对应的机器。
        2. 根据选择的机器，获取该机器的处理时间。
        3. 计算操作的开始时间：
            - 满足工件的前序操作完成时间。
            - 满足所选机器的最早空闲时间。
            - 满足装配依赖条件（如果有装配操作）。
        4. 根据开始时间和处理时间，计算操作的结束时间。
        5. 更新完成时间记录：
            - 更新工件完成时间列表（job_finished_times）。
            - 更新机器完成时间列表（machine_finished_times）。
        6. 调用操作的更新方法，记录调度结果。

        Args:
            job_id (int): 当前操作所属工件的ID。
            op_id (int): 当前操作在工件中的操作ID。
            op (Operation): 当前操作对象，包含操作的详细信息。
            job_finished_times (list): 工件完成时间记录，每个工件有独立的完成时间列表。
            machines_finished_times (list): 机器完成时间记录，每台机器有独立的完成时间列表。
            prev_time_assembly (int): 装配依赖完成时间，默认为 -1 表示无装配依赖。
            machine_selection (list): 机器选择策略，为每个操作选择对应的机器索引。

        Returns:
            None
        """
        # 🎈 获取当前操作的全局索引
        # 全局索引通过工件ID和操作ID推导，表示在全局调度顺序中的位置
        op_global_index = self.get_op_index(job_id, op_id)

        # 🎈 根据全局索引获取当前操作的机器索引
        # 从机器选择策略中获取当前操作分配的机器索引
        machine_index = machine_selection[op_global_index]

        # 🎈 确定当前操作分配的机器
        # `available_machines` 存储了当前操作可以使用的所有机器
        # 选择的机器由机器索引决定
        machine = op.available_machines[machine_index][0]

        # 🎈 获取当前操作在指定机器上的处理时间
        # 不同机器可能具有不同的处理时间
        processing_time = op.get_processing_time_by_machine(machine)
        # 求机器加工过程消耗的能量
        # energy_used = self.get_run_power_by_machine(machine) * processing_time

        # 🎈 获取当前工件的上一个操作的完成时间
        # job_finished_times[job_id - 1][-1] 表示该工件的最新完成时间
        prev_time_job = job_finished_times[job_id - 1][-1][1]

        # 🎈 获取当前机器的最近完成时间
        # machines_finished_times[machine - 1][-1] 表示该机器的最新完成时间
        prev_time_machine = get_machine_available_time(if_allow_forward, machines_finished_times[machine - 1],
                                                       prev_time_job,
                                                       prev_time_assembly,
                                                       processing_time)

        # 🎈 计算操作的开始时间
        # 开始时间需要满足以下条件：
        # 1. 工件的前序操作完成时间（prev_time_job）。
        # 2. 当前机器的最早空闲时间（prev_time_machine）。
        # 3. 装配条件完成时间（prev_time_assembly）。
        start_time = max(prev_time_job, prev_time_machine, prev_time_assembly)

        # 🎈 计算操作的结束时间
        # 结束时间 = 开始时间 + 当前操作的处理时间
        end_time = start_time + processing_time

        # 🎈 更新工件完成时间记录
        # 将当前操作的完成时间记录到对应的工件完成时间列表中

        if job_need is not None:
            # 能装配
            for job in job_need.assembly_jobs:
                job_finished_times[job.id - 1].append((start_time, end_time))
        else:
            # 不能装配
            job_finished_times[job_id - 1].append((start_time, end_time))

        # 🎈 更新机器完成时间记录
        # 将当前操作的完成时间记录到对应的机器完成时间列表中
        machines_finished_times[machine - 1].append((start_time, end_time))
        machines_finished_times[machine - 1].sort(key=lambda x: x[0])

        # 🎈 累加能量消耗到对应机器
        # self.machines_energy_usage[machine - 1] += energy_used

        # 🎈 调用操作的更新方法
        # 更新操作对象的调度信息，记录分配的机器、开始时间和结束时间
        op.update(machine, start_time, end_time)

    def get_op_index(self, job_id, op_id):
        """
        获取全局操作索引。

        功能：
        - 计算某个操作在全局操作列表中的索引。
        - 索引是基于所有工件的操作总和，按工件顺序累加计算的。

        调度背景：
        - 调度中需要根据全局索引来选择机器和操作，而操作索引是按照工件的操作顺序来推导的。

        计算逻辑：
        - 遍历 `self.jobs` 中从第 1 个工件到当前工件（`job_id - 1`）的所有操作数量。
        - 将这些操作数量相加，得到当前工件之前所有操作的总数。
        - 加上当前工件的 `op_id`（当前工件的第几个操作）并减去 1，得到全局索引。

        Args:
            job_id (int): 工件ID，从1开始编号。
            op_id (int): 操作ID，从1开始编号，表示工件中的第几个操作。

        Returns:
            int: 全局操作索引，表示该操作在所有工件的操作列表中的位置（从0开始计数）。
        """
        # 🎈 遍历从第 1 个工件到当前工件（job_id - 1）之前的所有工件
        # 使用 job.get_num_ops() 获取每个工件的操作数量，累加得到总操作数
        num_previous_ops = sum(job.get_num_ops() for job in self.jobs[:job_id - 1])

        # 🎈 加上当前工件的操作ID（op_id），再减去 1，得到全局索引
        global_op_index = num_previous_ops + op_id - 1

        # 🎈 返回计算后的全局索引
        return global_op_index

    def sequence_operations_by_job(self, job_sequence):
        """
        根据顺序返回工件ID。

        功能：
        - 根据输入的全局操作索引序列（`job_sequence`），返回对应的工件ID列表。
        - 该方法将所有操作按工件拆解，以便逐个工件处理调度。

        调度背景：
        - 在调度算法中，操作调度需要映射到具体的工件。该方法用于将全局索引映射为工件ID。

        实现逻辑：
        - 遍历所有工件的操作列表，提取每个操作对应的工件ID，形成全局操作到工件ID的映射表。
        - 按照 `job_sequence` 中的顺序，查找对应的工件ID，生成工件ID列表。

        Args:
            job_sequence (list): 操作顺序列表，每个元素是全局操作的索引。

        Returns:
            list: 工件ID顺序，表示每个全局操作索引对应的工件ID。
        """
        # 🎈 遍历所有工件的操作，生成全局操作索引对应的工件ID列表
        # operation_job_ids 是一个长度为所有操作数的列表，存储了每个操作的工件ID
        operation_job_ids = [operation.job_id for job in self.jobs for operation in job.ops]

        # 🎈 根据 `job_sequence` 中的全局操作索引，查找对应的工件ID
        # 将 `job_sequence` 转换为工件ID列表
        job_id_sequence = [operation_job_ids[index] for index in job_sequence]

        # 🎈 返回工件ID顺序列表
        return job_id_sequence

    def _can_assemble(self, job, op, assembly_queue, job_finished_times):
        """
        检查是否满足装配条件。

        功能：
        - 判断当前操作是否可以作为装配操作执行。
        - 检查当前工件是否满足装配规则的依赖条件。
        - 如果装配条件满足，则完成装配，并更新操作信息。
        - 如果装配条件不满足，则将当前工件加入等待队列。

        逻辑：
        1. 从当前操作的装配规则中获取配对所需的两种工件类型（param1 和 param2）。
        2. 根据当前工件的类型，判断需要的另一种工件类型。
        3. 检查装配队列中是否存在所需的另一种工件：
            - 如果存在，从队列中取出该工件，完成装配操作，并更新相关信息。
            - 如果不存在，将当前工件加入等待队列，并返回 -1 表示装配条件不满足。

        Args:
            job (Job): 当前工件对象，表示当前需要判断的工件。
            op (Operation): 当前操作对象，表示需要调度的操作。
            assembly_queue (dict): 装配队列，用于管理不同类型工件的等待队列。
                                   键为工件类型，值为该类型工件的双端队列。
            job_finished_times (list): 工件完成时间记录，每个工件的完成时间列表。

        Returns:
            int: 如果装配条件满足，返回所需工件的完成时间；如果不满足，返回 -1。
        """
        # 🎈 获取当前操作的装配规则
        # 每个装配操作都有特定的装配规则（assemble_style），定义需要配对的工件类型
        cur_assemble_style = op.assemble_style

        # 🎈 获取当前工件的类型
        # 工件类型决定了当前工件是装配规则中的哪种类型（param1 或 param2）
        job_style = job.style

        # 🎈 从装配规则中获取所需的两种工件类型
        # param1 和 param2 是需要配对的工件类型
        param1 = cur_assemble_style.param1
        param2 = cur_assemble_style.param2

        # 🎈 确定所需的另一种工件类型
        # 如果当前工件的类型是 param1，则需要另一种类型为 param2，反之亦然
        param = param2 if job_style == param1 else param1

        # 🎈 尝试获取当前工件类型的队列
        # 如果队列不存在，则创建一个空队列（防止 KeyError）
        try:
            deque_self = assembly_queue[job_style]
        except KeyError:
            deque_self = deque()  # 如果当前工件类型队列不存在，则初始化为空

        # 🎈 获取所需的另一种工件类型的队列
        deque_need = assembly_queue[param]

        # 🎈 检查所需工件队列是否为空
        # 如果所需工件的队列为空，则将当前工件加入自身队列，并返回 -1
        if not deque_need:
            # 如果当前工件尚未在自身队列中，则将其加入等待队列
            # if job not in deque_self :
            #     deque_self.append(job)
            if job not in deque_self and all(assembly_job not in deque_self for assembly_job in job.assembly_jobs):
                deque_self.append(job)

            return -1, None

        list_need = []
        for jobs in self.assemble_jobs:
            if job.id in jobs:
                for job_id in jobs:
                    list_need.append(self.jobs[job_id - 1])
                break

        if set(list_need) & set(deque_need):  # 或者使用 .intersection() 方法
            job_need = next(iter(set(list_need) & set(deque_need)))
        else:
            if job not in deque_self and all(assembly_job not in deque_self for assembly_job in job.assembly_jobs):
                deque_self.append(job)
            return -1, None

        # 🎈 从所需工件队列中取出一个工件
        # 如果存在满足条件的工件，从队列中弹出该工件，表示匹配成功
        # job_need = deque_need.pop()
        deque_need.remove(job_need)

        # 🎈 更新当前操作的装配信息
        # 记录装配操作的详细信息，包括装配规则名、当前工件ID和匹配工件ID
        op.assemble_jobs.append((cur_assemble_style.name, job.id, job_need.id))

        # 🎈 更新当前工件的类型
        # 装配完成后，当前工件的类型变更为装配规则所定义的新类型
        job.style = cur_assemble_style
        job_need.style = cur_assemble_style
        job.assembly_jobs.add(job_need)
        job_need.assembly_jobs.add(job)

        assembly_jobs = set()

        for job_as_self in job.assembly_jobs:
            for job_as_need in job_need.assembly_jobs:
                assembly_jobs.add(job_as_self)
                assembly_jobs.add(job_as_need)
        for job_ in assembly_jobs:
            self.jobs[job_.id - 1].style = cur_assemble_style
            self.jobs[job_.id - 1].assembly_jobs = assembly_jobs
        # print()

        # 🎈 获取所需工件的完成时间
        # 用于判断当前操作的开始时间，确保装配依赖条件满足
        prev_time_assembly = job_finished_times[job_need.id - 1][-1][1]

        # 🎈 返回装配依赖的完成时间
        # 如果装配条件满足，则返回装配依赖的工件完成时间
        return prev_time_assembly, job_need

    def get_run_power_by_machine(self, machine_index):
        """
        通过机器号获取机器的加工功率。

        Args:
            machine_index (int): 机器号。

        Returns:
            int: 对应机器的加工能量。如果机器不存在，返回 -1。
        """
        return next((machine.run_power for machine in self.machines if machine.id == machine_index), -1)

    def get_idle_power_by_machine(self, machine_index):
        """
        通过机器号获取机器的加工功率。

        Args:
            machine_index (int): 机器号。

        Returns:
            int: 对应机器的加工能量。如果机器不存在，返回 -1。
        """
        return next((machine.idle_power for machine in self.machines if machine.id == machine_index), -1)
