import os
import subprocess

def test_code():
    print("[ACTIVE ROLE: Tester Agent]")
    print("Testing ML Pipeline...")
    try:
        subprocess.check_call("set PYTHONIOENCODING=utf-8 && python tools/run_pipeline_ml.py", shell=True)
        print("ML Pipeline Passed.")
    except Exception as e:
        print("ML Pipeline Failed. Initiating Triage Director...")
        return
        
    print("Testing LSTM Pipeline...")
    try:
        subprocess.check_call("set PYTHONIOENCODING=utf-8 && python tools/run_pipeline_lstm.py", shell=True)
        print("LSTM Pipeline Passed.")
    except Exception as e:
        print("LSTM Pipeline Failed. Initiating Triage Director...")
        return

    print("All tests passed.")

if __name__ == "__main__":
    test_code()