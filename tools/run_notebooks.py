import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import os

nb_path1 = "projects/ĐỀ TÀI HỌC SÂU, kết hợp làm Đồ án môn AI & Học máy/Stock_Forecasting_Project/04_Source_Code/Tien_Machine_Learning/01_Tien_Data_Pipeline.ipynb"
nb_path2 = "projects/ĐỀ TÀI HỌC SÂU, kết hợp làm Đồ án môn AI & Học máy/Stock_Forecasting_Project/04_Source_Code/Danh_Deep_Learning_Core/03_Danh_LSTM_Models.ipynb"

def run_notebook(nb_path):
    print("Running a notebook...")
    try:
        with open(nb_path, encoding="utf-8") as f:
            nb = nbformat.read(f, as_version=4)
        
        # Execute in the notebook's directory
        folder = os.path.dirname(os.path.abspath(nb_path))
        ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
        ep.preprocess(nb, {'metadata': {'path': folder}})
        
        with open(nb_path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
        print("Successfully executed notebook")
    except Exception as e:
        print(f"Error executing notebook: {e}")

run_notebook(nb_path1)
run_notebook(nb_path2)
