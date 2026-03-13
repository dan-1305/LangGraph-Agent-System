import os
import re
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from langchain_experimental.utilities import PythonREPL
from .state import AgentState

# Khởi tạo công cụ thực thi code
python_repl = PythonREPL()

# Định nghĩa các LLMs cho từng Agent
llm_planner = ChatOpenAI(model="gemini-3.1-pro-preview", base_url=os.getenv("GCLI_BASE_URL"), api_key=os.getenv("GCLI_API_KEY"))
llm_architect = ChatOpenAI(model="gemini-2.5-pro", base_url=os.getenv("GCLI_BASE_URL"), api_key=os.getenv("GCLI_API_KEY"))
llm_worker = ChatOpenAI(model="gemini-2.5-flash", base_url=os.getenv("GCLI_BASE_URL"), api_key=os.getenv("GCLI_API_KEY"))
llm_reviewer = ChatOpenAI(model="gemini-3.1-pro-preview", base_url=os.getenv("GCLI_BASE_URL"), api_key=os.getenv("GCLI_API_KEY"))

def planner_node(state: AgentState) -> dict:
    """
    Agent Planner: Lên kế hoạch tổng thể dựa trên yêu cầu và dữ liệu đầu vào.
    """
    print("--- PLANNER: LẬP KẾ HOẠCH TỔNG THỂ ---")
    prompt = f"""Dữ liệu CSV: {state['csv_info']}
    Nhiệm vụ: {state['task']}
    Feedback cũ từ Reviewer: {state.get('review_feedback', 'Chưa có')}
    
    Vai trò của bạn là AI Planner. Dựa trên yêu cầu, hãy lập một kế hoạch nghiệp vụ tổng thể (không viết code). 
    Phân rã yêu cầu thành các Milestones rõ ràng (Giai đoạn 1, 2, 3...). Tùy thuộc vào yêu cầu là Data Science, Web App, Crypto Bot hay bất cứ thứ gì, hãy lập kế hoạch phù hợp.
    Lưu ý: Nếu có yêu cầu lưu file (model, report...), hãy đảm bảo kế hoạch có nhắc đến việc này ở bước cuối.
    
    YÊU CẦU BẮT BUỘC: Bạn phải bắt đầu bằng một thẻ <reasoning>...</reasoning> để tự hỏi và trả lời: 
    1. Bản chất của dự án này là gì (Data, Web, Automation...)?
    2. Các rủi ro kỹ thuật chính là gì?
    3. Trình tự (Milestones) tốt nhất để giải quyết là gì?
    Sau thẻ <reasoning>, mới trình bày kế hoạch chi tiết."""
    response = llm_planner.invoke(prompt)
    return {"plan": response.content, "revision_count": state.get("revision_count", 0) + 1}

