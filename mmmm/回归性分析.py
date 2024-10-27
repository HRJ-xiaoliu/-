# 导入Python常用数据分析库：常用的numpy、pandas、matplotlib先导入
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from matplotlib.font_manager import FontProperties

# 设置字体
my_font = FontProperties(fname=r"E:\OneDrive - divinaletion\Miscellaneous\fonts\LXGWWenKai.ttf", size=12)

# read_excel进行Excel文件读取，用sheet_name指定导入的sheet
df = pd.read_csv("E:\Edge download\sichuan.csv")

print(df)


