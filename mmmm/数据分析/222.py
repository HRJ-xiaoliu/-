import pandas as pd


# 读取数据
df = pd.read_csv("数据基础.csv")

# 将日期列转换为日期类型
df['日期'] = pd.to_datetime(df['日期'], format='%Y/%m/%d')

# 去除回报率为空的行
df = df.dropna(subset=['回报率'])

# 创建以日期为索引，股票代码为列的回报率矩阵
return_matrix = df.pivot(index='日期', columns='代码', values='回报率')

# 计算协方差矩阵
cov_matrix = return_matrix.cov()

# 计算每只股票的平均回报率
mean_returns = return_matrix.mean()

# 计算每只股票的标准差
std_devs = return_matrix.std()

# 计算夏普比率（假设无风险利率为0）
sharpe_ratios = mean_returns / std_devs

# 创建包含平均回报率、标准差和夏普比率的 DataFrame
results = pd.DataFrame({
    '平均回报率': mean_returns,
    '标准差': std_devs,
    '夏普比率': sharpe_ratios
})

# 根据夏普比率对股票进行排序
results_sorted = results.sort_values(by='夏普比率', ascending=False)

# 将协方差矩阵和股票指标写入Excel文件
with pd.ExcelWriter('股票分析结果.xlsx') as writer:
    cov_matrix.to_excel(writer, sheet_name='协方差矩阵')
    results_sorted.to_excel(writer, sheet_name='股票指标')

# 提示用户文件已保存
print("股票分析结果.xlsx已保存")