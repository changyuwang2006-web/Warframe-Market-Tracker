import pandas as pd
import matplotlib.pyplot as plt

# 1. 读取刚刚保存的 CSV 文件
item_name = "wisp_prime_set"
df = pd.read_csv(f"{item_name}_history.csv")

# 2. 转换日期格式，确保横轴是时间
df['datetime'] = pd.to_datetime(df['datetime'])

# 3. 开始画图
plt.figure(figsize=(10, 6))
plt.plot(df['datetime'], df['avg_price'], marker='o', linestyle='-', color='b')

# 4. 装饰图表
plt.title(f"Price Trend: {item_name}", fontsize=14)
plt.xlabel("Date", fontsize=12)
plt.ylabel("Average Price (Platinum)", fontsize=12)
plt.grid(True)
plt.xticks(rotation=45) # 日期倾斜一下

# 5. 显示图片
plt.tight_layout()
plt.show()