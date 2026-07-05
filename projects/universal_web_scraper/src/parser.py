import os
import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path

def parse_hacker_news(html_path: str, output_csv: str) -> None:
    """
    Parse Hacker News HTML and extract title, href, score, and comments.
    
    Args:
        html_path (str): Path to the raw HTML file.
        output_csv (str): Path to save the resulting CSV.
    """
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
            
        soup = BeautifulSoup(html_content, 'html.parser')
        story_rows = soup.find_all('tr', class_='athing')
        
        data = []
        for row in story_rows:
            # Lấy Title và Href
            title_element = row.find('span', class_='titleline')
            if not title_element:
                continue
                
            link_element = title_element.find('a')
            if not link_element:
                continue
                
            title = link_element.text.strip()
            href = link_element.get('href', '').strip()
            
            # Lấy Score và Comments từ dòng tiếp theo
            score = '0 points'
            comments = '0 comments'
            
            next_row = row.find_next_sibling('tr')
            if next_row:
                subtext = next_row.find('td', class_='subtext')
                if subtext:
                    # Lấy score
                    score_element = subtext.find('span', class_='score')
                    if score_element:
                        score = score_element.text.strip()
                        
                    # Lấy comments
                    comment_links = subtext.find_all('a')
                    for a in comment_links:
                        if 'comment' in a.text:
                            comments = a.text.strip()
                            break
                            
            data.append({
                'Title': title,
                'Href': href,
                'Score': score,
                'Comments': comments
            })
            
        # Lưu ra CSV
        df = pd.DataFrame(data)
        os.makedirs(os.path.dirname(output_csv), exist_ok=True)
        df.to_csv(output_csv, index=False, encoding='utf-8')
        
        print("✅ Thành công! Đã parse được {} bài viết.".format(len(df)))
        print("--- 5 DÒNG ĐẦU TIÊN ---")
        print(df.head(5).to_string())
        
    except Exception as e:
        print(f"Lỗi khi parse HTML: {e}")

if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent
    html_file = base_dir / "data" / "raw" / "full_page.html"
    csv_file = base_dir / "data" / "output" / "hn_results.csv"
    
    parse_hacker_news(str(html_file), str(csv_file))
