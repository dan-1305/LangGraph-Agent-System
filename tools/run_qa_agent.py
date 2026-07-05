import os
import re

def qa_agent_audit():
    print("[ACTIVE ROLE: QA & Security Auditor]")
    print("Scanning source code for vulnerabilities...\n")
    
    files_to_check = [
        r"projects\ĐỀ TÀI HỌC SÂU, kết hợp làm Đồ án môn AI & Học máy\Stock_Forecasting_Project\04_Source_Code\Tien_Machine_Learning\01_Tien_Data_Pipeline.ipynb",
        r"projects\ĐỀ TÀI HỌC SÂU, kết hợp làm Đồ án môn AI & Học máy\Stock_Forecasting_Project\04_Source_Code\Danh_Deep_Learning_Core\03_Danh_LSTM_Models.ipynb",
        r"tools\run_pipeline_ml.py",
        r"tools\run_pipeline_lstm.py"
    ]
    
    issues_found = 0
    for file_path in files_to_check:
        if not os.path.exists(file_path):
            continue
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Check 1: Data Leakage (shuffle=True)
            if re.search(r'train_test_split\s*\([^)]*shuffle\s*=\s*True[^)]*\)', content) or re.search(r'train_test_split\s*\([^)]*\)', content) and 'shuffle' not in content:
                # If train_test_split is used but shuffle=False is not explicitly set or shuffle=True is set
                if 'shuffle=False' not in content:
                    print(f"[CRITICAL] DATA LEAKAGE DETECTED in {file_path}")
                    print("   - WARNING: Used train_test_split on Time-series without setting shuffle=False!")
                    issues_found += 1
            
            # Check 2: PyTorch Backend for Keras
            if 'keras' in content and 'LSTM' in content:
                if 'KERAS_BACKEND' not in content or 'torch' not in content:
                    print(f"[WARNING] WRONG BACKEND in {file_path}")
                    print("   - REQUIRED: Must use Keras 3.0 with PyTorch backend as instructed.")
                    issues_found += 1
                    
            # Check 3: Check Dense(1) vs Dense(5) for LSTM
            if 'LSTM' in content and 'Dense(1)' in content:
                print(f"[WARNING] UNDER-REQUIREMENT in {file_path}")
                print("   - Model only predicts 1 step. Teacher requires 3-5 steps (Multi-step). Upgrade to Dense(5) required.")
                issues_found += 1

    print("\n================ QA REPORT ================")
    if issues_found == 0:
        print("PASS: Code is secure, no data leakage or wrong backends found.")
    else:
        print(f"FAILED: Detected {issues_found} issues that need immediate fix!")
        print("Please invoke [Coder Agent] to patch.")
        
if __name__ == "__main__":
    qa_agent_audit()