# ================================
# File cấu hình cho ứng dụng
# ================================

# Danh sách sản phẩm & các link cần kiểm tra giá (THAY URL THẬT)
PRODUCTS = {
    "iphone_14": [
        "https://example.com/product/iphone-14",
        "https://another-shop.com/iphone-14",
    ],
    "ipad_air": [
        "https://example.com/product/ipad-air",
    ],
}

# CSS selector để tìm thẻ chứa giá dựa theo tên miền
# Ví dụ: "span.price" nghĩa là <span class="price">...</span>
SELECTOR_BY_DOMAIN = {
    "example.com": "span.price",
    "another-shop.com": "div#product-price",
}

# Header giả lập trình duyệt khi gửi request
HEADERS = {"User-Agent": "Mozilla/5.0"}

# Thời gian giữa các lần quét giá (phút)
CRON_INTERVAL_MIN = 60

# Đường dẫn lưu file database SQLite (tạo ngay trong thư mục chạy)
DB_PATH = "prices.db"
