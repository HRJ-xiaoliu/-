import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# 定义微分方程组
def model(y, t, K):
    N, r = y
    dNdt = r * N * (1 - N / K)  # logistic growth model
    return [dNdt, -r*N]

# 初始条件和参数值
y0 = [1000, 0.03]  # initial population and growth rate
t = np.linspace(0, 100, 1000)  # time points
K = 1000  # carrying capacity

# 解微分方程组
sol = odeint(model, y0, t, args=(K,))
N, r = sol.T  # extract population and growth rate from solution array

# 绘制图形
plt.figure(figsize=(8, 4))
plt.plot(t, N, label='Population')
plt.plot(t, r, label='Growth Rate')
plt.xlabel('Time')
plt.ylabel('Value')
plt.legend()
plt.show()
