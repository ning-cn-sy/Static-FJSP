# -*- coding: utf-8 -*-
# @Time    : 2024/6/27 16:39
# @Author  : 宁诗铎
# @Site    : 
# @File    : name_util.py
# @Software: PyCharm 
# @Comment : 获取名称

def spilt_variable_name(result, i):
    return list(result[i][0].replace("(", "").replace(")", "").replace(",", "").replace(" ", ""))


def t_name(name):
    return f"t{name}"


def c_name(name1, name2):
    return f"C{name1, name2}"


def b_name(name1, name2):
    return f"B{name1, name2}"


def x_name(name1, name2, name3):
    return f"x{name1, name2, name3}"


def y_name(name1, name2, name3, name4):
    return f"y{name1, name2, name3, name4}"


def h_name(name1, name2, name3, name4):
    return f"η{name1, name2, name3, name4}"


def Y_name(name1, name2, name3, name4):
    return f"Y{name1, name2, name3, name4}"


def s_name(name1, name2, name3, name4):
    return f"σ{name1, name2, name3, name4}"


def constraint_name(name1, name2, name3="", name4="", name5="", name6="", name7="", name8="", flag=10):
    # 约束11、12 name8不一样 约束11 的name8是q'  约束12 k'
    ret = "C" + str(name1) + "-i" + str(name2)
    if name3 != "":
        ret = ret + "-j" + str(name3)
    if name4 != "":
        ret = ret + "-i'" + str(name4)
    if name5 != "":
        ret = ret + "-j'" + str(name5)
    if name6 != "":
        ret = ret + "-k" + str(name6)
    if name7 != "":
        ret = ret + "" + str(name7)
    if name8 != "":
        if flag == 0:
            ret = ret + "-q'" + str(name8)
        elif flag == 1:
            ret = ret + "-k'" + str(name8)

    return ret
