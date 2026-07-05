import sys
from pathlib import Path

# Thêm root_dir vào sys.path để import từ src/
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.token_tracker import TokenTracker

def test_calculate_cost_flash():
    tracker = TokenTracker()
    cost = tracker._calculate_cost("gemini-2.5-flash", 1000000, 1000000)
    # prompt = 0.075, completion = 0.30 => Total = 0.375
    assert cost == 0.375

def test_calculate_cost_pro():
    tracker = TokenTracker()
    cost = tracker._calculate_cost("gemini-2.5-pro", 1000000, 1000000)
    # prompt = 3.50, completion = 10.50 => Total = 14.0
    assert cost == 14.0

def test_calculate_cost_unknown_model():
    tracker = TokenTracker()
    cost = tracker._calculate_cost("unknown-model", 1000000, 1000000)
    # Fallback to 0.1 prompt + 0.5 completion
    assert cost == 0.6
