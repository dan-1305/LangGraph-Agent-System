import os
import pandas as pd
from pathlib import Path

def clean_and_rank_data(input_csv: str, output_csv: str) -> None:
    """
    Làm sạch dữ liệu Hacker News, tính Engagement_Score và lưu kết quả.
    
    Args:
        input_csv (str): Đường dẫn tới file CSV thô (hn_results.csv).
        output_csv (str): Đường dẫn lưu file CSV đã làm sạch (hn_cleaned.csv).
    """
    try:
        # 1. Đọc dữ liệu
        df = pd.read_csv(input_csv)
        
        # 2. Làm sạch bằng Regex (Chỉ lấy số)
        df['Score'] = df['Score'].str.extract(r'(\d+)').astype(float).fillna(0)
        df['Comments'] = df['Comments'].str.extract(r'(\d+)').astype(float).fillna(0)
        
        # 3. Tính Engagement Metric
        df['Engagement_Score'] = df['Score'] + (df['Comments'] * 2)
        
        # 4. Sắp xếp giảm dần
        df_cleaned = df.sort_values(by='Engagement_Score', ascending=False).reset_index(drop=True)
        
        # 5. Lưu ra file CSV
        os.makedirs(os.path.dirname(output_csv), exist_ok=True)
        df_cleaned.to_csv(output_csv, index=False, encoding='utf-8')
        
        # 6. In ra Top 3 bài viết Hot nhất
        print("✅ Đã làm sạch và xếp hạng dữ liệu thành công!")
        print(f"✅ Dữ liệu đã lưu tại: {output_csv}\n")
        print("🏆 TOP 3 BÀI VIẾT HOT NHẤT HACKER NEWS 🏆")
        print("-" * 50)
        
        top_3 = df_cleaned.head(3)
        for index, row in top_3.iterrows():
            print(f"Top {index + 1}: {row['Title']}")
            print(f"   => Engagement Score: {row['Engagement_Score']} (Score: {row['Score']}, Comments: {row['Comments']})")
            print("-" * 50)
            
    except Exception as e:
        print(f"[-] Lỗi trong quá trình làm sạch dữ liệu: {e}")

if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent
    input_file = base_dir / "data" / "output" / "hn_results.csv"
    output_file = base_dir / "data" / "output" / "hn_cleaned.csv"
    
    clean_and_rank_data(str(input_file), str(output_file))
