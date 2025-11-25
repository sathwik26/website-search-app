# backend/utils/parser.py

import requests
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
import nltk
from urllib.parse import urlparse

# Ensure punkt is available
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

MAX_TOKENS = 300     
BLOCK_TAGS = ["section", "article", "div", "main", "p", "li"]

def fetch_html(url: str) -> str:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": url,
    }
    res = requests.get(url, headers=headers, timeout=20)
    res.raise_for_status()  
    return res.text

def html_to_chunks(url: str):
    html = fetch_html(url)
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript", "footer", "svg", "img"]):
        tag.decompose()

    chunks = []
    parsed = urlparse(url)
    path = parsed.path or "/"
    idx = 0

    for el in soup.find_all(BLOCK_TAGS):
        text = el.get_text(separator=" ", strip=True)
        if len(text) < 30: 
            continue

        tokens = word_tokenize(text)
        if len(tokens) > MAX_TOKENS:
            tokens = tokens[:MAX_TOKENS]
            text = " ".join(tokens)

        chunks.append({
            "id": f"{path}-{idx}",
            "title": " ".join(tokens[:8]) + "...",
            "path": path,
            "html": str(el),
            "text": text
        })
        idx += 1

    return chunks
