import os
import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

class AIAuditReporter:
    """
    He thong tu dong sinh bao cao PDF ve tinh trang suc khoe va loi nhuan cua Vuong trieu AI.
    """
    def __init__(self):
        self.root_dir = Path(__file__).resolve().parent.parent
        self.report_dir = self.root_dir / "reports" / "daily"
        self.report_dir.mkdir(parents=True, exist_ok=True)
        
    def _get_airdrop_stats(self):
        db_path = self.root_dir / "projects" / "airdrop_guerrilla" / "data" / "airdrop_guerrilla.db"
        if not db_path.exists(): return "N/A"
        try:
            conn = sqlite3.connect(db_path)
            df = pd.read_sql_query("SELECT status, count(*) as count FROM onchain_logs GROUP BY status", conn)
            conn.close()
            return df.to_dict('records')
        except Exception: return "Error"

    def generate_pdf(self):
        today = datetime.now().strftime("%Y-%m-%d")
        file_name = self.report_dir / f"AI_Audit_Report_{today}.pdf"
        doc = SimpleDocTemplate(str(file_name), pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        # Title
        story.append(Paragraph(f"🏛️ AI SOVEREIGN AUDIT REPORT - {today}", styles['Title']))
        story.append(Spacer(1, 12))

        # 1. System Health
        story.append(Paragraph("1. System Health Status", styles['Heading2']))
        import psutil
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().available / (1024**3)
        health_data = [["Metric", "Value"], ["CPU Usage", f"{cpu}%"], ["RAM Available", f"{ram:.2f} GB"]]
        t = Table(health_data, colWidths=[200, 200])
        t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey), ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke)]))
        story.append(t)
        story.append(Spacer(1, 12))

        # 2. Airdrop Sentinel
        story.append(Paragraph("2. Airdrop Sentinel Activity", styles['Heading2']))
        stats = self._get_airdrop_stats()
        if isinstance(stats, list):
            airdrop_data = [["Status", "Count"]] + [[s['status'], s['count']] for s in stats]
            t2 = Table(airdrop_data, colWidths=[200, 200])
            t2.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.blue), ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke)]))
            story.append(t2)
        else:
            story.append(Paragraph(f"Status: {stats}", styles['Normal']))

        # Finalize
        doc.build(story)
        print(f"✅ Báo cáo PDF đã được tạo: {file_name}")
        return file_name

if __name__ == "__main__":
    reporter = AIAuditReporter()
    reporter.generate_pdf()
