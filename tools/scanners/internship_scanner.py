import os
import time
from datetime import datetime

def scan_internships():
    """
    Simulates scanning job boards (LinkedIn, TopDev, ITviec) for AI Intern positions.
    """
    print("Scanning job boards for AI Intern / Junior AI Engineer positions...")
    time.sleep(1)
    
    opportunities = [
        {
            "company": "TechMates VN",
            "position": "AI/ML Intern",
            "requirements": "Python, cơ bản về Machine Learning, ưu tiên biết về LLM/LangChain.",
            "status": "Ready to Auto-Apply",
            "fit_reason": "Có kinh nghiệm thực chiến với LangGraph Agent System."
        },
        {
            "company": "FinTech Innovators",
            "position": "Data Science Intern (Trading Models)",
            "requirements": "Xử lý dữ liệu time-series, XGBoost, Pandas. Đam mê tài chính.",
            "status": "Ready to Auto-Apply",
            "fit_reason": "Sở hữu project AI Trading Agent và Real Estate Prediction (XGBoost)."
        }
    ]

    report_path = os.path.join(os.path.dirname(__file__), "..", "reports", "internship_opportunities.md")
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"# AI Internship Opportunities - {datetime.now().strftime('%Y-%m-%d')}\n\n")
        f.write("Dưới đây là các vị trí thực tập AI phù hợp với hồ sơ năng lực của AI Factory:\n\n")
        
        for idx, opp in enumerate(opportunities, 1):
            f.write(f"### {idx}. {opp['position']} @ {opp['company']}\n")
            f.write(f"- **Yêu cầu:** {opp['requirements']}\n")
            f.write(f"- **Lý do phù hợp:** {opp['fit_reason']}\n")
            f.write(f"- **Trạng thái:** {opp['status']}\n\n")
            
    print(f"Scan complete. Report generated at: {report_path}")

if __name__ == "__main__":
    scan_internships()
