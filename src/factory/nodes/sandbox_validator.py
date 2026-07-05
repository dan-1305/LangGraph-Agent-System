import asyncio
import os
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

@dataclass
class ValidationResult:
    is_success: bool
    stdout: str
    stderr: str
    execution_time_ms: float
    return_code: int

class SandboxValidator:
    """
    Module cách ly để kiểm thử mã nguồn được sinh ra bởi Agent.
    Sử dụng runtime 'uv' phi đồng bộ để giảm thiểu overhead tối đa cho CPU.
    """
    def __init__(self, workspace_path: str, timeout: int = 30) -> None:
        self.workspace_path: str = workspace_path
        self.timeout: int = timeout

    async def execute_test_sandbox(self, test_target: str) -> ValidationResult:
        """
        Thực thi test suite một cách bất đồng bộ bằng lệnh 'uv run pytest'.
        Tránh nghẽn luồng chính của hệ thống LangGraph.
        """
        # Cấu hình biến môi trường lấy từ file .env an toàn
        env: Dict[str, str] = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"
        
        start_time: float = asyncio.get_event_loop().time()
        
        try:
            # Sử dụng non-blocking subprocess exec của asyncio
            process = await asyncio.create_subprocess_exec(
                "uv", "run", "pytest", test_target, "-v",
                cwd=self.workspace_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=env
            )
            
            # Chốt chặn Timeout bảo vệ tài nguyên máy trạm không bị treo luồng vô hạn
            stdout_bytes, stderr_bytes = await asyncio.wait_for(
                process.communicate(), 
                timeout=float(self.timeout)
            )
            
            end_time: float = asyncio.get_event_loop().time()
            execution_time: float = (end_time - start_time) * 1000
            
            return ValidationResult(
                is_success=(process.returncode == 0),
                stdout=stdout_bytes.decode("utf-8", errors="ignore"),
                stderr=stderr_bytes.decode("utf-8", errors="ignore"),
                execution_time_ms=execution_time,
                return_code=process.returncode if process.returncode is not None else -1
            )
            
        except asyncio.TimeoutError:
            return ValidationResult(
                is_success=False,
                stdout="",
                stderr="CRITICAL: Sandbox execution timed out.",
                execution_time_ms=float(self.timeout * 1000),
                return_code=-9
            )

def sandbox_validator_node(state: dict):
    """
    Node LangGraph thực thi kiểm thử. 
    Lưu ý: Vì Graph chính chạy bất đồng bộ (ainvoke), ta có thể sử dụng asyncio.run (hoặc await nếu đổi node thành async).
    Trong mô hình state graph hiện tại, ta có thể dùng một event loop nhỏ hoặc thiết lập node dạng async.
    """
    print("--- [Sandbox Validator] Kích hoạt ---")
    
    # Lấy thông số từ môi trường hoặc mặc định
    timeout = int(os.getenv("AGENT_SANDBOX_TIMEOUT", "45"))
    validator = SandboxValidator(workspace_path=".", timeout=timeout)
    
    # Chạy đồng bộ (do node này hiện đang đăng ký dạng sync, LangGraph sẽ gọi nó trong executor)
    # Tuy nhiên SandboxValidator là async, ta dùng asyncio.run để chặn ở mức node
    test_target = state.get("test_target", "tests/") 
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result: ValidationResult = loop.run_until_complete(validator.execute_test_sandbox(test_target))
    finally:
        loop.close()
    
    # Ghi nhận kết quả
    state["test_results_ptr"] = f"Success: {result.is_success}\nOutput:\n{result.stdout}\nErrors:\n{result.stderr}"
    state["sandbox_success"] = result.is_success
    
    if result.is_success:
        print("[Sandbox Validator] ✅ Kiểm thử Thành công.")
    else:
        print(f"[Sandbox Validator] ❌ Kiểm thử Thất bại (Mã lỗi {result.return_code}).")
        
    return state
