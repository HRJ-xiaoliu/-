import pandas as pd
import numpy as np

# 1. 读取数据
df = pd.read_csv('数据分析\数据基础.csv')

# 2. 数据预处理
df['日期'] = pd.to_datetime(df['日期'], format='%Y/%m/%d')
df = df.dropna(subset=['回报率'])
df['回报率'] = df['回报率'].astype(float)

# 3. 定义计算函数
def geometric_mean(returns):
    returns = returns + 1
    product = returns.prod()
    n = returns.count()
    return product ** (1 / n) - 1

def cumulative_wealth(returns):
    returns = returns + 1
    return returns.prod()

# 4. 分组计算指标
grouped = df.groupby('代码')

arithmetic_mean = grouped['回报率'].mean()
geometric_mean_return = grouped['回报率'].apply(geometric_mean)
std_dev = grouped['回报率'].std()
variance = grouped['回报率'].var()
cumulative_wealth_index = grouped['回报率'].apply(cumulative_wealth)
VaR_95 = grouped['回报率'].quantile(0.05)

# 5. 整理结果
stats = pd.DataFrame({
    '算术平均回报率': arithmetic_mean,
    '几何平均回报率': geometric_mean_return,
    '标准差': std_dev,
    '方差': variance,
    '累积财富指数': cumulative_wealth_index,
    'VaR 95%': VaR_95
})

stats = stats.reset_index()

# 6. 输出结果
print(stats)