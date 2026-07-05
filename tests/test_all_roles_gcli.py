import sys
import json
from pathlib import Path

# Add root to pythonpath
sys.path.append(str(Path(__file__).resolve().parent.parent))

from tools.system.gcli_delegate import GCLIDelegateAgent
from src.base_agent import BaseAgent

MOCK_DIR = Path(__file__).resolve().parent / "mock_data"
REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"

MOCK_FILES = {
    "Architect": {
        "file": MOCK_DIR / "mock_arch.py",
        "role": "Principal System Architect",
        "format": "markdown",
        "content": "class A:\n    def b(self):\n        return C().d()\nclass C:\n    def d(self):\n        pass\n"
    },
    "Backend": {
        "file": MOCK_DIR / "mock_req.txt",
        "role": "Senior Backend Developer",
        "format": "markdown",
        "content": "Tạo một app FastAPI cơ bản với 1 route GET /ping trả về {'status': 'ok'}."
    },
    "Triage": {
        "file": MOCK_DIR / "mock_error.log",
        "role": "Triage Director / Chaos Engineer",
        "format": "markdown",
        "content": "Traceback (most recent call last):\n  File 'main.py', line 10, in <module>\n    1/0\nZeroDivisionError: division by zero"
    },
    "Content": {
        "file": MOCK_DIR / "mock_lore.txt",
        "role": "Content / Creative Director",
        "format": "json",
        "content": "Nhân vật tên là Lyra. Cô ấy 25 tuổi, thích đọc sách và màu xanh dương. Có sức mạnh phép thuật."
    },
    "SRE": {
        "file": MOCK_DIR / "mock_docker.txt",
        "role": "SRE / DevOps Commander",
        "format": "markdown",
        "content": "CONTAINER ID   NAME      CPU %     MEM USAGE / LIMIT     MEM %     NET I/O\n1234567890ab   redis     0.05%     1.5GiB / 2GiB         75.0%     1kB / 0B"
    },
    "QA": {
        "file": MOCK_DIR / "mock_diff.txt",
        "role": "QA & Security Auditor",
        "format": "json",
        "content": "+ AWS_SECRET_ACCESS_KEY = 'AKIAIOSFODNN7EXAMPLE'\n+ def get_user(id):\n+     db.execute(f'SELECT * FROM users WHERE id = {id}')"
    },
    "ML": {
        "file": MOCK_DIR / "mock_vram.txt",
        "role": "AI/ML Engineer",
        "format": "markdown",
        "content": "| 0  NVIDIA GeForce RTX 4090 | 99%   24000MiB / 24576MiB |"
    }
}

def create_mocks():
    MOCK_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(exist_ok=True)
    for key, data in MOCK_FILES.items():
        with open(data["file"], "w", encoding="utf-8") as f:
            f.write(data["content"])

class ArenaJudge(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(model_name="label:tier-1", **kwargs)
        
    def _ai_handler(self, test_results: str) -> str:
        prompt = f"""
[ROLE: OVERLORD / PRINCIPAL ARCHITECT]
Nhiệm vụ: Bạn vừa nhận được log kết quả của Đấu trường "The Grand Arena". Trong đó, 7 Role đã sử dụng Vũ khí GCLI Delegation để giải quyết 7 loại Mock Data khác nhau, lặp lại trong 3 vòng (để kiểm tra độ ổn định/ảo giác).
Hãy phân tích chéo kết quả này và đưa ra đánh giá:
1. Role nào thực hiện tốt nhất, ổn định nhất qua 3 vòng?
2. Role nào có kết quả kém ổn định nhất (bị Hallucination, sinh sai JSON, hay giải quyết chưa dứt điểm)?
3. Kiến nghị bổ sung Giáp/Vũ khí gì tiếp theo?

Kết quả 3 vòng đấu:
{test_results}

Trả về định dạng Markdown.
"""
        response = self._call_llm(prompt, is_json=False)
        return response

    def _logic_handler(self, test_results: str) -> str:
        return "# Lỗi phân tích The Grand Arena (Logic Fallback)."

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    print("🚀 Bắt đầu tạo Mock Data cho 7 Đội trưởng...")
    create_mocks()
    
    all_results = {}
    
    for loop in range(1, 4):
        print(f"\n--- ⚔️ THE GRAND ARENA: VÒNG LẶP {loop}/3 ⚔️ ---")
        all_results[f"loop_{loop}"] = {}
        
        for role_key, data in MOCK_FILES.items():
            print(f"👉 Kích hoạt: {data['role']} ({role_key})...")
            
            with open(data["file"], "r", encoding="utf-8") as f:
                payload = f.read()
                
            agent = GCLIDelegateAgent(role_context=data["role"])
            result = agent.execute(payload=payload, output_format=data["format"])
            
            # Lưu log lại để đánh giá
            # Cắt ngắn result để đỡ tốn context khi gửi cho Judge
            all_results[f"loop_{loop}"][role_key] = result[:300] + " ...[TRUNCATED]" if len(result) > 300 else result
            print(f"   ✅ Xong {role_key}! Output length: {len(result)} bytes")
            
    print("\n🧠 Kích hoạt Overlord Judge (Gemini 3.1 Pro) để phân tích chéo 21 kết quả...")
    judge = ArenaJudge()
    evaluation = judge.execute(test_results=json.dumps(all_results, indent=2, ensure_ascii=False))
    
    report_path = REPORTS_DIR / "GRAND_ARENA_EVALUATION.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(evaluation)
        
    print(f"\n✅ Đấu trường kết thúc. Kết quả đánh giá đã lưu tại: {report_path}")

if __name__ == "__main__":
    main()
