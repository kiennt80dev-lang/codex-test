# ================================
# Quản lý database SQLite
# ================================
import sqlite3
from datetime import datetime
from price_checker.config import DB_PATH

# Tạo bảng lưu giá nếu chưa có
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS prices(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product   TEXT,  -- Tên sản phẩm
            url       TEXT,  -- Link web đối thủ
            price     TEXT,  -- Giá lấy được (giữ nguyên định dạng chuỗi)
            fetched_at TEXT  -- Thời điểm lấy giá (ISO)
        )
    """)
    conn.commit()
    conn.close()

# Lưu một bản ghi giá
def save_price(product, url, price):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO prices(product, url, price, fetched_at) VALUES (?, ?, ?, ?)",
        (product, url, price, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()
