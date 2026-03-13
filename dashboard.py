import os
import sys
import subprocess

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_menu():
    clear_screen()
    print("==========================================================")
    print("   🚀 HỆ THỐNG QUẢN LÝ TỔNG HỢP (MASTER DASHBOARD) 🚀")
    print("==========================================================")
    print("  [DỰ ÁN 2: BẤT ĐỘNG SẢN]")
    print("    1. 🏠 Chạy Web Dự báo BĐS & Bản đồ (Flask)")
    print("    2. ⏰ Khởi động Scheduler Tổng hợp (Cào BĐS & Trading)")
    print("    3. 🧠 Huấn luyện lại AI Mô hình BĐS (XGBoost)")
    print("")
    print("  [DỰ ÁN 3: AI TRADING AGENT]")
    print("    4. 🤖 Chạy AI Trading Live Advisor (Báo lệnh hôm nay)")
    print("    5. 📈 Chạy Backtest Mô phỏng AI Trading")
    print("    6. 🔄 Cập nhật Dữ liệu Giá & Tin tức mới nhất")
    print("")
    print("  [DỰ ÁN 1: AIRDROP GUERRILLA]")
    print("    7. 🎁 Chạy Bot cày Airdrop Zealy")
    print("    8. 🐦 Chạy Bot cày Twitter/Discord (Executor)")
    print("")
    print("  [DỰ ÁN 4: SILLYTAVERN WORLD CARD GENERATOR]")
    print("    9. 🃏 Chạy Web App Tạo World Card (Streamlit)")
    print("")
    print("  [DỰ ÁN 5: KNOWLEDGE BASE RAG AGENT]")
    print("   10. 📚 Nạp Dữ Liệu PDF Ebook vào ChromaDB")
    print("   11. 🧠 Chat/Hỏi đáp với Ebook Agent")
    print("")
    print("  [DỰ ÁN 6: JARVIS RPG ASSISTANT]")
    print("   12. 🦸‍♂️ Chạy Jarvis Dashboard (Streamlit RPG)")
    print("   13. 🗣️ Mở Terminal giao tiếp Jarvis CLI (Trợ lý cá nhân)")
    print("")
    print("  [QUẢN TRỊ HỆ THỐNG]")
    print("   14. 📊 Xuất Báo cáo Lịch sử Trading (Từ SQLite)")
    print("   15. 📝 Ghi Log Tiến độ Cập nhật (System Update Log)")
    print("   16. 💳 Kiểm tra số dư Binance Testnet (Live)")
    print("")
    print("  [0] ❌ Thoát")
    print("==========================================================")

def export_report():
    from src.database import SystemDB
    print("\n⏳ Đang truy xuất Database...")
    try:
        db = SystemDB()
        decisions = db.get_latest_decisions(limit=5)
        backtests = db.get_latest_backtests(limit=3)
        updates = db.get_latest_updates(limit=5)
        paper_trades = db.get_paper_trade_history(limit=5)
        db.close()
        
        report_content = "# 📊 BÁO CÁO HỆ THỐNG VÀ LỊCH SỬ CẬP NHẬT\n\n"
        
        report_content += "## 1. Kết quả Backtest Gần Nhất\n"
        if not backtests:
            report_content += "*Chưa có dữ liệu Backtest.*\n"
        else:
            for bt in backtests:
                report_content += f"- **Thời gian chạy:** {bt[0]}\n"
                report_content += f"  - Ticker: {bt[1]} ({bt[2]} -> {bt[3]})\n"
                report_content += f"  - ROI: **{bt[4]:.2f}%** | Sharpe: {bt[5]:.2f}\n"
                report_content += f"  - Max Drawdown: {bt[6]:.2f}% | Win Rate: {bt[7]:.2f}%\n\n"
                
        report_content += "## 2. Các Quyết định Live Advisor Gần Nhất\n"
        if not decisions:
            report_content += "*Chưa có quyết định nào được ghi nhận.*\n\n"
        else:
            for d in decisions:
                report_content += f"- **Ngày:** {d[0]} | Ticker: {d[1]} | Giá: ${d[2]:,.2f}\n"
                report_content += f"  - Hành động: **{d[3]}** (Tự tin: {d[4]}/10)\n"
                report_content += f"  - Lý do: {d[5]}\n\n"
                
        report_content += "## 3. Hiệu suất Paper Trading Gần Đây\n"
        if not paper_trades:
            report_content += "*Chưa có bản ghi Paper Trading nào.*\n\n"
        else:
            for pt in paper_trades:
                report_content += f"- **Ngày:** {pt[0]} | Tổng tài sản: **${pt[1]:,.2f}**\n"
            report_content += "\n"
                
        report_content += "## 4. Lịch sử Cập nhật Hệ thống (Changelog)\n"
        if not updates:
            report_content += "*Chưa có bản ghi cập nhật nào.*\n\n"
        else:
            for u in updates:
                report_content += f"- **[{u[0]}] Module {u[1]}:** {u[2]}\n"
                
        # Ghi ra file
        with open("LATEST_REPORT.md", "w", encoding="utf-8") as f:
            f.write(report_content)
            
        print("\n✅ Đã tạo thành công file: LATEST_REPORT.md")
        print("📄 Nội dung xem trước:\n")
        print(report_content)
        
    except Exception as e:
        print(f"❌ Lỗi truy xuất Database: {e}")
        
    input("\nBấm Enter để quay lại Menu chính...")

