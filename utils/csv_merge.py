import os
import pandas as pd

def merge_market_data_in_periods(root_path):
    """
    遍历所有 Period 文件夹，对其中的 A, B, C, D, E 子文件夹执行数据合并操作。
    
    Args:
    - root_path (str): 包含 Period 文件夹的根路径，例如 "TrainingData"。
    """
    periods = [f"Period{p}" for p in range(1, 21)]  # 动态生成 Period1 到 Period15
    stocks = ['A', 'B', 'C', 'D', 'E']  # 股票文件夹名称
    
    for period in periods:
        period_path = os.path.join(root_path, period)
        
        if not os.path.exists(period_path):
            print(f"路径不存在: {period_path}，跳过...")
            continue

        for stock in stocks:
            stock_path = os.path.join(period_path, stock)
            
            if not os.path.exists(stock_path):
                print(f"路径不存在: {stock_path}，跳过...")
                continue

            # 动态生成输出文件路径
            output_file = os.path.join(stock_path, f"merged_data_{stock}.csv")
            merge_market_data(stock_path, output_file)


def merge_market_data(folder_path, output_file):
    """
    合并指定文件夹中符合命名规则的 market_data 文件，并按时间戳排序。
    
    Args:
    - folder_path (str): 包含 market_data 文件的文件夹路径。
    - output_file (str): 合并后输出的文件名。
    """
    # 从路径中动态提取股票名称 (例如 "B")
    stock_name = os.path.basename(folder_path)  # 提取最后一级文件夹名
    if not stock_name:
        print("无法从路径中提取股票名称，请检查文件夹路径是否正确。")
        return
    
    # 动态匹配命名规则的文件，例如 market_data_B_0.csv
    file_pattern = f"market_data_{stock_name}_"
    all_data = []

    # 遍历文件夹中的所有文件
    for file in os.listdir(folder_path):
        # 只处理符合动态命名规则的文件
        if file.startswith(file_pattern) and file.endswith(".csv"):
            file_path = os.path.join(folder_path, file)
            
            # 加载文件并设置列名
            try:
                data = pd.read_csv(file_path, header=None, names=["bidVolume", "bidPrice", "askVolume", "askPrice", "timestamp"])
                all_data.append(data)
                print(f"成功加载文件: {file}")
            except Exception as e:
                print(f"加载文件失败: {file}, 错误: {e}")
    
    # 合并所有数据
    if all_data:
        combined_data = pd.concat(all_data, ignore_index=True)
        
        # 确保时间戳格式一致
        try:
            combined_data['timestamp'] = pd.to_datetime(
                combined_data['timestamp'],
                format="%H:%M:%S.%f",  # 明确指定格式为时分秒和微秒
                errors='coerce'
            )
        except Exception as e:
            print(f"时间戳解析失败，错误信息: {e}")
        
        # 删除任何时间戳无效的行
        combined_data = combined_data.dropna(subset=['timestamp'])

        # 按时间戳排序
        combined_data = combined_data.sort_values(by='timestamp')

        # 保存合并后的数据
        combined_data.to_csv(output_file, index=False)
        print(f"数据已合并并保存为: {output_file}")
    else:
        print(f"没有符合条件的文件可供合并: {folder_path}")


# 示例调用
root_path = "TestData"  # 替换为你的根文件夹路径
merge_market_data_in_periods(root_path)
