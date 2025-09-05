# -*- coding: utf-8 -*-
# @Time    : 2025/1/5 14:58
# @Author  : 宁诗铎
# @Site    : 
# @File    : Decode.py
# @Software: PyCharm 
# @Comment : 解码
from MultiObjectiveOptimization.FJSP.Config.Job import copy_job
from MultiObjectiveOptimization.FJSP.Util.Draw_gantt import plot_gantt_chart


def get_machine_available_time(if_allow_forward, machine_finished_times, prev_time_job, processing_time):
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
            available_start_time = max(idle_time[0], prev_time_job)
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


class Decode:
    """
    Decode类用于生成柔性作业车间调度方案，支持三种调度方式：
    1. 半主动调度（Semi-active scheduling）：按照给定顺序和机器选择，尽早安排操作。
    2. 主动调度（Active scheduling）：调整冲突，优化调度。
    3. 全主动调度（Fully active scheduling）：动态选择操作和机器，实现全局优化。
    """

    def __init__(self, jobs, machines):
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
        self.job_finished_times = None

    def run_semi_active_schedule(self, temp_sequence, machine_selection):
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
        self.run_schedule(temp_sequence, machine_selection, False)

    def run_schedule(self, temp_sequence, machine_selection, if_allow_forward):
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
        """
        # --------------- ✌️准备所需数据(begin)✌️ ---------------
        # 🎈 工件的完成时间记录
        # 每个工件有一个完成时间记录列表，以工件的释放时间（release_time）初始化。
        # 例如：job_finished_times[job_id - 1] 会存储该工件每个操作的完成时间。
        self.job_finished_times = [[job.release_time] for job in self.jobs]

        # 🎈 每台机器的完成时间记录
        # 每台机器有一个完成时间记录列表，初始化为0，表示机器最早从时间0开始可用。
        # 例如：machines_finished_times[machine_id - 1] 存储每台机器的完成时间。
        machines_finished_times = [[(0, 0)] for _ in self.machines]


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

            # 🎈 调度当前操作。
            # 调度的核心逻辑：包括计算开始时间、结束时间，更新机器和工件完成时间。
            self._schedule_operation(
                job_id,  # 当前操作所属的工件ID。
                op_id,  # 当前操作在工件中的操作ID。
                op,  # 当前操作对象。
                self.job_finished_times,  # 工件完成时间记录。
                machines_finished_times,  # 机器完成时间记录。
                machine_selection,  # 机器选择策略。
                if_allow_forward  # 是否前移，主动或者全主动会用
            )
            # plot_gantt_chart(self.jobs, self.machines)
            # print()

    def calculate_fitness(self):
        """
        计算 fitness function（最后一道工序的结束时间）。
        """
        if not self.job_finished_times:
            raise ValueError("调度尚未运行，job_finished_times 为空。请先运行调度方法。")

        # 获取每个工件的最后完成时间
        lasttime = max(times[-1] for times in self.job_finished_times if times)
        return lasttime

        # --------------- ✌️调度所有工序(end)✌️ ---------------

    def run_active_schedule(self, temp_sequence, machine_selection):
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
        self.run_schedule(temp_sequence, machine_selection, True)

    def run_fully_active_schedule(self):
        """
        全主动调度：动态选择操作和机器，进行全局优化。
        """
        pass


    def _schedule_operation(self, job_id, op_id, op, job_finished_times, machines_finished_times,
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

        # 🎈 获取当前工件的上一个操作的完成时间
        # job_finished_times[job_id - 1][-1] 表示该工件的最新完成时间
        prev_time_job = job_finished_times[job_id - 1][-1]

        # 🎈 获取当前机器的最近完成时间
        # machines_finished_times[machine - 1][-1] 表示该机器的最新完成时间
        prev_time_machine = get_machine_available_time(if_allow_forward, machines_finished_times[machine - 1],
                                                       prev_time_job,
                                                       processing_time)

        # 🎈 计算操作的开始时间
        # 开始时间需要满足以下条件：
        # 1. 工件的前序操作完成时间（prev_time_job）。
        # 2. 当前机器的最早空闲时间（prev_time_machine）。
        # 3. 装配条件完成时间（prev_time_assembly）。
        start_time = max(prev_time_job, prev_time_machine)

        # 🎈 计算操作的结束时间
        # 结束时间 = 开始时间 + 当前操作的处理时间
        end_time = start_time + processing_time

        # 🎈 更新工件完成时间记录

        job_finished_times[job_id - 1].append(end_time)

        # 🎈 更新机器完成时间记录
        # 将当前操作的完成时间记录到对应的机器完成时间列表中
        machines_finished_times[machine - 1].append((start_time, end_time))
        machines_finished_times[machine - 1].sort(key=lambda x: x[0])

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
