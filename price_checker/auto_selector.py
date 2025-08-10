# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup

CURRENCY_PAT = re.compile(r'(₫|VNĐ|VND|đ|\$|USD|EUR|€)', re.I)
PRICE_WORD_PAT = re.compile(r'(price|gia|giá)', re.I)

def _text(s): 
    return re.sub(r'\s+', ' ', (s or '')).strip()

def _build_selector(el):
    parts = []
    node = el
    while node and getattr(node, "name", None) and node.name != "[document]":
        seg = node.name
        if node.get("id"):
            seg += f"#{node['id']}"
            parts.insert(0, seg)
            break
        cls = node.get("class", [])
        if cls:
            seg += "." + ".".join(cls[:2])  # tối đa 2 class để gọn
        if node.parent:
            same = [sib for sib in node.parent.find_all(node.name, recursive=False)]
            if len(same) > 1:
                seg += f":nth-of-type({same.index(node)+1})"
        parts.insert(0, seg)
        node = node.parent
    if len(parts) > 4:
        parts = parts[-4:]  # rút gọn 4 cấp cuối
    return " > ".join(parts)

def _score(el):
    score = 0
    txt = _text(el.get_text(" "))
    # tín hiệu từ text
    if CURRENCY_PAT.search(txt): score += 5
    if re.search(r'\b\d{1,3}([.,]\d{3})+(\s*(₫|VNĐ|VND|đ))?\b', txt): score += 4
    # tín hiệu từ attr
    attrs = " ".join(f"{k}={v}" for k, v in el.attrs.items() if isinstance(v, (str, list)))
    if PRICE_WORD_PAT.search(attrs): score += 4
    if el.has_attr("data-price") or el.get("itemprop") == "price": score += 6
    for k in ("class","id"):
        v = el.get(k); 
        if isinstance(v, list): v = " ".join(v)
        if isinstance(v, str) and PRICE_WORD_PAT.search(v): score += 3
    if len(txt) > 60: score -= 3  # phạt nếu quá dài
    score += {"b":2,"span":2,"strong":2,"div":1}.get(el.name,0)
    return score, txt

def find_best(html, topk=1):
    soup = BeautifulSoup(html, "html.parser")
    cands = []
    for el in soup.find_all(["span","b","strong","div","p","meta"]):
        sc, txt = _score(el)
        if sc > 0 and _text(txt):
            sel = _build_selector(el)
            cands.append((sc, sel, _text(txt)))
    # lấy selector tốt nhất
    cands.sort(key=lambda x: x[0], reverse=True)
    return cands[:topk] if cands else []

