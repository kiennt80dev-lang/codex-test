# -*- coding: utf-8 -*-
import json, os, requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from config import (
    HEADERS, SELECTOR_BY_DOMAIN, AUTO_LEARN_SELECTORS,
    MIN_SELECTOR_SCORE, SELECTOR_CACHE_PATH
)
from price_checker.auto_selector import find_best


# tải/lưu cache selector đã học
def _load_cache():
    if os.path.exists(SELECTOR_CACHE_PATH):
        try:
            with open(SELECTOR_CACHE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def _save_cache(cache):
    try:
        with open(SELECTOR_CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

_SELECTOR_CACHE = _load_cache()  # {domain: selector}

def _get_selector(domain, html, preferred=None):
    # 1) ưu tiên selector truyền vào
    if preferred: 
        return preferred, "provided"
    # 2) có trong config
    if domain in SELECTOR_BY_DOMAIN: 
        return SELECTOR_BY_DOMAIN[domain], "config"
    # 3) có trong cache đã học
    if domain in _SELECTOR_CACHE:
        return _SELECTOR_CACHE[domain], "cache"
    # 4) tự đoán từ HTML
    if AUTO_LEARN_SELECTORS:
        best = find_best(html, topk=1)
        if best:
            score, sel, sample = best[0]
            if score >= MIN_SELECTOR_SCORE:
                _SELECTOR_CACHE[domain] = sel
                _save_cache(_SELECTOR_CACHE)
                print(f"[LEARN] Learned selector for {domain}: {sel} (score={score}) sample='{sample}'")
                return sel, "auto"
    return None, "none"

def get_price(url, selector=None):
    try:
        res = requests.get(url, headers=HEADERS, timeout=20)
        res.raise_for_status()
    except requests.RequestException as e:
        print(f"[ERROR] Request failed: {e} | {url}")
        return None

    domain = urlparse(url).netloc.replace("www.", "")
    sel, source = _get_selector(domain, res.text, selector)

    if not sel:
        print(f"[WARN] No selector available for domain {domain}")
        return None

    soup = BeautifulSoup(res.text, "html.parser")
    tag = soup.select_one(sel)
    if not tag:
        print(f"[WARN] Selector not found: {sel} | {url} (source={source})")
        return None

    price_text = tag.get_text(strip=True)
    print(f"[OK] {domain} ({source}) -> '{price_text}' via '{sel}'")
    return price_text
