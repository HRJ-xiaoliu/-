
#跑出十个股票五年的回报率（按周计算）
import yfinance as yf
import pandas as pd

# 股票代码列表
stocks =  ["000001.SZ", "000002.SZ", "000333.SZ", "000651.SZ", 
          "000725.SZ", "000858.SZ", "002415.SZ", "000001.SZ" ,"000063.SZ","000786.SZ","002475.SZ"]


# 获取过去5年的数据（每周）
start_date = "2018-01-01"
end_date = "2023-01-01"

# 初始化空列表，存储所有股票的回报率数据
all_data = []

for stock in stocks:
    ticker = yf.Ticker(stock)
    # 获取每周的收盘价
    data = ticker.history(start=start_date, end=end_date, interval="1wk")
    
    # 计算每周回报率
    data['Return'] = data['Close'].pct_change()
    
    # 重塑数据为所需的格式：日期、股票代码、回报率
    stock_data = data[['Return']].reset_index()
    stock_data['Stock'] = stock  # 添加股票代码列
    stock_data = stock_data[['Date', 'Stock', 'Return']]  # 按顺序排列
    
    # 将结果追加到all_data列表中
    all_data.append(stock_data)

# 合并所有股票的数据到一个数据框
final_data = pd.concat(all_data)

# 去除回报率为NaN的行
final_data = final_data.dropna(subset=['Return'])

# 保存为CSV文件
final_data.to_csv("stock_weekly_returns.csv", index=False)

# 显示前几行数据
print(final_data.head())
