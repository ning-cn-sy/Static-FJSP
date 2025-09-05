from ExactAlgorithm.Config.Job import Job
from ExactAlgorithm.Config.Machine import Machine
from ExactAlgorithm.Config.Operation import Operation


def readDataByFJS(fileNameFjs):
    file = open(fileNameFjs, "r")
    # 读第一行
    # basicInformation = file.readline().strip().split("\t")
    basicInformation = file.readline().strip().split("  ")
    # 工件数量 机器数量
    numJob = basicInformation[0]
    numMachine = basicInformation[1]

    job_list = []
    machine_list = []

    # 遍历每个工件
    for name in range(int(numJob)):
        result = file.readline().strip().split("  ")
        # sum_process 当前工件的工序数  int()类型
        sum_process = result[0]
        code = result[1].strip().split(" ")
        index = 0
        job_id = name + 1
        job_list.append(Job(job_id))
        job_list[name].op_list = []
        #  当前工件的工序列表
        for a in range(int(sum_process)):
            id = a + 1
            count = code[index]
            index += 1
            available_machines_am = {}
            for i in range(int(count)):
                machine = int(code[index])
                time = int(code[index + 1])
                available_machines_am[(machine, 0)] = time
                #  下一个使用的机器和时间
                index += 2
            #  op_list 找的不对
            job_list[name].op_list.append(Operation(id, job_id, available_machines_am, Job(job_id)))

    for name in range(int(numMachine)):
        machine_list.append(Machine(name + 1))

    return job_list, machine_list


if __name__ == '__main__':
    readDataByFJS("D:\pythonlearning\FJSP_MR\Example\Mk01_MR.fjs")
