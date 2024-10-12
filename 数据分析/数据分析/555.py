import pandas as pd
import numpy as np
from scipy.optimize import minimize

# 1. 读取并预处理数据
df = pd.read_csv('数据分析\数据基础.csv')
df['日期'] = pd.to_datetime(df['日期'], format='%Y/%m/%d')
df = df.dropna(subset=['回报率'])
df['回报率'] = df['回报率'].astype(float)
return_matrix = df.pivot(index='日期', columns='代码', values='回报率')
return_matrix = return_matrix.dropna()

# 2. 计算预期回报率和协方差矩阵
mean_returns = return_matrix.mean()
cov_matrix = return_matrix.cov()
num_stocks = len(mean_returns)

# 3. 定义约束和边界
def portfolio_weights_sum_to_one(weights):
    return np.sum(weights) - 1

bounds = tuple((0, 1) for _ in range(num_stocks))
constraints = ({
    'type': 'eq',
    'fun': portfolio_weights_sum_to_one
})

# 4. 最小方差投资组合
def portfolio_variance(weights, cov_matrix):
    return np.dot(weights.T, np.dot(cov_matrix, weights))

initial_weights = np.array([1 / num_stocks] * num_stocks)

min_variance_result = minimize(
    portfolio_variance,
    initial_weights,
    args=(cov_matrix,),
    method='SLSQP',
    bounds=bounds,
    constraints=constraints
)

min_variance_weights = min_variance_result.x
min_variance_return = np.dot(min_variance_weights, mean_returns)
min_variance_std = np.sqrt(portfolio_variance(min_variance_weights, cov_matrix))

# 月度无风险收益率
risk_free_rate_annual = 0.04
risk_free_rate_monthly = (1 + risk_free_rate_annual) ** (1/12) - 1

min_variance_sharpe = (min_variance_return - risk_free_rate_monthly) / min_variance_std

# 5. 最佳投资组合（最大化夏普比率）
def negative_sharpe_ratio(weights, mean_returns, cov_matrix, risk_free_rate):
    portfolio_return = np.dot(weights, mean_returns)
    portfolio_std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    return -(portfolio_return - risk_free_rate) / portfolio_std

max_sharpe_result = minimize(
    negative_sharpe_ratio,
    initial_weights,
    args=(mean_returns, cov_matrix, risk_free_rate_monthly),
    method='SLSQP',
    bounds=bounds,
    constraints=constraints
)

max_sharpe_weights = max_sharpe_result.x
max_sharpe_return = np.dot(max_sharpe_weights, mean_returns)
max_sharpe_std = np.sqrt(np.dot(max_sharpe_weights.T, np.dot(cov_matrix, max_sharpe_weights)))
max_sharpe_sharpe = (max_sharpe_return - risk_free_rate_monthly) / max_sharpe_std

# 6. 输出结果
print("最小方差投资组合：")
print(f"预期回报率: {min_variance_return:.4%}")
print(f"标准差: {min_variance_std:.4%}")
print(f"夏普比率: {min_variance_sharpe:.4f}")
print("投资权重：")
for code, weight in zip(mean_returns.index, min_variance_weights):
    print(f"{code}: {weight:.4%}")

print("\n最佳投资组合（最大化夏普比率）：")
print(f"预期回报率: {max_sharpe_return:.4%}")
print(f"标准差: {max_sharpe_std:.4%}")
print(f"夏普比率: {max_sharpe_sharpe:.4f}")
print("投资权重：")
for code, weight in zip(mean_returns.index, max_sharpe_weights):
    print(f"{code}: {weight:.4%}")