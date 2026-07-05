import nbformat as nbf
import os
from pathlib import Path

def create_colab_notebook():
    nb = nbf.v4.new_notebook()
    
    # Setup cell
    setup_cell = nbf.v4.new_code_cell("""# Cài đặt các thư viện cần thiết cho Colab
!pip install yfinance ta pandas numpy tensorflow scikit-learn matplotlib seaborn""")
    
    # Imports cell
    imports_cell = nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import yfinance as yf
import ta
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras import layers, Model
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')""")

    # Function to read python files and create cells
    code_cells = []
    
    src_dir = Path("Stock_Forecasting_Project/04_Source_Code")
    files_to_include = [
        "data_ingestion.py",
        "feature_engineering.py",
        "model_architecture.py",
        "backtest_engine.py"
    ]
    
    for filename in files_to_include:
        filepath = src_dir / filename
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                # Remove imports that are already in the first cell to avoid clutter
                cleaned_content = []
                for line in content.split('\n'):
                    if not line.startswith('import ') and not line.startswith('from '):
                        cleaned_content.append(line)
                code_cells.append(nbf.v4.new_markdown_cell(f"### {filename}"))
                code_cells.append(nbf.v4.new_code_cell('\n'.join(cleaned_content)))
        else:
            print(f"File not found: {filepath}")

    # Execution cell
    execution_cell = nbf.v4.new_code_cell("""# Hàm thực thi chính
print('Bắt đầu tải dữ liệu...')
# (Phần này sẽ gọi các class đã định nghĩa ở trên để chạy demo toàn bộ)
# Ví dụ:
# data = fetch_data('AAPL')
# features = engineer_features(data)
# model = DataFusionModel().build_model()
# model.summary()
print('Đã load xong các module, hệ thống sẵn sàng chạy!')
""")

    nb.cells = [
        nbf.v4.new_markdown_cell("# Đồ Án Học Sâu & Học Máy: Dự Báo Giá Cổ Phiếu"),
        setup_cell,
        imports_cell
    ] + code_cells + [execution_cell]

    output_path = "Stock_Forecasting_Project/Colab_Demo.ipynb"
    with open(output_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    
    print(f"Đã tạo file notebook thành công tại: {output_path}")

if __name__ == "__main__":
    # Ensure working directory is the project root
    os.chdir(Path(__file__).resolve().parent)
    create_colab_notebook()
