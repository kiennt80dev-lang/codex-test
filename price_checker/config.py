# ================================
# File cấu hình cho ứng dụng
# ================================

# Danh sách sản phẩm & các link cần kiểm tra giá (THAY URL THẬT)
PRODUCTS = {
    "B13UDXK-2410VN": [
        "https://www.anphatpc.com.vn/laptop-msi-katana-15-b13udxk-2410vn.html",
        "https://fptshop.com.vn/may-tinh-xach-tay/msi-gaming-katana-15-b13udxk-2410vn-i5-13420h",
    ],
    
}

# CSS selector để tìm thẻ chứa giá dựa theo tên miền
# Ví dụ: "span.price" nghĩa là <span class="price">...</span>
SELECTOR_BY_DOMAIN = {
    "anphatpc.com.vn": "",
    "fptshop.com.vn": "",
}

# Header giả lập trình duyệt khi gửi request
HEADERS = {"User-Agent": "Mozilla/5.0"}

# Thời gian giữa các lần quét giá (phút)
CRON_INTERVAL_MIN = 60

# Đường dẫn lưu file database SQLite (tạo ngay trong thư mục chạy)
DB_PATH = "prices.db"
# Tự học selector nếu chưa có trong SELECTOR_BY_DOMAIN
AUTO_LEARN_SELECTORS = True
MIN_SELECTOR_SCORE = 7         # ngưỡng chấm điểm tối thiểu để chấp nhận
SELECTOR_CACHE_PATH = "selectors_cache.json"  # nơi lưu cache selector đã học
