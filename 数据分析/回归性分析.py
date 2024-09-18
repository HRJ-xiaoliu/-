import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from matplotlib.font_manager import FontProperties

# 设置字体
my_font = FontProperties(fname=r"E:\Edge download\lxgw-wenkai-v1.330\lxgw-wenkai-v1.330\LXGWWenKai-Bold.ttf", size=12)

# 特征数据
X = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]).reshape(-1, 1)
# 目标数据
y = np.array([2, 3, 5, 7, 11, 13, 17, 21, 27, 33])

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 创建线性回归模型
model = LinearRegression()

# 训练模型
model.fit(X_train, y_train)

# 在测试集上进行预测
y_pred = model.predict(X_test)

# 计算均方误差
mse = mean_squared_error(y_test, y_pred)
print(f"均方误差: {mse}")

# 计算决定系数（R^2）
r2 = r2_score(y_test, y_pred)
print(f"决定系数: {r2}")

# 绘制实际值和预测值
plt.scatter(X_test, y_test, color='black', label='实际值')
plt.plot(X_test, y_pred, color='blue', linewidth=3, label='预测值')

# 设置标签和标题
plt.xlabel('特征', fontproperties=my_font)
plt.ylabel('目标', fontproperties=my_font)
plt.title('线性回归示例', fontproperties=my_font)

# 设置刻度标签大小
plt.tick_params(axis='both', labelsize=12)

# 添加图例
plt.legend()

# 显示图形
plt.show()
