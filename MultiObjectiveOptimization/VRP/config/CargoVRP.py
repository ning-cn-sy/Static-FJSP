class Cargo:
    def __init__(self, name, weight, allocatedBin=[], timeWindow=[]):
        self.name = name  # 货物名称
        self.weight = weight  # 重量
        self.allocatedBin = allocatedBin  # 位置  排，列，行
        self.timeWindow = timeWindow

    def deliver(self):
        print(f"The cargo {self.name} has been delivered to {self.allocatedBin}.")
