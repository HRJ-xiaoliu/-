import pandas as pd

data = {
    "A": [1, 2, 3, 4, 5],
    "B": [2, 4, 6, 8, 10]
}
df = pd.DataFrame(data)

correlation = df["A"].corr(df["B"], method="kendall")
print(correlation)  # 输出：1.0

 