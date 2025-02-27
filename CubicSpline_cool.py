#构造样条插值
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
import sympy as sp

# 示例数据点
#all
x_data = np.array([0,279.6,201.0,163.4,121.0,111.0,65.0,323.4,373.4,401.3,449.9,499.9,550.3,599.3,650.3,699.3,751.3,799.3,849.3,902.8,949.8,1004.8])
y_data = np.array([0,0.254,0.191,0.158,0.120,0.109,0.066,0.287,0.322,0.341,0.371,0.400,0.426,0.450,0.471,0.490,0.507,0.520,0.531,0.540,0.546,0.550])

# 将 x_data 和 y_data 组合成二维数组
data = np.column_stack((x_data, y_data))

# 按第一列（x_data）排序
sorted_data = data[data[:, 0].argsort()]

# 分离有序数据
x_data = sorted_data[:, 0]
y_data = sorted_data[:, 1]

# 定义符号变量
x = sp.symbols('x')

# 拉格朗日插值函数
def lagrange_interpolation(x_data, y_data):
    n = len(x_data)
    L = 0
    for i in range(n):
        # 计算每个基多项式
        term = y_data[i]
        for j in range(n):
            if j != i:
                term *= (x - x_data[j]) / (x_data[i] - x_data[j])
        L += term
    return L

# 计算插值函数
interpolation_function = lagrange_interpolation(x_data, y_data)

# 展示插值函数表达式
print("Lagrange Interpolation Function:")
print(sp.simplify(interpolation_function))

