import time, re, requests
from bs4 import BeautifulSoup

STEEL_SYMBOLS = ["MUGHAL", "ISL", "ASTL", "AGHA", "ITTEFAQ"]

FALLBACK = {
    "MUGHAL": 88.00,
    "ISL": 92.00,
    "ASTL": 24.00,
    "AGHA": 14.00,
    "ITTEFAQ": 6.00,
}

def _num(x):
    try:
        return float(re.sub(r"[^\d.\-]", "", str(x)))
    except Exception:
        return None

def fetch_company(symbol):
    symbol = symbol.upper().strip()
    url = f"https://dps.psx.com.pk/company/{symbol}"
    headers = {"User-Agent": "Mozilla/5.0 SHMRY/2.0"}

    try:
        r = requests.get(url, headers=headers, timeout=8)
        soup = BeautifulSoup(r.text, "html.parser")
        text = soup.get_text(" ", strip=True)

        nums = [_num(x) for x in re.findall(r"\b\d{1,4}(?:,\d{3})*(?:\.\d+)?\b", text)]
        nums = [x for x in nums if x is not None]

        price = None
        for label in ["Current", "PRICE", "Rate", "LDCP"]:
            m = re.search(label + r"\s*[:\-]?\s*([0-9,.]+)", text, re.I)
            if m:
                price = _num(m.group(1))
                break

        if not price or price <= 0:
            plausible = [x for x in nums if 1 <= x <= 1000]
            price = plausible[0] if plausible else FALLBACK.get(symbol)

        change = None
        m = re.search(r"CHANGE\s*[:\-]?\s*([+\-]?[0-9,.]+)", text, re.I)
        if m:
            change = _num(m.group(1))

        volume = None
        m = re.search(r"VOLUME\s*[:\-]?\s*([0-9,]+)", text, re.I)
        if m:
            volume = _num(m.group(1))

        return {
            "symbol": symbol,
            "price": price,
            "change": change,
            "volume": volume,
            "source": url,
            "status": "live_or_fallback_parsed",
            "timestamp": int(time.time())
        }
    except Exception as e:
        return {
            "symbol": symbol,
            "price": FALLBACK.get(symbol),
            "change": None,
            "volume": None,
            "source": "fallback",
            "status": "fallback_error",
            "error": str(e),
            "timestamp": int(time.time())
        }

def fetch_steel_watchlist():
    return [fetch_company(s) for s in STEEL_SYMBOLS]
