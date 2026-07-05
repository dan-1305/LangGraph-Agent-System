import sys
import os
import json
import traceback
import codecs

# Force stdout to be UTF-8 for Windows Terminal
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

# Setup environment path so we can import src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.factory.config import create_fallback_chain
from langchain_core.prompts import PromptTemplate
from chaos_monkey import ChaosMonkey

# Monkey Patch Langchain's BaseChatModel
from langchain_core.language_models.chat_models import BaseChatModel

monkey = ChaosMonkey(failure_rate=0.6) # 60% tỉ lệ tàn phá API
original_invoke = BaseChatModel.invoke

@monkey.inject_chaos
def chaotic_invoke(self, *args, **kwargs):
    return original_invoke(self, *args, **kwargs)

BaseChatModel.invoke = chaotic_invoke

def run_test():
    print("Khởi động Bầy Khỉ Hỗn Loạn (Chaos Monkey)...")
    
    prompt = PromptTemplate.from_template("Hãy trả lời ngắn gọn 1 câu duy nhất: 1 + 1 bằng mấy? Bắt buộc output phải là JSON theo định dạng: {{\\\"result\\\": \\\"<đáp án>\\\"}}")
    flash_model_list = ["gemini-3-flash-preview", "gemini-2.5-flash", "gemini-1.5-flash"]
    chain = create_fallback_chain(flash_model_list, temperature=0.1, max_tokens=100)
    
    success_count = 0
    failure_count = 0
    corrupted_json_count = 0
    
    report = []
    
    for i in range(1, 21):
        print(f"\\n--- REQUEST #{i} ---")
        try:
            res = chain.invoke({"input": ""})
            content = res.content
            print(f"Output nhận được: {content[:50]}...")
            
            # Check JSON
            try:
                # Xóa backtick nếu có
                clean_content = content.replace("```json", "").replace("```", "").strip()
                data = json.loads(clean_content)
                if "result" in data:
                    print("=> THÀNH CÔNG: JSON hợp lệ và vượt qua Chaos!")
                    success_count += 1
                    report.append({"request": i, "status": "SUCCESS", "reason": "Valid JSON"})
                else:
                    print("=> THẤT BẠI: JSON thiếu key 'result'")
                    failure_count += 1
                    report.append({"request": i, "status": "FAIL", "reason": "Missing Key"})
            except json.JSONDecodeError:
                print("=> LỖI PARSE: Output bị vỡ (Corrupted JSON) do ảo giác!")
                corrupted_json_count += 1
                report.append({"request": i, "status": "CORRUPTED", "reason": "JSON Decode Error"})
                
        except Exception as e:
            print(f"=> THẤT BẠI HOÀN TOÀN: Fallback Matrix bị xuyên thủng! Lỗi: {str(e)[:50]}...")
            failure_count += 1
            report.append({"request": i, "status": "CRITICAL_FAIL", "reason": str(e)})

    print("\\n================ TỔNG KẾT CHIẾN DỊCH CHAOS ================")
    print(f"Tổng số Request: 20")
    print(f"Thành công (Vượt qua mạng sập): {success_count}")
    print(f"Sập nguồn (API chết hẳn): {failure_count}")
    print(f"Lỗi Ảo giác (Corrupted JSON): {corrupted_json_count}")
    
    # Xuất file
    os.makedirs(os.path.join(os.path.dirname(__file__), 'output'), exist_ok=True)
    with open(os.path.join(os.path.dirname(__file__), 'output', 'chaos_report.json'), 'w', encoding='utf-8') as f:
        json.dump({"success": success_count, "fail": failure_count, "corrupted": corrupted_json_count, "logs": report}, f, indent=4, ensure_ascii=False)
        
    print(f"Đã lưu report tại: tests/chaos_module/output/chaos_report.json")

if __name__ == "__main__":
    run_test()
