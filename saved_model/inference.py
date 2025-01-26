#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import numpy as np
import pandas as pd
import xgboost as xgb
import matplotlib.pyplot as plt

# 如果你训练时用 joblib 保存了 scaler, onehot 等，可以在这里加载:
# from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
# import joblib
# scaler = joblib.load("my_scaler.pkl")
# ohe    = joblib.load("my_onehot.pkl")

def simulate_prediction(test_csv: str, model_path: str):
    """
    读取 test.csv, 然后行-by-行预测，模拟实时输出过程。
    最后再打印所有真实值，和模型结果对比。
    """
    # 1) 加载已经训练好的 XGBoost 模型
    model = xgb.XGBRegressor()
    model.load_model(model_path)
    print(">>> 已加载模型:", model_path)

    # 2) 读取 test.csv
    df_test = pd.read_csv(test_csv)
    if df_test.empty:
        print(f"警告: {test_csv} 文件是空的，无法预测。")
        return

    # 3) 如果没有 MidpointPrice，就创建 (视情况而定)
    if "MidpointPrice" not in df_test.columns:
        df_test["MidpointPrice"] = (df_test["bidPrice"] + df_test["askPrice"]) / 2

    # 假设要预测的目标就是 MidpointPrice
    # 这里先把真实值提取出来，后面对比
    y_true = df_test["MidpointPrice"].values

    # 4) 定义和训练时一致的特征处理
    #    (此处仅作演示，实际上你需要跟你训练时一样的 numeric_cols / OneHot / Scaler 等)
    numeric_cols = ["bidVolume", "bidPrice", "askVolume", "askPrice", "MidpointPrice"]
    # 如果你有更多列，请自行添加
    # 如果你在训练时对 stock 做 OneHot, 也要在这里做一致的处理
    
    # 这个函数预处理一行数据
    def preprocess_one_row(row: pd.Series) -> np.ndarray:
        """
        把单行 row 转成模型输入向量。
        注意：这里的写法要和训练时保持一致！
        """
        # 取出 numeric_cols
        arr_num = row[numeric_cols].values.astype(float)
        # 演示：简单缩放 => arr_num / 1000.0
        # 你必须用和训练时相同的 scaler
        arr_num_scaled = arr_num / 1000.0

        # 如果训练时对 stock 做OneHot:
        #   stock_val = row["stock"]
        #   arr_stock_ohe = ohe.transform([[stock_val]])  # shape (1, onehot_dim)
        #   X = np.hstack([arr_num_scaled, arr_stock_ohe[0]])
        # else:
        X = arr_num_scaled  # 简化处理

        # XGBoost 接受 (n_features,) 或 (1, n_features), 这里返回1行
        return X.reshape(1, -1)

    # 5) 循环逐行预测 & 模拟展示
    predictions = []
    print(">>> 开始逐行预测，模拟实时输出...")
    for i in range(len(df_test)):
        # 取出第 i 行
        row = df_test.iloc[i]
        # 预处理 => 得到模型输入
        X_i = preprocess_one_row(row)
        # 预测
        pred_i = model.predict(X_i)[0]  # 取标量
        predictions.append(pred_i)

        # 实时打印结果
        print(f"行{i}: 预测MidpointPrice = {pred_i:.4f}")
        # 模拟等待1秒
        time.sleep(1)

    # 6) 全部预测结束后，对比真实值
    print("\n>>> 预测结束! 现在显示所有真实值 vs. 预测值:\n")
    for i, (truth, pred) in enumerate(zip(y_true, predictions)):
        print(f"行{i}: 真值={truth:.4f}, 预测={pred:.4f}")
    
    # 7) 也可做简单误差计算 & 可视化
    errors = np.array(predictions) - y_true
    mse = np.mean(errors**2)
    rmse = np.sqrt(mse)
    print(f"\n整体MSE={mse:.4f}, RMSE={rmse:.4f}")

    # 简单画图
    plt.figure(figsize=(10,5))
    plt.plot(y_true, label='True')
    plt.plot(predictions, label='Predicted')
    plt.title("MidpointPrice: True vs. Predicted")
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    import sys

    test_csv_path = "data/TestData/merged/A_stock.csv"
    model_path    = "saved_model/xgb_model_A.json"

    simulate_prediction(test_csv_path, model_path)
