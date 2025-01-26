import numpy as np
import pandas as pd
import xgboost as xgb
import joblib
import matplotlib.pyplot as plt
import time
from sklearn.metrics import mean_squared_error, mean_absolute_error
import sys

def preprocess_test_data(df_test, scaler, ohe, seq_length=60):
    """
    预处理 test 数据，与训练时保持一致：
    1. 如果没有 MidpointPrice，就添加
    2. 对数值列做缩放
    3. 对 stock 做 One-Hot 编码
    4. 构造滑动窗口
    """
    # 1. 添加 MidpointPrice 列（如果不存在）
    if "MidpointPrice" not in df_test.columns:
        df_test["MidpointPrice"] = (df_test["bidPrice"] + df_test["askPrice"]) / 2

    # 2. 数值列和分类列
    numeric_cols = [
        "bidVolume",
        "bidPrice",
        "askVolume",
        "askPrice",
        "OrderFlowImbalance",
        "WeightedSpread",
        "MidpointPrice"
    ]

    # 确保所有必要的列都存在
    missing_cols = [col for col in numeric_cols + ['stock'] if col not in df_test.columns]
    if missing_cols:
        raise ValueError(f"测试数据中缺少以下必要列: {missing_cols}")

    # 3. 对数值列进行缩放
    data_numeric = scaler.transform(df_test[numeric_cols].values)

    # 4. 对 'stock' 列进行 One-Hot 编码
    cat_array = df_test[['stock']].astype(str).values  # shape: (N, 1)
    ohe_feats = ohe.transform(cat_array)               # shape: (N, onehot_dim)

    # 5. 拼接数值特征和 One-Hot 特征
    data_combined = np.hstack([data_numeric, ohe_feats])  # shape: (N, 7 + onehot_dim)

    # 6. 构造滑动窗口
    def create_supervised_data(data_combined, seq_length):
        """
        构造滑动窗口特征
        """
        X_out, y_out = [], []
        mid_price_idx = 6  # numeric_cols 中 MidpointPrice 的索引（从0开始）
        N = len(data_combined)
        for i in range(seq_length, N):
            # 过去 seq_length 行 => flatten 到一维
            x_i = data_combined[i-seq_length:i].flatten()
            # 目标 => 当前行(i) 的 MidpointPrice
            y_i = data_combined[i, mid_price_idx]
            X_out.append(x_i)
            y_out.append(y_i)
        return np.array(X_out), np.array(y_out)

    X_test, y_test = create_supervised_data(data_combined, seq_length)
    return X_test, y_test

def simulate_realtime_prediction(test_csv: str, model_path: str, scaler_path: str, ohe_path: str, seq_length=60, delay=0.1):
    """
    逐步预测 test.csv 的数据，模拟实时预测过程。
    最后与真实值对比。
    """
    # 1. 加载模型和预处理器
    try:
        model = xgb.XGBRegressor()
        model.load_model(model_path)
        print(f">>> 已加载模型: {model_path}")
    except Exception as e:
        print(f"加载模型时出错: {e}")
        sys.exit(1)

    try:
        scaler = joblib.load(scaler_path)
        print(f">>> 已加载 Scaler: {scaler_path}")
    except Exception as e:
        print(f"加载 Scaler 时出错: {e}")
        sys.exit(1)

    try:
        ohe = joblib.load(ohe_path)
        print(f">>> 已加载 OneHotEncoder: {ohe_path}")
    except Exception as e:
        print(f"加载 OneHotEncoder 时出错: {e}")
        sys.exit(1)

    # 2. 读取 test.csv
    try:
        df_test = pd.read_csv(test_csv)
        if df_test.empty:
            print(f"警告: {test_csv} 文件是空的，无法预测。")
            sys.exit(1)
    except Exception as e:
        print(f"读取 test.csv 时出错: {e}")
        sys.exit(1)

    # 3. 预处理 test 数据
    try:
        X_test, y_test = preprocess_test_data(df_test, scaler, ohe, seq_length)
        print(">>> Data Preprocess finished.")
    except Exception as e:
        print(f"Error when proprocess: {e}")
        sys.exit(1)

    # 4. 模拟逐步预测
    preds = []
    print(">>> Prediction starting...")
    for i in range(len(X_test)):
        X_i = X_test[i].reshape(1, -1)  # shape: (1, 60 * (7 + onehot_dim))
        try:
            pred_i = model.predict(X_i)[0]
            preds.append(pred_i)
            print(f"Predict {i + 1} Samples: MidpointPrice = {pred_i:.4f}")
            time.sleep(delay)  # 模拟延迟
        except Exception as e:
            print(f"Error when Predict {i + 1} sample: {e}")
            preds.append(np.nan)

    # 5. 逆缩放预测结果和真实值
    try:
        mid_price_idx = 6
        numeric_size = 7  # numeric_cols 有7列

        # 创建 dummy 数组用于逆缩放预测结果
        y_pred_scaled = np.array(preds).reshape(-1, 1)
        dummy_pred = np.zeros((len(y_pred_scaled), numeric_size))
        dummy_pred[:, mid_price_idx] = y_pred_scaled[:, 0]
        y_pred_inv = scaler.inverse_transform(dummy_pred)[:, mid_price_idx]

        # 创建 dummy 数组用于逆缩放真实值
        y_test_scaled = y_test.reshape(-1, 1)
        dummy_true = np.zeros((len(y_test_scaled), numeric_size))
        dummy_true[:, mid_price_idx] = y_test_scaled[:, 0]
        y_true_inv = scaler.inverse_transform(dummy_true)[:, mid_price_idx]
    except Exception as e:
        print(f"逆缩放时出错: {e}")
        sys.exit(1)

    # 6. 显示对比
    print("\n>>> Prediction Finished! True vs Predict Price:")
    for i in range(len(y_true_inv)):
        print(f"The No. {i + 1} Sample: True = {y_true_inv[i]:.4f}, Predict = {y_pred_inv[i]:.4f}")

    # 7. 计算误差
    try:
        mse = mean_squared_error(y_true_inv, y_pred_inv)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_true_inv, y_pred_inv)
        print(f"\n整体 MSE = {mse:.4f}, RMSE = {rmse:.4f}, MAE = {mae:.4f}")
    except Exception as e:
        print(f"计算误差时出错: {e}")
        sys.exit(1)

    # 8. 可视化
    try:
        plt.figure(figsize=(12,6))
        plt.plot(y_true_inv, label='True Price')
        plt.plot(y_pred_inv, label='Predicted Price')
        plt.title("MidpointPrice: True vs Predicted")
        plt.legend()
        plt.grid(True)
        plt.show()
    except Exception as e:
        print(f"绘图时出错: {e}")

if __name__ == "__main__":
    # 用法: python inference.py [test_csv_path] [model_path] [scaler_path] [ohe_path] [seq_length=60] [delay=0.1]

    test_csv_path = "data/TestData/merged/A_stock.csv"
    model_path    = "saved_model/XGBoostA/xgb_model_A.json"
    scaler_path   = "saved_model/XGBoostA/scaler_A.pkl"           # 第三个参数：保存的 scaler 文件路径
    ohe_path      = "saved_model/XGBoostA/ohe_A.pkl"           # 第四个参数：保存的 OneHotEncoder 文件路径
    seq_length    = 60       # 可选参数：滑动窗口长度，默认为60
    delay         = 0.1     # 可选参数：预测间延迟时间，默认为0.1秒

    simulate_realtime_prediction(test_csv_path, model_path, scaler_path, ohe_path, seq_length, delay)
