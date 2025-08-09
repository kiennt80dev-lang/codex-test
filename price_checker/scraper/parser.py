# ================================
# Lấy giá sản phẩm từ website
# ================================
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from config import HEADERS, SELECTOR_BY_DOMAIN

def get_price(url, selector=None):
    """Trả về chuỗi giá lấy được từ URL, hoặc None nếu không tìm thấy."""
    try:
        res = requests.get(url, headers=HEADERS, timeout=15)
        res.raise_for_status()
    except requests.RequestException as e:
        print(f"[ERROR] Request failed: {e} | {url}")
        return None

    soup = BeautifulSoup(res.text, "html.parser")

    # Nếu chưa truyền selector, xác định theo domain
    if not selector:
        domain = urlparse(url).netloc.replace("www.", "")
        selector = SELECTOR_BY_DOMAIN.get(domain)

    if not selector:
        print(f"[WARN] No selector configured for: {url}")
        return None

    tag = soup.select_one(selector)
    if not tag:
        print(f"[WARN] Selector not found: {selector} | {url}")
        return None

    return tag.get_text(strip=True)
