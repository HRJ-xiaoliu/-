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

# 4. 计算最佳投资组合（最大化夏普比率）
def negative_sharpe_ratio(weights, mean_returns, cov_matrix, risk_free_rate):
    portfolio_return = np.dot(weights, mean_returns)
    portfolio_std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    return -(portfolio_return - risk_free_rate) / portfolio_std

initial_weights = np.array([1 / num_stocks] * num_stocks)

# 月度无风险收益率
risk_free_rate_annual = 0.04
risk_free_rate_monthly = (1 + risk_free_rate_annual) ** (1 / 12) - 1

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

# 5. 调整投资组合以包含无风险资产

# 计算最佳投资组合的年预期回报率
E_Rp_annual = (1 + max_sharpe_return) ** 12 - 1

# 新的年预期回报率（降低 2%）
E_Rnew_annual = E_Rp_annual - 0.02  # 减少 2%

# 确保新的年预期回报率不低于无风险收益率
E_Rnew_annual = max(E_Rnew_annual, risk_free_rate_annual)

# 计算新的月度预期回报率
E_Rnew = (1 + E_Rnew_annual) ** (1 / 12) - 1

# 求解 y
y = (E_Rnew - risk_free_rate_monthly) / (max_sharpe_return - risk_free_rate_monthly)

# 确保 y 在 0 到 1 之间
y = min(max(y, 0), 1)

# 调整风险资产的权重
adjusted_risky_weights = max_sharpe_weights * y

# 无风险资产的权重
risk_free_weight = 1 - y

# 新的投资组合预期回报率
new_portfolio_return = y * max_sharpe_return + (1 - y) * risk_free_rate_monthly

# 新的投资组合标准差
new_portfolio_std = y * max_sharpe_std

# 创建投资组合权重字典
portfolio_weights = dict(zip(mean_returns.index, adjusted_risky_weights))
portfolio_weights['无风险资产'] = risk_free_weight

# 6. 输出结果
print("新的投资组合：")
print(f"预期回报率: {new_portfolio_return:.4%}")
print(f"标准差: {new_portfolio_std:.4%}")
print(f"投资于风险资产的比例 (y): {y:.4%}")
print("投资权重：")
for asset, weight in portfolio_weights.items():
    print(f"{asset}: {weight:.4%}")