def log_system_update():
    from src.database import SystemDB
    print("\n📝 GHI NHẬN CẬP NHẬT HỆ THỐNG")
    module = input("Tên Module/Dự án vừa cập nhật (vd: AI Trading, BĐS): ").strip()
    desc = input("Mô tả thay đổi: ").strip()
    
    if module and desc:
        try:
            db = SystemDB()
            db.log_project_update(module, desc)
            db.close()
            print("✅ Đã lưu vào Database thành công!")
        except Exception as e:
            print(f"❌ Lỗi khi lưu vào Database: {e}")
    else:
        print("⚠️ Thông tin không được để trống. Hủy ghi log.")
        
    input("\nBấm Enter để quay lại Menu chính...")

def check_binance_balance():
    import sys
    from pathlib import Path
    
    # Add project root to path
    base_dir = Path(__file__).resolve().parent
    sys.path.append(str(base_dir))
    
    from projects.ai_trading_agent.binance_executor import BinanceExecutor
    
    executor = BinanceExecutor()
    executor.print_testnet_balance()
    
    input("\nBấm Enter để quay lại Menu chính...")

def run_script(script_path):
    try:
        # Lấy đường dẫn tuyệt đối để chạy file
        full_path = os.path.join(os.getcwd(), script_path)
        
        # Chạy subprocess và chờ kết thúc
        subprocess.run([sys.executable, full_path], check=True)
        print("\n✅ Tác vụ hoàn tất!")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Tác vụ bị lỗi hoặc bị dừng. Mã lỗi: {e.returncode}")
    except KeyboardInterrupt:
        print("\n🛑 Đã dừng tác vụ bởi người dùng.")
    except Exception as e:
        print(f"\n❌ Lỗi hệ thống: {e}")
    
    input("\nBấm Enter để quay lại Menu chính...")

def main():
    while True:
        print_menu()
        choice = input("Nhập lựa chọn của bạn (0-16): ").strip()
        
        if choice == '1':
            run_script("projects/real_estate_prediction/app.py")
        elif choice == '2':
            run_script("scheduler/main_scheduler.py")
        elif choice == '3':
            run_script("projects/real_estate_prediction/train_model.py")
        elif choice == '4':
            run_script("projects/ai_trading_agent/live_advisor.py")
        elif choice == '5':
            run_script("projects/ai_trading_agent/backtester.py")
        elif choice == '6':
            run_script("projects/ai_trading_agent/data_fetcher.py")
        elif choice == '7':
            run_script("projects/airdrop_guerrilla/src/automation/zealy_bot.py")
        elif choice == '8':
            run_script("projects/airdrop_guerrilla/src/automation/executor.py")
        elif choice == '9':
            print("\n🃏 Đang khởi động Web App Tạo Thẻ Thế Giới (SillyTavern)...")
            import subprocess
            try:
                subprocess.run(["streamlit", "run", "projects/sillytavern_world_card_generator/ui/app.py"], check=True)
            except Exception as e:
                print(f"❌ Lỗi chạy Streamlit: {e}")
        elif choice == '10':
            print("\n📚 Đang chạy Ingest PDF (Có thể mất thời gian)...")
            run_script("projects/knowledge_base_agent/src/ingest.py")
        elif choice == '11':
            print("\n🧠 Đang khởi động RAG Agent...")
            run_script("projects/knowledge_base_agent/src/rag_agent.py")
        elif choice == '12':
            print("\n🦸‍♂️ Đang khởi động Jarvis RPG Dashboard...")
            import subprocess
            try:
                subprocess.run(["streamlit", "run", "tools/dashboard.py"], cwd="projects/jarvis-rpg-assistant", check=True)
            except Exception as e:
                print(f"❌ Lỗi chạy Jarvis Dashboard: {e}")
        elif choice == '13':
            print("\n🗣️ Đã mở Terminal mới trỏ vào thư mục Jarvis. Bạn có thể gõ lệnh như 'python main.py daily'...")
            import subprocess
            try:
                subprocess.run('cmd.exe /c start "Jarvis CLI" /d "projects\\jarvis-rpg-assistant" cmd.exe', check=True)
            except Exception as e:
                print(f"❌ Lỗi mở Jarvis CLI: {e}")
        elif choice == '14':
            export_report()
        elif choice == '15':
            log_system_update()
        elif choice == '16':
            check_binance_balance()
        elif choice == '0':
            print("\n👋 Hẹn gặp lại! Đang tắt hệ thống...\n")
            sys.exit(0)
        else:
            input("\n⚠️ Lựa chọn không hợp lệ. Bấm Enter để thử lại...")

if __name__ == "__main__":
    main()
