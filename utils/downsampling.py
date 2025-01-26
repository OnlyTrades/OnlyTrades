import os
import pandas as pd

def process_csv_file(file_path):
    """
    对单个 CSV 文件进行降采样和排序（仅处理存在的列）。
    """
    try:
        # 读取数据
        data = pd.read_csv(file_path)

        # 确保有 timestamp 列
        if 'timestamp' not in data.columns:
            print(f"文件 {file_path} 中没有 'timestamp' 列，跳过")
            return

        # 确保 timestamp 是 datetime 类型
        data['timestamp'] = pd.to_datetime(data['timestamp'])

        # 设置 timestamp 为索引
        data.set_index('timestamp', inplace=True)

        # 动态生成降采样的聚合规则
        available_columns = data.columns
        agg_rules = {}

        if 'bidVolume' in available_columns:
            agg_rules['bidVolume'] = 'mean'
        if 'bidPrice' in available_columns:
            agg_rules['bidPrice'] = 'mean'
        if 'askVolume' in available_columns:
            agg_rules['askVolume'] = 'mean'
        if 'askPrice' in available_columns:
            agg_rules['askPrice'] = 'mean'
        if 'MidpointPrice' in available_columns:
            agg_rules['MidpointPrice'] = 'mean'
        if 'OrderFlowImbalance' in available_columns:
            agg_rules['OrderFlowImbalance'] = 'mean'
        if 'WeightedSpread' in available_columns:
            agg_rules['WeightedSpread'] = 'mean'
        if 'period' in available_columns:
            agg_rules['period'] = 'first'
        if 'stock' in available_columns:
            agg_rules['stock'] = 'first'

        # 对数据降采样：每秒一次
        downsampled_data = data.resample('1s').agg(agg_rules)

        # 填充可能的缺失值
        downsampled_data = downsampled_data.fillna(method='ffill')  # 前向填充

        # 重置索引
        downsampled_data.reset_index(inplace=True)

        # 如果存在 period 列，按其排序
        if 'period' in downsampled_data.columns:
            downsampled_data['period_numeric'] = downsampled_data['period'].str.extract('(\d+)').astype(float)
            downsampled_data.sort_values(by='period_numeric', inplace=True)
            downsampled_data.drop(columns=['period_numeric'], inplace=True)

        # 保存降采样后的数据，覆盖原文件
        downsampled_data.to_csv(file_path, index=False)
        print(f"文件 {file_path} 已完成降采样并保存")
    
    except Exception as e:
        print(f"处理文件 {file_path} 时发生错误: {e}")

def process_all_csv_files(base_folder):
    """
    遍历 Period1-Period15 文件夹内的子文件夹 A-E，对其内的 CSV 文件逐一处理。
    """
    for period_folder in [f"Period{i}" for i in range(1, 21)]:
        period_path = os.path.join(base_folder, period_folder)

        # 确保 Period 文件夹存在
        if not os.path.exists(period_path):
            print(f"主文件夹 {period_folder} 不存在，跳过")
            continue

        # 遍历子文件夹 A, B, C, D, E
        for sub_folder in ['A', 'B', 'C', 'D', 'E']:
            sub_folder_path = os.path.join(period_path, sub_folder)

            # 确保子文件夹存在
            if not os.path.exists(sub_folder_path):
                print(f"子文件夹 {sub_folder_path} 不存在，跳过")
                continue

            # 确定子文件夹下的对应文件名
            file_name = f"merged_data_{sub_folder}.csv"
            file_path = os.path.join(sub_folder_path, file_name)

            # 检查文件是否存在
            if os.path.exists(file_path):
                process_csv_file(file_path)
            else:
                print(f"文件 {file_name} 在 {sub_folder_path} 中不存在，跳过")

# 使用示例
base_folder = "TestData"  # 替换为你的根目录路径
process_all_csv_files(base_folder)
