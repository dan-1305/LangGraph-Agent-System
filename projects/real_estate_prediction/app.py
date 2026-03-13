from pathlib import Path
from flask import Flask, request, render_template, jsonify
from flask.wrappers import Response
import joblib
import pandas as pd
import folium
from typing import Any

app = Flask(__name__)

import sqlite3

# Cấu hình đường dẫn bằng pathlib
BASE_DIR = Path(__file__).resolve().parent
MODEL_HIGH_END_PATH = BASE_DIR / "models" / "model_high_end.pkl"
MODEL_MASS_PATH = BASE_DIR / "models" / "model_mass_market.pkl"
DB_PATH = BASE_DIR.parent.parent / "data" / "real_estate.db"

# Load mô hình đa phân khúc
try:
    model_high_end = joblib.load(MODEL_HIGH_END_PATH)
    model_mass_market = joblib.load(MODEL_MASS_PATH)
except Exception as e:
    print(f"Lỗi tải mô hình: {e}")
    model_high_end = None
    model_mass_market = None

# Load raw_data từ SQLite để lấy unique dropdown
try:
    conn = sqlite3.connect(DB_PATH)
    df_raw = pd.read_sql_query("SELECT Province, District FROM Properties", conn)
    conn.close()
    provinces = sorted(df_raw['Province'].dropna().unique().tolist())
    districts = sorted(df_raw['District'].dropna().unique().tolist())
except Exception as e:
    print(f"Lỗi tải Database: {e}")
    provinces = []
    districts = []

@app.route('/')
def home() -> str:
    """
    Render trang chủ với các dropdown động lấy từ data.
    """
    return render_template('index.html', provinces=provinces, districts=districts)

@app.route('/map')
def show_map() -> str:
    """
    Render bản đồ Heatmap giá nhà theo Quận/Huyện.
    """
    try:
        # Load lại data từ Database
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT Price_VND, Area_m2, District FROM Properties", conn)
        conn.close()
        
        df = df.dropna(subset=['Price_VND', 'Area_m2', 'District'])
        df = df[df['Area_m2'] > 10]
        df['Price_per_m2'] = df['Price_VND'] / df['Area_m2']
        
        # Lọc outlier nhanh
        df = df[(df['Price_per_m2'] >= 1_000_000) & (df['Price_per_m2'] <= 500_000_000)]
        
        # Tính giá trung bình theo quận
        district_prices = df.groupby('District')['Price_per_m2'].mean().reset_index()
        
        # Khởi tạo bản đồ lấy tâm là TP.HCM (Tọa độ: 10.762622, 106.660172)
        m = folium.Map(location=[10.762622, 106.660172], zoom_start=11)
        
        # Tọa độ giả định cho một số quận phổ biến (Vì raw data không có Lat/Lon)
        # Trong thực tế cần dùng thư viện geopy để geocode, ở đây dùng mock tọa độ cho bản demo
        district_coords = {
            'Quận 1': [10.7756, 106.7019],
            'Quận 3': [10.7843, 106.6816],
            'Quận 10': [10.7743, 106.6675],
            'Quận Tân Bình': [10.8015, 106.6526],
            'Quận Phú Nhuận': [10.7997, 106.6803],
            'Quận Gò Vấp': [10.8386, 106.6653],
            'Quận Bình Thạnh': [10.8105, 106.6961],
            'Thành phố Thủ Đức': [10.8494, 106.7537],
            'Quận 7': [10.8106, 106.7093],
            'Quận 4': [10.7355, 106.7218],
            'Quận 2': [10.7388, 106.7345],
            'Quận 9': [10.7857, 106.8267],
            'Quận 5': [10.7583, 106.6738],
            'Quận 6': [10.7483, 106.6347],
            'Quận 8': [10.7357, 106.6212],
            'Quận 11': [10.7226, 106.6394],
            'Quận 12': [10.8037, 106.6601],
            'Quận Tân Phú': [10.7937, 106.6216],
            'Quận Bình Tân': [10.7865, 106.6121],
            'Huyện Bình Chánh': [10.7511, 106.5684],
            'Huyện Hóc Môn': [10.8656, 106.5772],
            'Huyện Củ Chi': [10.9329, 106.5318],
            'Huyện Nhà Bè': [10.6384, 106.7289],
            'Thành phố Biên Hòa': [10.9575, 106.8427],
            'Huyện Long Thành': [10.6865, 106.9458],
            'Huyện Nhơn Trạch': [10.7283, 106.8992],
            'Thành phố Dĩ An': [10.9419, 106.7876],
            'Thành phố Thuận An': [10.9102, 106.7118]
        }
        
        for index, row in district_prices.iterrows():
            district = row['District']
            price = row['Price_per_m2']
            
            if district in district_coords:
                coord = district_coords[district]
                # Chọn màu dựa trên giá (Giá cao -> Đỏ, Giá thấp -> Xanh)
                color = 'red' if price > 150_000_000 else ('orange' if price > 80_000_000 else 'green')
                
                folium.CircleMarker(
                    location=coord,
                    radius=15,
                    popup=f"{district}: {price:,.0f} VNĐ/m2",
                    tooltip=f"{district} (Click để xem giá)",
                    color=color,
                    fill=True,
                    fill_color=color
                ).add_to(m)
                
        # Trả về HTML của bản đồ
        return m.get_root().render()
    except Exception as e:
        return f"Lỗi tạo bản đồ: {str(e)}"

