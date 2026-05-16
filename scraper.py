import requests
import pandas as pd
import os
import time

def get_all_warframe_sets():
    """
    全量战甲配置表（目前所有可交易的 Prime 战甲）
    """
    all_prime_warframes = [
        "ash_prime_set", "atlas_prime_set", "banshee_prime_set", "baruuk_prime_set",
        "chroma_prime_set", "ember_prime_set", "equinox_prime_set", "frost_prime_set",
        "gara_prime_set", "garuda_prime_set", "gauss_prime_set", "grendel_prime_set",
        "hildryn_prime_set", "hydroid_prime_set", "inaros_prime_set", "ivara_prime_set",
        "khora_prime_set", "limbo_prime_set", "loki_prime_set", "mag_prime_set",
        "mesa_prime_set", "mirage_prime_set", "nekros_prime_set", "nezha_prime_set",
        "nidus_prime_set", "nova_prime_set", "nyx_prime_set", "oberon_prime_set",
        "octavia_prime_set", "revenant_prime_set", "rhino_prime_set", "saryn_prime_set",
        "titania_prime_set", "trinity_prime_set", "valkyr_prime_set", "vauban_prime_set",
        "volt_prime_set", "wisp_prime_set", "wukong_prime_set", "zephyr_prime_set"
    ]
    print(f"成功激活追踪计划！共计 {len(all_prime_warframes)} 个战甲。")
    return all_prime_warframes

def fetch_and_save_data(item_name):
    """根据战甲名称抓取历史数据，清洗时间戳并保存为 CSV"""
    url = f"https://api.warframe.market/v1/items/{item_name}/statistics"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            data_list = data['payload']['statistics_closed']['90days']
            
            # 1. 转换为 DataFrame
            df = pd.DataFrame(data_list)
            
            # 2. 清洗时间戳，转换为日期格式
            df['datetime'] = pd.to_datetime(df['datetime']).astype(str).str.slice(0, 10)
            
            # 3. 提取核心列
            df = df[['datetime', 'avg_price', 'volume', 'min_price', 'max_price']]
            
            # 4. 确保 data 文件夹存在
            os.makedirs('data', exist_ok=True)
            
            # 5. 保存文件
            file_path = f"data/{item_name}_history.csv"
            df.to_csv(file_path, index=False)
            print(f"✅ {item_name} 数据保存并清洗成功，共 {len(df)} 条记录。")
        else:
            print(f"❌ {item_name} 请求失败，状态码: {response.status_code}")
    except Exception as e:
        print(f"💥 抓取 {item_name} 时发生异常: {e}")

if __name__ == "__main__":
    # 1. 获取 40 个全量战甲名单
    warframes = get_all_warframe_sets()
    print("--------------------------------------------------")
    
    # 2. 循环遍历抓取
    for wf in warframes:
        print(f"正在获取: {wf} ...")
        fetch_and_save_data(wf)
        
        # 严格遵守频率限制：抓完一个，休息 1.5 秒，防止被官方封 IP
        time.sleep(1.5)
        
    print("--------------------------------------------------")
    print(" 数据抓取任务全部完成！")