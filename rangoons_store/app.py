from flask import Flask, request, send_from_directory
import sqlite3, os, math
from pathlib import Path

ROOT = Path.home() / "shmry_cloud_hyperscale"
DB = ROOT / "vault/shmry_cloud.db"
IMG_ROOT = ROOT / "catalog_images"

app = Flask(__name__)

def db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

@app.route("/media/<source>/<path:name>")
def media(source, name):
    return send_from_directory(IMG_ROOT / source, name)

@app.route("/")
def home():
    q = request.args.get("q","").strip()
    source = request.args.get("source","").strip()
    page = max(int(request.args.get("page","1")), 1)
    per = 60
    off = (page-1)*per

    where = []
    args = []

    if q:
        where.append("(item LIKE ? OR category LIKE ? OR subcategory LIKE ? OR brand LIKE ?)")
        args += [f"%{q}%"]*4

    if source:
        where.append("source_model=?")
        args.append(source)

    where_sql = "WHERE " + " AND ".join(where) if where else ""

    con = db()
    total = con.execute(f"SELECT COUNT(*) FROM rangoons_universal_catalog {where_sql}", args).fetchone()[0]

    rows = con.execute(f"""
        SELECT sku_code, source_model, category, subcategory, brand, item,
               selling_price, gross_margin, potential_monthly_volume,
               monthly_gross_profit, local_image_path, product_url
        FROM rangoons_universal_catalog
        {where_sql}
        ORDER BY monthly_gross_profit DESC
        LIMIT ? OFFSET ?
    """, args + [per, off]).fetchall()

    sources = con.execute("""
        SELECT source_model, COUNT(*) c
        FROM rangoons_universal_catalog
        GROUP BY source_model
        ORDER BY c DESC
    """).fetchall()

    real_count = 0
    try:
        real_count = con.execute("SELECT COUNT(*) FROM catalog_master").fetchone()[0]
    except Exception:
        pass

    img_count = 0
    try:
        img_count = con.execute("SELECT COUNT(*) FROM catalog_images").fetchone()[0]
    except Exception:
        pass

    con.close()

    cards = ""
    for r in rows:
        img = ""
        lp = r["local_image_path"]
        if lp and "/catalog_images/" in lp:
            rel = lp.split("/catalog_images/",1)[1]
            img = f"/media/{rel}"
        else:
            img = "https://via.placeholder.com/300x220?text=RANGOONS"

        cards += f"""
        <div class="card">
          <img src="{img}" loading="lazy">
          <div class="body">
            <div class="src">{r['source_model']} · {r['category']} · {r['subcategory'] or ''}</div>
            <h3>{r['item']}</h3>
            <p>SKU: {r['sku_code']}</p>
            <b>PKR {r['selling_price'] or 0:,.0f}</b>
            <small>Margin: PKR {r['gross_margin'] or 0:,.0f} · Monthly profit: PKR {r['monthly_gross_profit'] or 0:,.0f}</small>
          </div>
        </div>
        """

    source_links = '<a href="/">All</a> '
    for s in sources:
        source_links += f'<a href="/?source={s["source_model"]}">{s["source_model"]} ({s["c"]:,})</a> '

    pages = math.ceil(total/per) if total else 1

    return f"""
<!doctype html>
<html>
<head>
<title>RANGOONS Store</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{{font-family:Arial;margin:0;background:#f6f7fb;color:#111}}
header{{background:#0b1020;color:white;padding:22px}}
h1{{margin:0;font-size:30px}}
.stats{{margin-top:10px;color:#b9c3ff}}
form{{padding:18px;background:white;display:flex;gap:10px;flex-wrap:wrap}}
input,select,button{{padding:12px;border:1px solid #ddd;border-radius:10px}}
button{{background:#0b1020;color:white}}
.sources{{padding:0 18px 18px;background:white}}
.sources a{{margin-right:12px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:16px;padding:18px}}
.card{{background:white;border-radius:18px;overflow:hidden;box-shadow:0 3px 12px #0001}}
.card img{{width:100%;height:180px;object-fit:cover;background:#eee}}
.body{{padding:14px}}
.src{{font-size:12px;color:#666}}
h3{{font-size:16px;min-height:42px}}
small{{display:block;margin-top:8px;color:#555}}
.pager{{padding:20px;text-align:center}}
.pager a{{margin:6px;padding:10px 14px;background:white;border-radius:10px;text-decoration:none}}
.warn{{padding:12px 18px;background:#fff3cd;color:#5a4300}}
</style>
</head>
<body>
<header>
<h1>🛒 RANGOONS Store</h1>
<div class="stats">Universal catalog: {total:,} visible items · Real scraped rows: {real_count:,} · Image records: {img_count:,}</div>
</header>

<div class="warn">
Current store is live from SQLite. Some 200k rows are generated/photo-linked; real verified scraping currently has {real_count:,} rows and must keep increasing.
</div>

<form>
<input name="q" placeholder="Search products..." value="{q}">
<select name="source">
<option value="">All Sources</option>
<option {"selected" if source=="Daraz-style" else ""}>Daraz-style</option>
<option {"selected" if source=="Imtiaz-style" else ""}>Imtiaz-style</option>
<option {"selected" if source=="RANGOONS Priority" else ""}>RANGOONS Priority</option>
</select>
<button>Search</button>
</form>

<div class="sources">{source_links}</div>
<div class="grid">{cards}</div>

<div class="pager">
<a href="/?q={q}&source={source}&page={max(page-1,1)}">Previous</a>
Page {page} / {pages}
<a href="/?q={q}&source={source}&page={page+1}">Next</a>
</div>
</body>
</html>
"""

@app.route("/health")
def health():
    return {"ok": True, "service": "RANGOONS_STORE", "db": str(DB)}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8088)