def architect_node(state: AgentState) -> dict:
    """
    Agent Architect: Chuyển đổi kế hoạch thành thiết kế kỹ thuật chi tiết, 
    chống Data Leakage và giới hạn tài nguyên hệ thống.
    """
    print("--- ARCHITECT: THIẾT KẾ KIẾN TRÚC KỸ THUẬT ---")
    
    error_log_content = ""
    force_rewrite_prompt = ""
    if "error_log_path" in state and os.path.exists(state["error_log_path"]):
        try:
            with open(state["error_log_path"], "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            unfixed_errors = [line for line in lines if "[FIXED]" not in line]
            if unfixed_errors:
                error_log_content = "DANH SÁCH LỖI CHƯA ĐƯỢC GIẢI QUYẾT TỪ CÁC LẦN CHẠY TRƯỚC:\n" + "".join(unfixed_errors)
                
                # Đếm lỗi lặp lại (ví dụ NameError)
                error_types = [line.split("]:")[0].split("[")[-1] for line in unfixed_errors if "]:" in line]
                for err_type in set(error_types):
                    if error_types.count(err_type) >= 2:
                        force_rewrite_prompt = f"\nCẢNH BÁO NGHIÊM TRỌNG: Lỗi {err_type} đã lặp lại nhiều lần. BẠN PHẢI THIẾT KẾ LẠI TOÀN BỘ SCRIPT và thêm khối Standard Import Block (os, pandas, numpy, sklearn...) ở đầu file. Tuyệt đối không chỉ đề xuất sửa một dòng."
                        break
        except Exception as e:
            error_log_content = f"Không thể đọc file lỗi: {e}"

    prompt = f"""Kế hoạch tổng thể: {state['plan']}
    Cấu trúc dữ liệu: {state['csv_info']}
    Tóm tắt lịch sử lỗi: {state.get('summary_history', '')}
    {error_log_content}
    {force_rewrite_prompt}
    
    Vai trò của bạn là AI Architect. Hãy chuyển kế hoạch trên thành thiết kế kỹ thuật (Blueprinting) chi tiết cho Worker viết code.
    Bạn phải xác định rõ CÔNG CỤ (Tools), Thư viện (Libraries) và APIs cần thiết cho dự án này (dù là Data Science, Automation hay App).
    
    YÊU CẦU BẮT BUỘC: Bạn phải bắt đầu bằng một thẻ <reasoning>...</reasoning> để phân tích:
    1. Kế hoạch này cần sử dụng những công nghệ/thư viện cốt lõi nào?
    2. Cần những thư viện/import cụ thể nào để code chạy không bị NameError?
    3. Logic nào phù hợp để tối ưu trên cấu hình máy CPU yếu (tránh đa luồng nặng)?
    Sau thẻ <reasoning>, mới trình bày thiết kế.

    Yêu cầu bắt buộc phải đưa vào thiết kế (Hệ thống ràng buộc):
    1. Nếu là dự án Data Science (ML): Tránh Data Leakage (chia Train/Test trước xử lý), dùng K-Fold nhỏ (CV=3), và luôn set n_jobs=1.
    2. TRÁNH LỖI MÔI TRƯỜNG REPL: 
       - Code sẽ được chạy trong Python REPL, vì vậy KHÔNG BAO GIỜ SỬ DỤNG biến `__file__`. Hãy dùng `os.getcwd()` để lấy đường dẫn.
       - Hạn chế bọc tất cả trong hàm `main()` rồi gọi, hãy viết code phẳng hoặc đảm bảo hàm thực thi chuẩn xác.
    
    Hãy viết ra danh sách các bước lập trình chi tiết, cụ thể từng tên hàm, thư viện cần dùng.
    3. CỰC KỲ QUAN TRỌNG: Khai báo rõ MỌI thư viện cần dùng để Worker không bị thiếu import."""
    response = llm_architect.invoke(prompt)
    return {"architecture": response.content}

import traceback
import datetime
import ast

def worker_node(state: AgentState) -> dict:
    """
    Agent Worker: Viết mã Python dựa trên thiết kế của Architect và thực thi.
    """
    print("--- WORKER: VIẾT VÀ CHẠY CODE ---")
    prompt = f"""Thiết kế kỹ thuật: {state['architecture']}
    Feedback cũ từ Reviewer: {state.get('review_feedback', 'Chưa có')}
    
    Vai trò của bạn là Coder. Hãy viết 1 đoạn mã Python hoàn chỉnh thực thi chính xác thiết kế kỹ thuật trên.
    
    YÊU CẦU BẮT BUỘC: Bạn phải bắt đầu bằng một thẻ <reasoning>...</reasoning> để tự phân tích xem thiết kế này yêu cầu những thư viện gì, đường dẫn file xử lý thế nào để không lỗi. Sau thẻ <reasoning>, MỚI XUẤT CODE PYTHON.
    
    Lưu ý: 
    - CHỈ XUẤT CODE PYTHON sau thẻ <reasoning>, KHÔNG GIẢI THÍCH THÊM (có thể print báo cáo kết quả trong code).
    - KHÔNG SỬ DỤNG biến `__file__` vì code chạy trong REPL (nếu cần thư mục gốc, dùng `os.getcwd()`).
    - Phải chủ động import mọi thư viện bạn dùng (pandas, numpy, re, sklearn...) ngay trong code của bạn. Đừng dựa dẫm vào inject.
    - Dùng thư viện pathlib hoặc os.path kết hợp `os.getcwd()` để nối file projects/real_estate_prediction/data/raw_data.csv.
    - Cuối cùng lưu mô hình thành thư mục projects/real_estate_prediction/models/model.pkl. Không lưu ở thư mục gốc."""
    
    # Sinh code
    response = llm_worker.invoke(prompt)
    
    # Extract code safely using regex
    match = re.search(r"```(?:python)?(.*?)```", response.content, re.DOTALL)
    if match:
        code = match.group(1).strip()
    else:
        code = response.content.strip()
    
    # Header chuẩn để chống NameError
    STANDARD_IMPORTS = """
import os
import re
import joblib
import warnings
from pathlib import Path
import pandas as pd
import numpy as np
warnings.filterwarnings('ignore')
"""
    final_code = STANDARD_IMPORTS + "\n" + code

    # Kiểm tra tĩnh cơ bản (Basic Static Check) cho các thư viện ML nếu có gọi mà chưa import
    if "sklearn" in code and "import sklearn" not in code and "from sklearn" not in code:
        return {"draft": code, "execution_log": "ERROR:\nNameError: Thiếu import cho sklearn. Yêu cầu thêm import các module sklearn cần thiết vào code."}
    
    # Static Check: Kiểm tra cú pháp Python trước khi chạy
    try:
        ast.parse(final_code)
    except SyntaxError as e:
        error_msg = f"SyntaxError tại dòng {e.lineno}, cột {e.offset}: {e.msg}\nCode có lỗi cú pháp, yêu cầu viết lại cẩn thận."
        return {"draft": code, "execution_log": f"ERROR:\n{error_msg}"}

    # Thực thi code
    try:
        result = python_repl.run(final_code)
        return {"draft": code, "execution_log": f"SUCCESS:\n{result}"}
    except Exception as e:
        error_detail = traceback.format_exc()
        error_type = type(e).__name__
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Ghi log lỗi vào file
        if "error_log_path" in state:
            try:
                # Đảm bảo thư mục tồn tại
                os.makedirs(os.path.dirname(state["error_log_path"]), exist_ok=True)
                with open(state["error_log_path"], "a", encoding="utf-8") as f:
                    f.write(f"[{timestamp}] [worker_node] [{error_type}]: {str(e)}\n")
            except Exception as io_err:
                print(f"Lỗi khi ghi log: {io_err}")

        return {"draft": code, "execution_log": f"ERROR:\n{error_detail}"}

def reviewer_node(state: AgentState) -> dict:
    """
    Agent Reviewer: Kiểm duyệt chất lượng mã nguồn, phát hiện Data Leakage và 
    đảm bảo mô hình không Overfitting.
    """
    print("--- REVIEWER: KIỂM TRA ĐÁNH GIÁ ---")
    prompt = f"""Yêu cầu gốc: {state['task']}
    Code Worker đã viết: {state['draft']}
    Kết quả thực thi thực tế: {state['execution_log']}
    
    Vai trò của bạn là Reviewer.
    
    YÊU CẦU BẮT BUỘC: Bạn phải bắt đầu bằng một thẻ <reasoning>...</reasoning> để phân tích xem có lỗi gì ẩn giấu về Data Leakage hay Overfitting không, hoặc tại sao lỗi runtime lại xảy ra. Sau thẻ <reasoning>, mới đưa ra nhận xét hoặc chữ 'OK'.
    
    Đánh giá dựa trên yêu cầu gốc. Bạn là "Quality Gate".
    1. Nếu có lỗi (ERROR) Runtime, hãy chỉ ra cách fix. NẾU lỗi là SyntaxError, HÃY GẮT GAY yêu cầu Architect và Worker CHỈ XUẤT MÃ PYTHON TRONG KHỐI ```python, KHÔNG ĐƯỢC CHÈN TEXT GIẢI THÍCH LẪN VÀO CODE.
    2. Nếu là dự án Data Science: Kiểm tra Data Leakage và Overfitting (R2, MAE).
       - LUẬT CHẨN ĐOÁN (Diagnostic Rule) BẮT BUỘC: Đọc trong execution_log để tìm "Số lượng dòng của tập huấn luyện" (len(X_train)) và tính khoảng cách Overfitting "gap = R2_train - R2_test". NẾU len(X_train) < 1000 HOẶC gap > 0.15, bạn KHÔNG ĐƯỢC PHÉP báo SUCCESS hay OK. Bạn PHẢI trả về chính xác dòng chữ sau (thay [X] và [Y] bằng số liệu thực tế):
       "DATA_STARVATION_WARNING: Dữ liệu hiện tại chỉ có [X] dòng, quá ít để mô hình học tổng quát, dẫn đến Overfitting (Gap = [Y]). NGHIÊM CẤM THỬ ĐỔI THUẬT TOÁN MODEL NỮA. YÊU CẦU DỪNG LẠI VÀ BÁO CÁO CON NGƯỜI để cào thêm dữ liệu thô (ít nhất 1000 dòng) hoặc làm sạch Outliers sâu hơn."
    3. Nếu là dự án khác (Bot, Web, Script): Kiểm tra xem code đã thực hiện đủ logic yêu cầu chưa.
    4. Nếu thấy lỗi 'NameError', hãy mạnh mẽ chỉ trích việc quên import thư viện.
    
    Nếu MỌI THỨ TỐT ĐẸP và ĐẠT YÊU CẦU (vượt qua cả Luật chẩn đoán), chỉ cần trả về chữ 'OK' sau thẻ <reasoning>. Nếu chưa đạt, hãy phân tích lỗi chi tiết để hệ thống làm lại."""
    response = llm_reviewer.invoke(prompt)
    
    review_feedback = response.content
    summary_history = state.get("summary_history", "")
    
    # Recursive Summarization nếu có lỗi
    if "ERROR" in state['execution_log'] or "OK" not in review_feedback.strip()[:5]:
        summary_prompt = f"""Dưới đây là tóm tắt lịch sử lỗi trước đó:
{summary_history}
Và đây là lỗi/phản hồi mới nhất:
Lỗi: {state['execution_log'][:500]}
Review: {review_feedback[:500]}

Hãy viết một tóm tắt siêu ngắn gọn (dưới 3 câu) tổng hợp lại các lỗi đã gặp và những gì chưa giải quyết được. Không giải thích thêm."""
        summary_response = llm_worker.invoke(summary_prompt)
        summary_history = summary_response.content
    
    # Nếu code chạy thành công, đánh dấu các lỗi cũ trong error_log.md là FIXED
    if "SUCCESS" in state['execution_log'] and "error_log_path" in state and os.path.exists(state["error_log_path"]):
        try:
            with open(state["error_log_path"], "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            # Cập nhật các dòng chưa có FIXED
            updated_lines = []
            for line in lines:
                if line.strip() and "[FIXED]" not in line:
                    updated_lines.append(f"[FIXED] {line}")
                else:
                    updated_lines.append(line)
            
            with open(state["error_log_path"], "w", encoding="utf-8") as f:
                f.writelines(updated_lines)
        except Exception as e:
            print(f"Lỗi khi cập nhật log: {e}")

    return {
        "review_feedback": review_feedback, 
        "summary_history": summary_history,
        "execution_log": state['execution_log'][:1000] + "\n...[TRUNCATED]" if len(state['execution_log']) > 1000 else state['execution_log'],
        "revision_count": state.get("revision_count", 0) + 1
    }
