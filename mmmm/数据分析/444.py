import pandas as pd
import numpy as np

# 1. 读取数据
df = pd.read_csv('数据基础.csv')

# 2. 数据预处理
df['日期'] = pd.to_datetime(df['日期'], format='%Y/%m/%d')
df = df.dropna(subset=['回报率'])
df['回报率'] = df['回报率'].astype(float)

# 3. 创建回报率矩阵
return_matrix = df.pivot(index='日期', columns='代码', values='回报率')
return_matrix = return_matrix.dropna()  # 删除存在缺失值的日期

# 4. 计算每只股票的平均回报率
mean_returns = return_matrix.mean()

# 5. 计算协方差矩阵
cov_matrix = return_matrix.cov()

# 6. 设置等权重
num_stocks = len(return_matrix.columns)
weights = np.array([1 / num_stocks] * num_stocks)

# 7. 计算投资组合的预期回报率
portfolio_return = np.dot(weights, mean_returns)

# 8. 计算投资组合的方差和标准偏差
portfolio_variance = np.dot(weights.T, np.dot(cov_matrix, weights))
portfolio_std_dev = np.sqrt(portfolio_variance)



# 创建包含结果的Data
data = {
    '指标': ['投资组合的预期回报率', '投资组合的标准偏差'],
    '值': [f'{portfolio_return:.4%}', f'{portfolio_std_dev:.4%}']
}

# 将数据转换为DataFrame
results_df = pd.DataFrame(data)

# 将结果写入Excel的同一个Sheet
with pd.ExcelWriter('股票分析结果.xlsx', mode='a', engine='openpyxl') as writer:
    results_df.to_excel(writer, sheet_name='回报组合', index=False)

print("结果已写入股票分析结果.xlsx文件的回报组合表格中")