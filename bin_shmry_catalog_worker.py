#!/usr/bin/env python3
import sqlite3, time, hashlib, re, os
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urljoin
from html import unescape

ROOT = Path.home() / "shmry_cloud_hyperscale"
DB = ROOT / "vault/shmry_cloud.db"
IMG = ROOT / "catalog_images"
LOG = ROOT / "logs/catalog_ingestion.log"

def log(x):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(time.strftime("%F %T ") + x + "\n")
    print(x)

def fetch(url):
    req = Request(url, headers={
        "User-Agent": "Mozilla/5.0 SHMRY-RANGOONS-CATALOG/1.0",
        "Accept": "text/html,application/xhtml+xml"
    })
    with urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8", "ignore")

def clean_price(x):
    if not x:
        return None
    x = re.sub(r"[^\d.]", "", x)
    try:
        return float(x) if x else None
    except:
        return None

def sku_hash(source, url, title):
    return hashlib.sha256(f"{source}|{url}|{title}".encode()).hexdigest()[:24]

def extract_basic_products(source, base_url, html):
    products = []

    # Generic JSON-LD/product-ish extraction fallback
    title_patterns = [
        r'"name"\s*:\s*"([^"]{3,180})"',
        r'"title"\s*:\s*"([^"]{3,180})"',
        r'alt="([^"]{3,180})"'
    ]
    price_patterns = [
        r'"price"\s*:\s*"?([0-9,.]+)"?',
        r'Rs\.?\s*([0-9,]+)',
        r'PKR\s*([0-9,]+)'
    ]
    img_patterns = [
        r'"image"\s*:\s*"([^"]+)"',
        r'<img[^>]+src="([^"]+)"'
    ]

    titles = []
    for p in title_patterns:
        titles += re.findall(p, html, flags=re.I)

    prices = []
    for p in price_patterns:
        prices += re.findall(p, html, flags=re.I)

    imgs = []
    for p in img_patterns:
        imgs += re.findall(p, html, flags=re.I)

    titles = [unescape(t).strip() for t in titles if len(t.strip()) > 3]
    prices = [clean_price(p) for p in prices]
    prices = [p for p in prices if p and p > 0]
    imgs = [urljoin(base_url, i.replace("\\/", "/")) for i in imgs if i.startswith("http") or i.startswith("/")]

    limit = min(len(titles), 100)
    for i in range(limit):
        title = titles[i]
        price = prices[i % len(prices)] if prices else None
        img = imgs[i % len(imgs)] if imgs else None
        products.append({
            "title": title[:180],
            "price": price,
            "image": img,
            "url": base_url
        })

    return products

def download_image(source, sku, image_url):
    if not image_url:
        return None
    folder = IMG / source.lower()
    folder.mkdir(parents=True, exist_ok=True)
    ext = ".jpg"
    if ".webp" in image_url.lower():
        ext = ".webp"
    path = folder / f"{sku}{ext}"

    if path.exists() and path.stat().st_size > 100:
        return str(path)

    try:
        req = Request(image_url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=15) as r:
            data = r.read()
        if len(data) > 100:
            path.write_bytes(data)
            return str(path)
    except Exception as e:
        log(f"⚠️ image failed {image_url}: {e}")
    return None

con = sqlite3.connect(DB)
cur = con.cursor()

jobs = cur.execute("""
SELECT id, source, category, url FROM raw_scrape_queue
WHERE status='PENDING'
ORDER BY id
LIMIT 20
""").fetchall()

if not jobs:
    log("No pending crawl jobs.")
    raise SystemExit

for jid, source, category, url in jobs:
    try:
        log(f"🌐 Fetching {source} | {category} | {url}")
        html = fetch(url)
        products = extract_basic_products(source, url, html)
        log(f"   found candidate products: {len(products)}")

        for p in products:
            title = p["title"]
            price = p["price"]
            image_url = p["image"]
            product_url = p["url"]
            sku = sku_hash(source, product_url, title)
            cost = round(price * 0.82, 2) if price else None
            margin = round(price - cost, 2) if price and cost else None
            local_img = download_image(source, sku, image_url)

            cur.execute("""
            INSERT OR IGNORE INTO raw_scrape_results
            (ts, source, source_url, raw_title, raw_category, raw_price, raw_image_url, raw_description, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'RAW')
            """, (int(time.time()), source, product_url, title, category, str(price), image_url, title))

            cur.execute("""
            INSERT OR IGNORE INTO catalog_master
            (ts, sku_hash, source, category, brand, item, description, selling_price,
             cost_to_acquire, gross_margin, product_url, image_url, local_image_path,
             stock_status, verification_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'UNKNOWN', 'SCRAPED_UNVERIFIED')
            """, (
                int(time.time()), sku, source, category, None, title, title,
                price, cost, margin, product_url, image_url, local_img
            ))

            if price:
                cur.execute("""
                INSERT INTO catalog_price_history
                (ts, sku_hash, source, selling_price, product_url)
                VALUES (?, ?, ?, ?, ?)
                """, (int(time.time()), sku, source, price, product_url))

            if image_url:
                cur.execute("""
                INSERT OR IGNORE INTO catalog_images
                (ts, sku_hash, source, image_url, local_image_path, status)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (int(time.time()), sku, source, image_url, local_img, "DOWNLOADED" if local_img else "FAILED"))

        cur.execute("UPDATE raw_scrape_queue SET status='DONE', attempts=attempts+1 WHERE id=?", (jid,))
        con.commit()

    except Exception as e:
        cur.execute("""
        UPDATE raw_scrape_queue
        SET status='FAILED', attempts=attempts+1, last_error=?
        WHERE id=?
        """, (str(e), jid))
        con.commit()
        log(f"❌ job failed {url}: {e}")

print("\n✅ Crawl worker pass complete.")
print("Catalog rows:", cur.execute("SELECT COUNT(*) FROM catalog_master").fetchone()[0])
print("Images:", cur.execute("SELECT COUNT(*) FROM catalog_images").fetchone()[0])

con.close()
