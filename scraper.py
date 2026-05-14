import requests
import pandas as pd
import os
from datetime import datetime

def scrape_and_append(item_name):
    api_url = f"https://api.warframe.market/v1/items/{item_name}/statistics"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        # 获取最近的数据点（通常是最后一行）
        latest_data = data['payload']['statistics_closed']['90days'][-1]
        
        # 转换为 DataFrame
        new_row = pd.DataFrame([latest_data])
        new_row['datetime'] = pd.to_datetime(new_row['datetime'])
        
        file_path = f"data/{item_name}_history.csv"
        
        # 如果文件不存在，创建它；如果存在，追加数据且不写表头
        if not os.path.isfile(file_path):
            os.makedirs('data', exist_ok=True)
            new_row.to_csv(file_path, index=False)
        else:
            new_row.to_csv(file_path, mode='a', header=False, index=False)
        print(f"Successfully updated {item_name}")

if __name__ == "__main__":
    # 列出追踪的战甲
    targets = ["wisp_prime_set", "revenant_prime_set"]
    for target in targets:
        scrape_and_append(target)