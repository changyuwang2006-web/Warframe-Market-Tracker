import requests
import pandas as pd
from datetime import datetime

def get_warframe_data(item_url_name):
    """
    item_url_name: 物品在网址里的名字，比如 'wisp_prime_set'
    """
    # 1. 构造 API 地址
    api_url = f"https://api.warframe.market/v1/items/{item_url_name}/statistics"
    
    # 2. 发送请求获取数据
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        
        # 3. 提取过去 90 天的数据 (取 daily 统计)
        # 我们要提取的是 'closed_min' (成交最低价), 'avg_price' (均价), 'datetime' (日期)
        rows = data['payload']['statistics_closed']['90days']
        
        # 4. 转换成 Pandas 的 DataFrame (数据表格格式)
        df = pd.DataFrame(rows)
        
        # 5. 时间格式转换（将原始字符串转成你看得懂的日期）
        df['datetime'] = pd.to_datetime(df['datetime'])
        
        # 只保留我们关心的几列：日期、均价、成交量、最低价
        df = df[['datetime', 'avg_price', 'volume', 'min_price']]
        
        return df
    else:
        print(f"报错啦！状态码是: {response.status_code}")
        return None

# --- 使用示例 ---
target_item = "wisp_prime_set" # 你可以换成任何你想追踪的物品
df_wisp = get_warframe_data(target_item)

if df_wisp is not None:
    print(df_wisp.tail(10)) # 显示最后10行数据
    # 将数据保存到你的本地，这就是你的第一个数据集！
    df_wisp.to_csv(f"{target_item}_history.csv", index=False)
    print(f"\n数据已保存为 {target_item}_history.csv")
