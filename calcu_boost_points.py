y=5413 #面板力量 一格共鸣
s=4400 #基础力量
n=y/s #当前力量百分比
rate=1.07


'''
现有游戏的属性：
基础力量z 计算得到 由(s2-s1)/(p2-p1) 其中p2-p1是精确值 误差为0，s2 s1为观测值 误差范围为1
攻击力 a 观测得到 误差范围1
力量倍率p 计算得到 由s/z得到
面板力量s 观测得到 误差范围1 也可由计算得到 s=p*z
其他数值 m 计算得到 由a/(s/1000+1)得到 误差未知
先已有观测的攻击力a2 a1，我要通过攻击力计算公式 a=(p*z/100+1)*m 算出p的变动值，计算其误差范围

final=x*(1+0.05+other+change)*m
x*(1+0.05+other)=y
final=y*m+x*change*m
change=(final-y*m)/x*m

'''

def calculate_output(final, times):
    persent=(final-y)/(times*s)
    return persent/0.05*10000/1.07

# 示例使用：用户输入 final 和 times 值
final_input = input("输入力量 攻击次数 ")
values=final_input.strip().split(" ")
final_input = [float(value) for value in values]
final_value = final_input[0]  # 用户输入的 final 值
times_value = final_input[1]   # 用户输入的 times 值

result = calculate_output(final_value, times_value)
print(f"结果为: {result}")