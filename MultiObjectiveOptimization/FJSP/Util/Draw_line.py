# -*- coding: utf-8 -*-
# @Time    : 2025/1/5 15:52
# @Author  : 宁诗铎
# @Site    : 
# @File    : Draw_line.py
# @Software: PyCharm 
# @Comment : 画折线图


import matplotlib.pyplot as plt


def plot_line(y, title="fitness", xlabel="iters", ylabel="makespan"):
    """
    绘制折线图，只需要传入Y值的列表，X轴自动生成。

    参数:
        y (list): Y轴数据
        title (str): 图表标题
        xlabel (str): X轴标签
        ylabel (str): Y轴标签
    """
    # 自动生成 X 轴
    x = list(range(len(y)))

    # 创建折线图
    plt.plot(x, y, marker='o')

    # 添加标题和标签
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # 显示网格
    plt.grid(True)

    # 显示图形
    plt.show()

