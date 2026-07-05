import os
import sys
import time
import subprocess
import requests

def test_shadow_sentinel_api():
    print("[+] Khoi dong Shadow Sentinel V6 API (Local mode, Docker not available)...")
    
    # Run API
    env = os.environ.copy()
    env["PYTHONPATH"] = ".;../.."
    api_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "api:app", "--host", "127.0.0.1", "--port", "8080"],
        env=env,
        cwd="projects/nsfw_multimedia_auditor",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for API to start (NudeNet takes time to load)
    print("Waiting 30 seconds for NudeNet to load...")
    time.sleep(30)
    
    # Check if process is still running
    if api_process.poll() is not None:
        out, err = api_process.communicate()
        print(f"API crashed. STDERR: {err.decode('utf-8', errors='ignore')}")
        return

    # Create test directory and a dummy image (absolute path to avoid cwd issues)
    test_dir = os.path.abspath("data/NSFW/TestFrames")
    os.makedirs(test_dir, exist_ok=True)
    import cv2
    import numpy as np
    dummy_img = np.zeros((100, 100, 3), dtype=np.uint8)
    cv2.imwrite(os.path.join(test_dir, "test_frame.jpg"), dummy_img)
    
    try:
        print("Calling API...")
        response = requests.post(
            "http://127.0.0.1:8080/api/v1/audit",
            json={"frames_dir": test_dir},
            timeout=10
        )
        print(f"Status Code: {response.status_code}")
        try:
            print(f"Response: {response.json()}")
        except Exception:
            print("Response contains unicode that cannot be printed in this terminal.")
    except Exception as e:
        print(f"Error calling API: {e}")
        out, err = api_process.communicate(timeout=2)
        print(f"API STDERR: {err.decode('utf-8', errors='ignore')}")
    finally:
        api_process.terminate()
        api_process.wait()
        print("Shadow Sentinel V6 API Terminated.")

if __name__ == "__main__":
    test_shadow_sentinel_api()