import os
import pandas as pd

def process_and_merge_csv_files(base_folder, output_file):
    """
    遍历 Period1-Period15 文件夹内的所有 merged_data 文件，计算特征并合并为一个文件。
    
    Args:
        base_folder (str): 根文件夹路径，包含 Period1 到 Period15 文件夹。
        output_file (str): 最终合并的输出文件路径。
    """
    all_data = []  # 用于存储所有文件的数据

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
                try:
                    # 读取文件
                    df = pd.read_csv(file_path)

                    # 检查必要的列是否存在
                    if 'bidPrice' not in df.columns or 'askPrice' not in df.columns or \
                       'bidVolume' not in df.columns or 'askVolume' not in df.columns:
                        print(f"文件 {file_path} 缺少必要的列，跳过")
                        continue

                    # 计算 Midpoint Price
                    df['MidpointPrice'] = (df['bidPrice'] + df['askPrice']) / 2

                    # 计算 Order Flow Imbalance (OFI)
                    df['OrderFlowImbalance'] = df['bidVolume'] - df['askVolume']

                    # 计算 Weighted Spread
                    df['WeightedSpread'] = ((df['askPrice'] - df['bidPrice']) / df['MidpointPrice']) * 100

                    # 添加 period 和 stock 信息（可选，根据你的需求）
                    df['period'] = period_folder  # 添加 period 信息
                    df['stock'] = sub_folder      # 添加 stock 信息

                    # 收集数据
                    all_data.append(df)

                    print(f"文件 {file_path} 已处理并加入合并数据")

                except Exception as e:
                    print(f"处理文件 {file_path} 时发生错误: {e}")
            else:
                print(f"文件 {file_name} 在 {sub_folder_path} 中不存在，跳过")

    # 合并所有数据
    if all_data:
        merged_data = pd.concat(all_data, ignore_index=True)

        # 保存到输出文件
        merged_data.to_csv(output_file, index=False)
        print(f"所有文件已合并并保存到: {output_file}")
    else:
        print("未找到任何有效数据，未生成输出文件")

# 使用示例
base_folder = "TestData"  # 替换为你的根目录路径
output_file = "featured_test_data.csv"          # 替换为输出文件路径
process_and_merge_csv_files(base_folder, output_file)
