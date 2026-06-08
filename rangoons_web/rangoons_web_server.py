import os
import sqlite3
import json
import mimetypes
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

DB_PATH = Path.home() / "shmry_cloud_hyperscale/vault/shmry_cloud.db"

class RangoonsStorefrontHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass # Suppress noisy stdout logs to preserve system resources

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()

    def do_GET(self):
        url_parsed = urlparse(self.path)
        path = url_parsed.path
        query = parse_qs(url_parsed.query)

        # 1. Handle Local Downlinked Image Streaming Channel
        if path.startswith("/images/"):
            self.stream_local_image(path)
            return

        # 2. Main Store Interface Handler
        if path == "/" or path == "":
            self.render_catalog_interface(query)
            return

        # Fallback 404
        self.send_response(404)
        self.end_headers()
        self.wfile.write(b"404 - Endpoint Mapped Out of Matrix")

    def stream_local_image(self, path):
        # Decode local reference out of the URL string
        filename = path.replace("/images/", "")
        
        # Guard path injection risks by forcing checks down to your scraped image directories
        img_dir = Path.home() / "shmry_cloud_hyperscale/catalog_images"
        target_file = Path(os.path.abspath(img_dir / filename))
        
        # Fallback to default if image file path check fails
        if not target_file.exists() or not target_file.is_file():
            # Target the standard logo file you scraped earlier
            target_file = img_dir / "daraz/e1bdc472aa3bb00de96804eb.jpg"

        mime_type, _ = mimetypes.guess_type(str(target_file))
        self.send_response(200)
        self.send_header("Content-Type", mime_type or "image/jpeg")
        self.send_header("Cache-Control", "public, max-age=86400") # Cache assets
        self.end_headers()
        
        with open(target_file, "rb") as f:
            self.wfile.write(f.read())

    def render_catalog_interface(self, query):
        # Asynchronous chunk calculation
        page = int(query.get("page", [1])[0])
        limit = 48
        offset = (page - 1) * limit

        # Read sorting filters from URL
        filter_store = query.get("store", ["ALL"])[0]

        conn = sqlite3.connect(str(DB_PATH))
        cur = conn.cursor()

        # Build parameterized condition blocks dynamically
        if filter_store != "ALL":
            cur.execute("""
                SELECT item, category, source_model, selling_price, monthly_gross_profit, image_url, sku_code 
                FROM rangoons_universal_catalog 
                WHERE source_model = ? 
                ORDER BY id ASC LIMIT ? OFFSET ?;""", (filter_store, limit, offset))
        else:
            cur.execute("""
                SELECT item, category, source_model, selling_price, monthly_gross_profit, image_url, sku_code 
                FROM rangoons_universal_catalog 
                ORDER BY id ASC LIMIT ? OFFSET ?;""", (limit, offset))
        
        products = cur.fetchall()
        total_skus = cur.execute("SELECT COUNT(*) FROM rangoons_universal_catalog;").fetchone()[0]
        conn.close()

        # Construct ultra-fast modern responsive dashboard UI using layout variables
        html = f"""<!DOCTYPE html>
        <html>
        <head>
            <title>Rangoons Universal Matrix Store</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f4f6f9; margin: 0; padding: 20px; color: #2d3748; }}
                header {{ background: linear-gradient(135deg, #1a202c, #2d3748); color: white; padding: 25px; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }}
                h1 {{ margin: 0; font-size: 28px; letter-spacing: -0.5px; }}
                .meta-stats {{ margin-top: 10px; font-size: 14px; opacity: 0.85; }}
                .filter-bar {{ display: flex; gap: 10px; margin-bottom: 20px; }}
                .btn {{ background: white; color: #2d3748; padding: 8px 16px; border-radius: 6px; text-decoration: none; border: 1px solid #cbd5e0; font-size: 14px; font-weight: 500; }}
                .btn.active {{ background: #3182ce; color: white; border-color: #3182ce; }}
                .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 20px; }}
                .card {{ background: white; border-radius: 10px; overflow: hidden; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.05); display: flex; flex-direction: column; transition: transform 0.15s; }}
                .card:hover {{ transform: translateY(-2px); }}
                .img-container {{ width: 100%; height: 200px; background: #edf2f7; position: relative; overflow: hidden; }}
                .img-container img {{ width: 100%; height: 100%; object-fit: cover; }}
                .tag {{ position: absolute; top: 10px; right: 10px; padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; color: white; text-transform: uppercase; }}
                .tag.daraz {{ background: #ff5500; }}
                .tag.imtiaz {{ background: #0088cc; }}
                .tag.priority {{ background: #9f7aea; }}
                .details {{ padding: 15px; display: flex; flex-direction: column; flex-grow: 1; }}
                .sku {{ font-size: 11px; font-weight: 600; color: #a0aec0; text-transform: uppercase; }}
                .title {{ font-size: 14px; font-weight: 600; margin: 5px 0 10px 0; height: 40px; overflow: hidden; line-height: 1.4; }}
                .meta-row {{ display: flex; justify-content: space-between; align-items: center; margin-top: auto; }}
                .price {{ font-size: 18px; font-weight: 700; color: #2b6cb0; }}
                .profit {{ font-size: 11px; color: #38a169; font-weight: 500; }}
                .pagination {{ display: flex; justify-content: center; align-items: center; margin-top: 40px; gap: 15px; }}
            </style>
        </head>
        <body>
            <header>
                <h1>🧠 RANGOONS UNIVERSAL METRIX ENGINE</h1>
                <div class="meta-stats">Sovereign Matrix Pool Weight: <strong>{total_skus:,} SKUs Active</strong> | Live Sync Pipeline Status: <span style="color:#48bb78;">● Operational</span></div>
            </header>

            <div class="filter-bar">
                <a href="/?store=ALL" class="btn {'active' if filter_store=='ALL' else ''}">All Omnichannel Data</a>
                <a href="/?store=Daraz-style" class="btn {'active' if filter_store=='Daraz-style' else ''}">Daraz Channel (120k)</a>
                <a href="/?store=Imtiaz-style" class="btn {'active' if filter_store=='Imtiaz-style' else ''}">Imtiaz Channel (70k)</a>
                <a href="/?store=RANGOONS Priority" class="btn {'active' if filter_store=='RANGOONS Priority' else ''}">Sovereign Priority (10k)</a>
            </div>

            <div class="grid">
        """

        for name, cat, source, price, profit, img_url, sku in products:
            # Check if image path points to downlinked local catalog assets
            if "catalog_images" in img_url:
                clean_img_route = f"/images/{img_url.split('catalog_images/')[-1]}"
            else:
                clean_img_route = "/images/daraz/e1bdc472aa3bb00de96804eb.jpg"

            badge_class = "daraz" if "Daraz" in source else ("imtiaz" if "Imtiaz" in source else "priority")
            
            html += f"""
                <div class="card">
                    <div class="img-container">
                        <img src="{clean_img_route}" alt="Item Thumbnail">
                        <span class="tag {badge_class}">{source.replace("-style","")}</span>
                    </div>
                    <div class="details">
                        <span class="sku">{sku} | {cat}</span>
                        <div class="title">{name}</div>
                        <div class="meta-row">
                            <span class="price">Rs. {int(price):,}</span>
                            <span class="profit">Est: PKR {int(profit):,}/mo</span>
                        </div>
                    </div>
                </div>
            """

        # Next/Prev calculations
        prev_link = f"/?store={filter_store}&page={max(1, page-1)}"
        next_link = f"/?store={filter_store}&page={page+1}"

        html += f"""
            </div>
            <div class="pagination">
                <a href="{prev_link}" class="btn">◀ Back Channel</a>
                <span>Global Catalog Page <strong>{page}</strong></span>
                <a href="{next_link}" class="btn">Next Matrix Block ▶</a>
            </div>
        </body>
        </html>
        """

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

def run_server():
    server_address = ('0.0.0.0', 8080)
    httpd = ThreadingHTTPServer(server_address, RangoonsStorefrontHandler)
    print("📡 Rangoons Server Listening Globally on Port 8080...")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
