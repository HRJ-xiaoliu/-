from scipy.stats import kstest
import numpy as np

# 生成一个正态分布的随机数组
#生成一个非正态分布的随机数组data = np.random.exponential(scale=2.0, size=1000)
data = np.random.normal(0, 1, 1000)

# 进行正态性检验
statistic, pvalue = kstest(data, 'norm')

print('K-S test statistic: %.6f' % statistic)
print('P value: %.6f' % pvalue)

