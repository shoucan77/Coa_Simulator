import numpy as np
from scipy.optimize import curve_fit

# 数据点
#0-300 0.543 947 RMSE: 0.0005461421411649066
#x_data = np.array([0,293.4,273.4,279.6,201.0,163.4,121.0,111.0,65.0])
#y_data = np.array([0,0.265,0.250,0.254,0.191,0.158,0.120,0.109,0.066])

#300-600 0.751 878 0.0009929727736950806
#x_data=np.array([323.4,373.4,401.3,449.9,499.9,550.3,599.3])
#y_data=np.array([0.287,0.322,0.341,0.371,0.400,0.426,0.450])

#600-1000 1.248 552 0.00391685959432527
x_data=np.array([650.3,699.3,751.3,799.3,849.3,902.8,949.8,1004.8])
y_data=np.array([0.471,0.490,0.507,0.520,0.531,0.540,0.546,0.550])

#all 0.935 809 0.010233208717944682
#x_data = np.array([0,279.6,201.0,163.4,121.0,111.0,65.0,323.4,373.4,401.3,449.9,499.9,550.3,599.3,650.3,699.3,751.3,799.3,849.3,902.8,949.8,1004.8])
#y_data = np.array([0,0.254,0.191,0.158,0.120,0.109,0.066,0.287,0.322,0.341,0.371,0.400,0.426,0.450,0.471,0.490,0.507,0.520,0.531,0.540,0.546,0.550])

#y_data=np.array([x*100 for x in y_data])
# 定义新的模型函数
def model_pow(x,a,b,c):
    return np.power(x,a)/(b*x+c)

def model1(x,a,b,c):
    return a*x/(b*x+c)

def model2(x,a,b,c):
    return a*x/(b*x+c)

def model(x,a,b):
    return x/(a*x+b)

# 拟合曲线，更新为三个参数
params, covariance = curve_fit(model, x_data, y_data,maxfev=1000000)

# 输出拟合参数
# 输出拟合参数
a, b= params
print(f"拟合参数: a={a:.6f}, b={b:.6f}")

#模型评价
# 计算模型的预测值
y_fit = model(x_data, *params)
# 计算均方根误差 (RMSE)
rmse = np.sqrt(np.mean((y_data - y_fit) ** 2))
print(f"RMSE: {rmse}")
