import sqlite3, time, pathlib
db = pathlib.Path.home() / "SHMRY/marketplace/shmry_business.db"
con = sqlite3.connect(db)
c = con.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS rangoons_inventory(
 sku TEXT PRIMARY KEY,
 name TEXT,
 category TEXT,
 qty REAL,
 price_pkr REAL,
 city TEXT,
 updated_at INTEGER
)""")

c.execute("""CREATE TABLE IF NOT EXISTS nifdu_listings(
 id TEXT PRIMARY KEY,
 title TEXT,
 category TEXT,
 city TEXT,
 price_pkr REAL,
 seller TEXT,
 status TEXT,
 updated_at INTEGER
)""")

c.execute("""CREATE TABLE IF NOT EXISTS whatsapp_leads(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 customer TEXT,
 query TEXT,
 intent TEXT,
 reply TEXT,
 created_at INTEGER
)""")

seed = [
("RNG-SHAMI-6","Rangoons Beef Shami Kabab Pack of 6","Frozen Food",25,500,"Rawalpindi/Islamabad"),
("RNG-BOTTLE-DINO","Dino Water Bottle 450ml","Kids",12,1500,"Rawalpindi/Islamabad"),
("RNG-ZIP-HOLO","Holographic Ziplock Pouches","Packaging",80,0,"Rawalpindi/Islamabad"),
("RNG-ACT-KIDS","Kids Activities Package","Activities",20,3000,"Rawalpindi/Islamabad"),
]
for x in seed:
    c.execute("""INSERT OR IGNORE INTO rangoons_inventory
    (sku,name,category,qty,price_pkr,city,updated_at)
    VALUES (?,?,?,?,?,?,?)""", (*x, int(time.time())))

nifdu = [
("NIFDU-STEEL-RFQ","Steel RFQ Marketplace","Steel","Pakistan",0,"SHMRY","active"),
("NIFDU-SOLAR","Solar + Battery Vendor Marketplace","Energy","Pakistan",0,"SHMRY","active"),
("NIFDU-RANGOONS","Rangoons Retail Marketplace","Retail","Islamabad/Rawalpindi",0,"Rangoons","active"),
]
for x in nifdu:
    c.execute("""INSERT OR IGNORE INTO nifdu_listings
    (id,title,category,city,price_pkr,seller,status,updated_at)
    VALUES (?,?,?,?,?,?,?,?)""", (*x, int(time.time())))

con.commit()
con.close()
print("business db ready:", db)
