import os
import os
import re
import pandas as pd
import numpy as np
from pathlib import Path
import joblib
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, r2_score

import sqlite3

# 1. Setup paths
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR.parent.parent / "data" / "real_estate.db"
MODEL_PATH = BASE_DIR / "models" / "model.pkl"

def main():
    print("Starting execution...")
    # 2. Load data from SQLite
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM Properties", conn)
    conn.close()
    
    # Drop duplicates and NAs
    df = df.drop_duplicates()
    df = df.dropna(subset=['Price_VND', 'Area_m2', 'District', 'Province'])
    
    # Clean Outliers in Area (basic thresholds)
    df = df[(df['Area_m2'] > 10) & (df['Area_m2'] < 1000)]
    
    # Tạo biến Price_per_m2
    df['Price_per_m2'] = df['Price_VND'] / df['Area_m2']
    
    # Hard Threshold cho Đơn giá (1 Triệu - 300 Triệu VNĐ/m2)
    df = df[(df['Price_per_m2'] >= 1_000_000) & (df['Price_per_m2'] <= 300_000_000)]
    
    # Clean Outliers by District using Z-Score Filtering trên Đơn giá (Price_per_m2)
    counts = df.groupby('District')['Price_per_m2'].transform('count')
    means = df.groupby('District')['Price_per_m2'].transform('mean')
    stds = df.groupby('District')['Price_per_m2'].transform('std')
    
    z_scores = np.abs((df['Price_per_m2'] - means) / stds)
    # Keep rows where count <= 5 or z_score <= 3 (also keep if std is NaN)
    df = df[(counts <= 5) | (z_scores <= 3) | z_scores.isna()]
    
    # FEATURE ENGINEERING (Extract from Title)
    # Regex xử lý mặt tiền / hẻm cải tiến
    df['is_frontage'] = df['Title'].str.contains(r'\b(?:mặt tiền|mt|mặt đường|phố)\b', case=False, na=False).astype(int)
    df['is_alley'] = df['Title'].str.contains(r'\b(?:hẻm|ngõ|hxh|hx h|hẻm xe hơi)\b', case=False, na=False).astype(int)
    df['has_furniture'] = df['Title'].str.contains(r'nội thất|đầy đủ đồ|full đồ|cao cấp', case=False, na=False).astype(int)
    
    # Regex số lầu cải tiến: Bắt cả "1t2l" (1 trệt 2 lầu -> lấy 2 lầu), hoặc "\d+ lầu"
    # Logic: Tìm "(số)l" hoặc "(số) lầu/tầng/tấm"
    df['num_floors'] = df['Title'].str.extract(r'(\d+)\s*(?:lầu|tầng|tấm|l\b)', flags=re.IGNORECASE)[0].astype(float).fillna(0)
    
    # Bổ sung trích xuất quận (q1, q.tb) từ Title nếu bị thiếu trong District
    # Dù ở đây District đã có, nhưng hàm này giúp enrich thêm nếu cần
    
    # Trích xuất bề ngang (width_m)
    df['width_m'] = df['Title'].str.extract(r'(?:ngang|mt|mặt tiền)\s*(\d+[.,]?\d*)\s*m?', flags=re.IGNORECASE)[0].str.replace(',', '.').astype(float).fillna(0)
    
    # Trích xuất độ rộng hẻm (alley_width_m)
    df['alley_width_m'] = df['Title'].str.extract(r'(?:hẻm|ngõ|hxh|hx h).*?(\d+[.,]?\d*)\s*m', flags=re.IGNORECASE)[0].str.replace(',', '.').astype(float).fillna(0)
    
    # Trích xuất Loại hình BĐS (Property_Type)
    def get_property_type(title):
        title = str(title).lower()
        if 'đất' in title or 'nền' in title or 'sào' in title:
            return 'Land'
        elif 'biệt thự' in title or 'villa' in title:
            return 'Villa'
        elif 'căn hộ' in title or 'chung cư' in title:
            return 'Apartment'
        elif 'kho' in title or 'xưởng' in title:
            return 'Warehouse'
        else:
            return 'House'
            
    df['Property_Type'] = df['Title'].apply(get_property_type)
    
    # Trích xuất Pháp lý (is_so_hong)
    df['is_so_hong'] = df['Title'].str.contains(r'sổ hồng|shr|sổ riêng|sổ đỏ', case=False, na=False).astype(int)
    
    print(f"Data shape after filtering & feature engineering: {df.shape}")
    
    # LOGIC PHÂN ĐOẠN (SEGMENTATION LOGIC)
    # Phân cụm dữ liệu thành 2 phân khúc: Cao cấp (High_End) và Phổ thông (Mass_Market)
    # Phân khúc Cao cấp: Nhà Mặt tiền, Biệt thự hoặc ở Quận trung tâm
    high_end_districts = ['Quận 1', 'Quận 3', 'Quận 10', 'Quận Phú Nhuận', 'Quận Tân Bình']
    is_high_end_location = df['District'].isin(high_end_districts)
    is_high_end_type = (df['Property_Type'] == 'Villa') | (df['is_frontage'] == 1)
    
    df['Segment'] = np.where(is_high_end_location | is_high_end_type, 'High_End', 'Mass_Market')
    
    print(f"Phân mảnh dữ liệu:")
    print(df['Segment'].value_counts())
    
    # 3. Features and Preprocessing
    features = ['Area_m2', 'District', 'Province', 'is_frontage', 'is_alley', 'has_furniture', 'num_floors', 'width_m', 'alley_width_m', 'Property_Type', 'is_so_hong']
    
    numeric_features = ['Area_m2', 'num_floors', 'width_m', 'alley_width_m']
    categorical_features = ['District', 'Province', 'is_frontage', 'is_alley', 'has_furniture', 'Property_Type', 'is_so_hong']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features)
        ])
    
    # Huấn luyện 2 mô hình riêng biệt cho 2 phân khúc
    segments = ['High_End', 'Mass_Market']
    
    for seg in segments:
        print(f"\n--- Đang huấn luyện cho phân khúc: {seg} ---")
        df_seg = df[df['Segment'] == seg]
        
        X = df_seg[features]
        y = df_seg['Price_VND']
        y_log = np.log1p(y)
        
        X_train, X_test, y_train_log, y_test_log = train_test_split(X, y_log, test_size=0.2, random_state=42)
        
        model = XGBRegressor(random_state=42, n_jobs=1)
        
        pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                                   ('model', model)])
        
        param_distributions = {
            'model__n_estimators': [100, 200, 300],
            'model__max_depth': [3, 4, 5],
            'model__learning_rate': [0.01, 0.05, 0.1],
            'model__subsample': [0.7, 0.8, 0.9],
            'model__colsample_bytree': [0.7, 0.8, 0.9],
            'model__reg_alpha': [0, 1.0, 2.0],
            'model__reg_lambda': [0, 1.0, 2.0],
            'model__min_child_weight': [1, 3, 5]
        }
        
        search = RandomizedSearchCV(
            pipeline, 
            param_distributions=param_distributions, 
            n_iter=5, # Giữ số lần lặp nhỏ để CPU không bị quá tải
            cv=3, 
            scoring='r2', 
            n_jobs=1, 
            random_state=42,
            verbose=1
        )
        
        print(f"Đang tìm tham số tối ưu (Hyperparameter Tuning)...")
        search.fit(X_train, y_train_log)
        
        best_pipeline = search.best_estimator_
        print(f"Best params: {search.best_params_}")
        
        y_pred_train_log = best_pipeline.predict(X_train)
        y_pred_test_log = best_pipeline.predict(X_test)
        
        y_train_real = np.expm1(y_train_log)
        y_test_real = np.expm1(y_test_log)
        y_pred_train_real = np.expm1(y_pred_train_log)
        y_pred_test_real = np.expm1(y_pred_test_log)
        
        r2_train = r2_score(y_train_real, y_pred_train_real)
        r2_test = r2_score(y_test_real, y_pred_test_real)
        mae_test = mean_absolute_error(y_test_real, y_pred_test_real)
        
        print(f"Metrics ({seg}):")
        print(f"R^2 Train: {r2_train:.4f}")
        print(f"R^2 Test: {r2_test:.4f}")
        print(f"MAE Test: {mae_test:,.0f} VND")
        
        # 7. Save models separately
        MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
        seg_model_path = BASE_DIR / "models" / f"model_{seg.lower()}.pkl"
        joblib.dump(best_pipeline, seg_model_path)
        print(f"Model saved to {seg_model_path}")

if __name__ == "__main__":
    main()
