import sqlite3
import json
from pathlib import Path
from datetime import datetime

base_dir = Path(__file__).resolve().parent.parent.parent
db_path = base_dir / "data" / "airdrop_guerrilla.db"
json_path = base_dir / "data" / "wallets" / "secure_wallets.json"

def init_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Bảng wallets
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wallets (
            address TEXT PRIMARY KEY,
            name TEXT,
            proxy TEXT,
            user_agent TEXT,
            encrypted_private_key TEXT,
            encrypted_twitter_token TEXT,
            encrypted_discord_token TEXT,
            status TEXT
        )
    ''')
    
    # Bảng activity_log
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wallet_address TEXT,
            project_name TEXT,
            step_name TEXT,
            status TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(wallet_address) REFERENCES wallets(address)
        )
    ''')
    
    conn.commit()
    return conn

def migrate_data(conn):
    if not json_path.exists():
        print("Không tìm thấy file secure_wallets.json để migrate.")
        return
        
    with open(json_path, 'r', encoding='utf-8') as f:
        wallets = json.load(f)
        
    cursor = conn.cursor()
    count = 0
    for address, data in wallets.items():
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO wallets 
                (address, name, proxy, user_agent, encrypted_private_key, encrypted_twitter_token, encrypted_discord_token, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                address,
                data.get("name", ""),
                data.get("proxy", ""),
                data.get("user_agent", ""),
                data.get("encrypted_private_key", ""),
                data.get("encrypted_twitter_token", ""),
                data.get("encrypted_discord_token", ""),
                data.get("status", "Active")
            ))
            count += 1
        except Exception as e:
            print(f"Lỗi khi migrate ví {address}: {e}")
            
    conn.commit()
    print(f"✅ Đã di cư thành công {count} ví sang SQLite database.")

if __name__ == "__main__":
    print("Khởi tạo SQLite Database...")
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = init_db()
    print("Bắt đầu Migration...")
    migrate_data(conn)
    conn.close()
    
    # Xóa file JSON để bảo mật
    if json_path.exists():
        json_path.unlink()
        print("🗑️ Đã xóa file secure_wallets.json (Dọn dẹp bảo mật).")
