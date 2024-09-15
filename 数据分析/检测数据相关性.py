import pandas as pd

data = {
    "A": [1, 2, 3, 4, 5,6,7],
    "B": [2, 4, 5, 8, 13,16,]
}
df = pd.DataFrame(data)

correlation = df["A"].corr(df["B"], method="kendall")
print(correlation)  # 输出：1.0

 