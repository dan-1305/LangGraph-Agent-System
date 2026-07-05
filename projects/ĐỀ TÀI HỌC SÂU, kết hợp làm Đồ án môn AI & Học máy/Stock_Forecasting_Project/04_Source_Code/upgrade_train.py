import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_ingestion import DataIngestor
from feature_engineering import FeatureEngineer
from model_architecture import DataFusionModel

def plot_training_history(history, save_path):
    plt.figure(figsize=(10, 5))
    plt.plot(history.history['loss'], label='Train Loss', color='#3498db', linewidth=2)
    plt.plot(history.history['val_loss'], label='Val Loss', color='#e74c3c', linewidth=2)

    best_epoch = np.argmin(history.history['val_loss'])
    plt.axvline(best_epoch, color='gray', linestyle='--', alpha=0.6, label=f'Best Epoch: {best_epoch}')

    plt.title('Đồ thị Train Loss vs Validation Loss (Upgraded)', fontsize=14)
    plt.xlabel('Epochs')
    plt.ylabel('Loss (Huber)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(save_path)
    plt.close()

def plot_predictions(y_true, y_pred, save_path):
    plt.figure(figsize=(10, 5))
    # Chuyển đổi thành 1 chiều để vẽ đơn giản
    y_true_1d = y_true[:, 0]
    y_pred_1d = y_pred[:, 0]
    
    plt.plot(y_true_1d[-100:], label='Thực tế', color='black', alpha=0.7)
    plt.plot(y_pred_1d[-100:], label='Dự đoán', color='blue', alpha=0.7)
    
    plt.title('Kết quả Dự báo (Upgraded Model)', fontsize=14)
    plt.xlabel('Thời gian')
    plt.ylabel('Tín hiệu')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(save_path)
    plt.close()

def main():
    print("Fetching data...")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, '../01_Data/FPT_VN_clean.csv')
    
    if os.path.exists(data_path):
        df_raw = pd.read_csv(data_path, skiprows=[1, 2], index_col=0, parse_dates=True)
        df_raw.index.name = 'Date'
        # Nếu cột đầu là Price thay vì Date do file csv
        if df_raw.index.name == 'Price':
            df_raw.index.name = 'Date'
        engineer = FeatureEngineer(window_size=30, forecast_horizon=3)
        df_features = engineer.add_indicators(df_raw)
    else:
        ingestor = DataIngestor(ticker='FPT.VN', start_date='2020-01-01', end_date='2024-01-01')
        df_raw = ingestor.fetch_stock_data()
        engineer = FeatureEngineer(window_size=30, forecast_horizon=3)
        df_features = engineer.add_indicators(df_raw)

    print("Engineering features...")
    feature_cols = ['Close', 'RSI', 'Log_Ret']
    X, y = engineer.create_sliding_windows(df_features, feature_cols)
    X_train, X_test, y_train, y_test = engineer.time_series_split(X, y)

    nlp_train = np.zeros((X_train.shape[0], 3))
    nlp_test = np.zeros((X_test.shape[0], 3))

    print("Building model...")
    fusion_model = DataFusionModel(sequence_length=30, n_features=3, nlp_dim=3, forecast_horizon=3)
    model = fusion_model.build_model()

    callbacks = [
        EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True),
        ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=1e-5)
    ]

    print("Training model...")
    history = model.fit(
        [X_train, nlp_train],
        y_train,
        epochs=50,
        batch_size=32,
        validation_split=0.1,
        callbacks=callbacks,
        verbose=1
    )

    print("Saving plots...")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    loss_path = os.path.join(base_dir, '../01_Data/lstm_loss_chart.png')
    pred_path = os.path.join(base_dir, '../01_Data/lstm_prediction_chart.png')
    
    plot_training_history(history, loss_path)
    
    predictions = model.predict([X_test, nlp_test])
    plot_predictions(y_test, predictions, pred_path)
    print("Done!")

if __name__ == '__main__':
    main()
