# -*- coding: utf-8 -*-
"""
Parser: lấy giá sản phẩm từ URL.
- Ưu tiên selector truyền vào (nếu có)
- Nếu SELECTOR_BY_DOMAIN có selector khác rỗng -> dùng
- Nếu cache đã học có selector -> dùng
- Nếu chưa có -> tự học bằng auto_selector.find_best, lưu vào cache
"""

import os
import json
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup

from price_checker.config import (
    HEADERS,
    SELECTOR_BY_DOMAIN,
    AUTO_LEARN_SELECTORS,
    MIN_SELECTOR_SCORE,
    SELECTOR_CACHE_PATH,
)
from price_checker.auto_selector import find_best


# ---------- Cache selector đã học ----------
def _load_cache():
    if os.path.exists(SELECTOR_CACHE_PATH):
        try:
            with open(SELECTOR_CACHE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def _save_cache(cache: dict):
    try:
        with open(SELECTOR_CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


_SELECTOR_CACHE = _load_cache()  # {domain: "css selector"}


# ---------- Headers theo domain (giảm 403) ----------
def _headers_for(domain: str) -> dict:
    h = dict(HEADERS)  # copy
    h.setdefault(
        "Accept",
        "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    )
    h.setdefault("Accept-Language", "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7")
    h.setdefault("Connection", "keep-alive")
    h.setdefault("Referer", f"https://{domain}/")
    return h


# ---------- Lấy selector tốt nhất cho 1 domain ----------
def _get_selector(domain: str, html: str, preferred: str | None):
    # 1) Ưu tiên selector truyền vào
    if preferred:
        return preferred, "provided"

    # 2) Nếu config có selector và KHÔNG rỗng -> dùng
    if domain in SELECTOR_BY_DOMAIN:
        sel = (SELECTOR_BY_DOMAIN or {}).get(domain)  # có thể rỗng
        if sel:
            return sel, "config"

    # 3) Nếu cache có -> dùng
    if domain in _SELECTOR_CACHE:
        return _SELECTOR_CACHE[domain], "cache"

    # 4) Tự học từ HTML
    if AUTO_LEARN_SELECTORS:
        best = find_best(html, topk=1)
        if best:
            score, sel, sample = best[0]
            if score >= MIN_SELECTOR_SCORE:
                _SELECTOR_CACHE[domain] = sel
                _save_cache(_SELECTOR_CACHE)
                print(
                    f"[LEARN] {domain}: selector='{sel}' score={score} sample='{sample}'"
                )
                return sel, "auto"

    return None, "none"


# ---------- API chính: lấy giá ----------
def get_price(url: str, selector: str | None = None) -> str | None:
    domain = urlparse(url).netloc.replace("www.", "")

    # Gửi request
    try:
        res = requests.get(url, headers=_headers_for(domain), timeout=20)
        res.raise_for_status()
    except requests.RequestException as e:
        print(f"[ERROR] Request failed: {e} | {url}")
        return None

    # Tìm selector khả dụng
    sel, source = _get_selector(domain, res.text, selector)
    if not sel:
        print(f"[WARN] No selector available for domain {domain}")
        return None

    # Parse và lấy giá
    soup = BeautifulSoup(res.text, "html.parser")
    tag = soup.select_one(sel)
    if not tag:
        print(f"[WARN] Selector not found: {sel} | {url} (source={source})")
        return None

    price_text = tag.get_text(strip=True)
    print(f"[OK] {domain} ({source}) -> '{price_text}' via '{sel}'")
    return price_text
