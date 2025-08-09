# ================================
# File chính để chạy ứng dụng
# ================================
import time
import schedule
from config import PRODUCTS, CRON_INTERVAL_MIN
from db import init_db, save_price
from scraper.parser import get_price

def check_prices():
    """Duyệt qua PRODUCTS, lấy giá từng URL và lưu DB."""
    for product, urls in PRODUCTS.items():
        for url in urls:
            price = get_price(url)
            if price:
                print(f"[OK] {product} | {url} -> {price}")
                save_price(product, url, price)
            else:
                print(f"[MISS] {product} | {url}")

def main():
    init_db()                 # Tạo bảng nếu chưa có
    check_prices()            # Quét 1 lần ngay khi khởi động
    schedule.every(CRON_INTERVAL_MIN).minutes.do(check_prices)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
