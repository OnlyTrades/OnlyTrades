import os
import pandas as pd
from natsort import natsorted  # 引入自然排序库

def process_stock_data(stock_folder, stock_name):
    """
    合并一个股票文件夹中的所有 market_data，并基于 timestamp 合并。
    """
    try:
        # 动态生成 market_data 文件路径
        market_data_files = [
            os.path.join(stock_folder, f) for f in os.listdir(stock_folder) if f.startswith(f'market_data_{stock_name}_')
        ]

        # 检查 market_data 文件是否存在
        if not market_data_files:
            print(f"No market data files in {stock_folder} for {stock_name}, skipping.")
            return pd.DataFrame()

        # 读取并合并所有 market_data
        market_data_list = []
        for file_path in market_data_files:
            market_data = pd.read_csv(file_path, header=None)
            if 'timestamp' not in market_data.columns and len(market_data.columns) == 5:
                # 设置 market_data 的默认列名
                market_data.columns = ['bidVolume', 'bidPrice', 'askVolume', 'askPrice', 'timestamp']
            # 保持为 datetime64，但只保留时间部分
            market_data['timestamp'] = pd.to_datetime(market_data['timestamp'], format='%H:%M:%S.%f', errors='coerce')
            market_data.dropna(subset=['timestamp'], inplace=True)
            market_data_list.append(market_data)

        combined_market_data = pd.concat(market_data_list, ignore_index=True)
        combined_market_data.sort_values('timestamp', inplace=True)

        return combined_market_data
    except Exception as e:
        print(f"Error processing {stock_folder}: {e}")
        return pd.DataFrame()


def process_all_data(base_path):
    all_data = []
    stock_names = ['A', 'B', 'C', 'D', 'E']

    # 使用 natsorted 进行自然排序
    for period_folder in natsorted(os.listdir(base_path)):
        period_path = os.path.join(base_path, period_folder)
        if os.path.isdir(period_path):
            print(f"Processing period folder: {period_folder}")
            for stock_folder in natsorted(os.listdir(period_path)):
                stock_path = os.path.join(period_path, stock_folder)
                if os.path.isdir(stock_path) and stock_folder in stock_names:
                    print(f"  Processing stock folder: {stock_folder}")
                    merged_stock_data = process_stock_data(stock_path, stock_folder)
                    if not merged_stock_data.empty:
                        merged_stock_data['period'] = period_folder
                        merged_stock_data['stock'] = stock_folder
                        all_data.append(merged_stock_data)

    if all_data:
        return pd.concat(all_data, ignore_index=True)
    else:
        print("No valid data found!")
        return pd.DataFrame()


# 基础路径
base_path = 'TestData'  # 替换为实际的根路径

# 合并所有数据
final_dataset = process_all_data(base_path)

# 保存最终结果
if not final_dataset.empty:
    final_dataset.to_csv('merged_all_stock_data.csv', index=False)
    print("所有数据合并完成，已保存为 'merged_all_stock_test_data.csv'")
else:
    print("最终数据集为空，未生成文件。")
