from typing import List, Dict, Any

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