@app.route('/predict', methods=['POST'])
def predict() -> Response:
    """
    API endpoint xử lý dự báo giá nhà.
    """
    if not model_high_end or not model_mass_market:
        return jsonify({'error': 'Chưa load được mô hình dự báo đa phân khúc!'})
    
    try:
        area = float(request.form.get('area', 0))
        district = request.form.get('district', '')
        province = request.form.get('province', '')
        property_type = request.form.get('property_type', 'House')
        num_floors = float(request.form.get('num_floors', 0))
        width_m = float(request.form.get('width_m', 0))
        alley_width_m = float(request.form.get('alley_width_m', 0))
        
        is_frontage = int(request.form.get('is_frontage', 0))
        is_alley = int(request.form.get('is_alley', 0))
        has_furniture = int(request.form.get('has_furniture', 0))
        is_so_hong = int(request.form.get('is_so_hong', 0))

        # Model pipeline takes care of OneHotEncoding, we just need to provide a DataFrame 
        # with the exact column names used during training:
        # ['Area_m2', 'District', 'Province', 'is_frontage', 'is_alley', 'has_furniture', 
        # 'num_floors', 'width_m', 'alley_width_m', 'Property_Type', 'is_so_hong']
        
        input_data = {
            'Area_m2': [area],
            'District': [district],
            'Province': [province],
            'is_frontage': [is_frontage],
            'is_alley': [is_alley],
            'has_furniture': [has_furniture],
            'num_floors': [num_floors],
            'width_m': [width_m],
            'alley_width_m': [alley_width_m],
            'Property_Type': [property_type],
            'is_so_hong': [is_so_hong]
        }
        
        df_input = pd.DataFrame(input_data)
        
        # LOGIC PHÂN CỤM TỰ ĐỘNG LÚC DỰ BÁO (Proxy Segmentation)
        high_end_districts = ['Quận 1', 'Quận 3', 'Quận 10', 'Quận Phú Nhuận', 'Quận Tân Bình']
        is_high_end = (district in high_end_districts) or (property_type == 'Villa') or (is_frontage == 1)
        
        selected_model = model_high_end if is_high_end else model_mass_market
        segment_name = "Cao Cấp (High-End)" if is_high_end else "Phổ Thông (Mass-Market)"
        
        # Dự báo (Note: model trả về giá trị Log, cần dùng expm1 để chuyển về giá thực)
        import numpy as np
        prediction_log = selected_model.predict(df_input)[0]
        prediction = np.expm1(prediction_log)
        
        return jsonify({
            'success': True,
            'prediction': f"{prediction:,.2f} VNĐ",
            'segment': segment_name
        })
        
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
