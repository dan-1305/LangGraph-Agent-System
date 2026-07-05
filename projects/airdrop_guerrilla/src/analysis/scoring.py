import os
import io
import sys
import sqlite3
import pandas as pd
from typing import List, Dict, Any
from pathlib import Path

# Force stdout to be UTF-8 for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class AlphaAnalyzer:
    """
    AlphaAnalyzer: Module đánh giá tiềm năng Airdrop của các dự án Crypto.
    Dựa trên số tiền gọi vốn (Funding) và danh tiếng của Quỹ đầu tư (VC Tier).
    """
    
    # Định nghĩa các Tier của Venture Capital
    VC_TIERS = {
        'tier_1': ['a16z', 'paradigm', 'binance labs', 'polychain', 'multicoin', 'coinbase ventures'],
        'tier_2': ['animoca', 'dragonfly', 'spartan', 'pantera', 'okx ventures'],
    }
    
    # Trọng số cho từng Tier
    WEIGHTS = {
        'tier_1': 10,
        'tier_2': 5,
        'others': 1
    }

    @classmethod
    def get_vc_weight(cls, investors: List[str]) -> int:
        """
        Xác định trọng số lớn nhất dựa trên danh sách các quỹ đầu tư của dự án.
        Chỉ cần có 1 quỹ Tier 1 tham gia là dự án được tính điểm Tier 1.
        
        Args:
            investors (List[str]): Danh sách tên các quỹ đầu tư.
            
        Returns:
            int: Trọng số tương ứng.
        """
        if not investors:
            return cls.WEIGHTS['others']
            
        investors_lower = [inv.lower() for inv in investors]
        
        # Kiểm tra Tier 1
        for vc in cls.VC_TIERS['tier_1']:
            if any(vc in inv for inv in investors_lower):
                return cls.WEIGHTS['tier_1']
                
        # Kiểm tra Tier 2
        for vc in cls.VC_TIERS['tier_2']:
            if any(vc in inv for inv in investors_lower):
                return cls.WEIGHTS['tier_2']
                
        return cls.WEIGHTS['others']

    @classmethod
    def calculate_score(cls, funding_amount: float, investors: List[str], risk_factor: float = 1.0) -> float:
        """
        Tính toán điểm số tiềm năng (Alpha Score).
        Công thức: Score = (Funding_Amount * VC_Tier_Weight) / Risk_Factor
        
        Args:
            funding_amount (float): Tổng số tiền gọi vốn (tính bằng triệu USD để con số không quá lớn).
            investors (List[str]): Danh sách các quỹ đầu tư.
            risk_factor (float): Hệ số rủi ro (mặc định 1.0, dự án càng rủi ro hệ số càng cao).
            
        Returns:
            float: Điểm số Alpha.
        """
        vc_weight = cls.get_vc_weight(investors)
        
        # Đảm bảo risk_factor không bằng 0 để tránh lỗi chia cho 0
        safe_risk = max(0.1, risk_factor)
        
        score = (funding_amount * vc_weight) / safe_risk
        return round(score, 2)

    @classmethod
    def analyze_projects(cls, projects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Phân tích và chấm điểm hàng loạt dự án.
        
        Args:
            projects (List[Dict]): Danh sách thông tin dự án.
            
        Returns:
            List[Dict]: Danh sách dự án đã được bổ sung cột Alpha_Score và sắp xếp giảm dần theo điểm.
        """
        results = []
        for p in projects:
            # Chuyển đổi Funding Amount sang đơn vị Triệu USD (M) để tính toán dễ nhìn
            funding_m = p.get('funding_usd', 0) / 1_000_000
            investors = p.get('investors', [])
            risk = p.get('risk_factor', 1.0)
            
            score = cls.calculate_score(funding_amount=funding_m, investors=investors, risk_factor=risk)
            
            project_data = p.copy()
            project_data['alpha_score'] = score
            results.append(project_data)
            
        # Sắp xếp các dự án tiềm năng nhất lên đầu
        results.sort(key=lambda x: x['alpha_score'], reverse=True)
        return results

class AirdropScoringEngine:
    def __init__(self, db_path: str = None):
        if db_path is None:
            base_dir = Path(__file__).resolve().parent.parent.parent
            self.db_path = str(base_dir / "data" / "airdrop_guerrilla.db")
        else:
            self.db_path = db_path

    def calculate_wallet_metrics(self, wallet_address: str) -> dict:
        """Truy vấn SQLite và tính toán ma trận điểm cho từng ví."""
        if not os.path.exists(self.db_path):
            return {"address": wallet_address, "total_score": 0, "status": "No DB"}
            
        conn = sqlite3.connect(self.db_path)
        
        # Đọc dữ liệu log của ví cụ thể
        query = "SELECT timestamp, network_name, action_type, status FROM onchain_logs WHERE wallet_address = ?"
        df = pd.read_sql_query(query, conn, params=(wallet_address,))
        conn.close()
        
        if df.empty:
            return {
                "address": wallet_address,
                "active_days": 0,
                "tx_count": 0,
                "deploy_count": 0,
                "total_score": 0,
                "tier": "Newbie"
            }

        # Trích xuất các chỉ số từ DataFrame
        df['date'] = pd.to_datetime(df['timestamp']).dt.date
        active_days = df[df['status'] == 'SUCCESS']['date'].nunique()
        tx_count = df[(df['status'] == 'SUCCESS') & (df['action_type'] == 'Transfer')].shape[0]
        deploy_count = df[(df['status'] == 'SUCCESS') & (df['action_type'] == 'Deploy Contract')].shape[0]
        failed_count = df[df['status'] == 'FAILED'].shape[0]

        # Tính toán điểm tổng hợp theo thuật toán
        total_score = (active_days * 50) + (tx_count * 10) + (deploy_count * 200) - (failed_count * 100)

        return {
            "address": wallet_address,
            "active_days": active_days,
            "tx_count": tx_count,
            "deploy_count": deploy_count,
            "total_score": max(0, total_score),
            "tier": "Tier 1 (VIP)" if total_score >= 1000 else "Tier 2 (Standard)"
        }

    def generate_markdown_report(self, output_path: str):
        """Quét toàn bộ ví trong DB và tạo báo cáo Markdown."""
        if not os.path.exists(self.db_path):
            print("❌ Không tìm thấy database.")
            return
            
        conn = sqlite3.connect(self.db_path)
        wallets_df = pd.read_sql_query("SELECT DISTINCT wallet_address FROM onchain_logs", conn)
        conn.close()
        
        if wallets_df.empty:
            print("⚠️ Chưa có dữ liệu giao dịch nào trong DB.")
            return
            
        results = []
        for wallet in wallets_df['wallet_address']:
            metrics = self.calculate_wallet_metrics(wallet)
            results.append(metrics)
            
        # Sắp xếp theo điểm giảm dần
        results.sort(key=lambda x: x['total_score'], reverse=True)
        
        # Tạo Markdown content
        md_content = "# 🏆 BẢNG XẾP HẠNG VÍ AIRDROP (MONI SCORE)\n\n"
        md_content += f"*Cập nhật lúc: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
        md_content += "| Xếp hạng | Địa chỉ Ví | Tier | Active Days | TX Count | Deploy Count | 🌟 Tổng Điểm |\n"
        md_content += "|---|---|---|---|---|---|---|\n"
        
        for idx, r in enumerate(results, 1):
            addr = r['address']
            short_addr = f"{addr[:6]}...{addr[-4:]}"
            md_content += f"| {idx} | `{short_addr}` | {r['tier']} | {r['active_days']} | {r['tx_count']} | {r['deploy_count']} | **{r['total_score']}** |\n"
            
        # Ghi ra file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
            
        print(f"✅ Đã tạo báo cáo thành công tại: {output_path}")

if __name__ == "__main__":
    engine = AirdropScoringEngine()
    base_dir = Path(__file__).resolve().parent.parent.parent
    report_path = base_dir / "docs" / "status_report_scoring.md"
    engine.generate_markdown_report(str(report_path))
