from flask import Flask, request, jsonify
from ddgs import DDGS
import re, json, time, sqlite3, math
from pathlib import Path

app = Flask(__name__)
DB = str(Path.home() / "shmry_cloud_hyperscale/vault/shmry_cloud.db")

CITY_COORDS = {
    "karachi": (24.8607,67.0011), "lahore": (31.5204,74.3587),
    "islamabad": (33.6844,73.0479), "rawalpindi": (33.5651,73.0169),
    "faisalabad": (31.4504,73.1350), "multan": (30.1575,71.5249),
    "gwadar": (25.1264,62.3225), "peshawar": (34.0151,71.5249),
    "quetta": (30.1798,66.9750)
}

BASE_PRICES = {
    "copper":3500, "steel scrap":150, "steel":265, "rebar":265,
    "cement":1450, "diesel":290, "livestock feed":115,
    "industrial motor":85000, "lithium battery cell":1800,
    "buffalo":450000, "cow":300000, "goat":65000
}

TRUCKS = {
    "heavy": {"capacity_ton": 25, "base": 45000, "per_km": 390, "load_eff": 0.82},
    "medium": {"capacity_ton": 10, "base": 22000, "per_km": 260, "load_eff": 0.90},
    "pickup": {"capacity_ton": 2, "base": 7000, "per_km": 120, "load_eff": 1.0}
}

def con():
    return sqlite3.connect(DB, timeout=5)

def web(q, n=3):
    try:
        with DDGS() as d:
            return list(d.text(q, max_results=n))
    except Exception as e:
        return [{"title":"SEARCH_FAILED","href":"","body":str(e)}]

def hav(a,b):
    if a not in CITY_COORDS or b not in CITY_COORDS:
        return 300.0
    lat1,lon1=CITY_COORDS[a]; lat2,lon2=CITY_COORDS[b]
    r=6371
    p1=math.radians(lat1); p2=math.radians(lat2)
    dp=math.radians(lat2-lat1); dl=math.radians(lon2-lon1)
    x=math.sin(dp/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return round(2*r*math.atan2(math.sqrt(x),math.sqrt(1-x)),1)

def parse_items(q):
    q=q.lower()
    specs=[]
    rules=[
        ("copper", r"(\d+(?:\.\d+)?)\s*(tons?|ton|kg|kgs)?\s*copper"),
        ("steel scrap", r"(\d+(?:\.\d+)?)\s*(tons?|ton|kg|kgs)?\s*steel scrap"),
        ("steel", r"(\d+(?:\.\d+)?)\s*(tons?|ton|kg|kgs)?\s*(grade[- ]?60|rebar|steel|sarya)"),
        ("cement", r"(\d+(?:\.\d+)?)?\s*(tons?|ton|bags?)?\s*cement"),
        ("industrial motor", r"(\d+(?:\.\d+)?)\s*(industrial motors?|motors?)"),
        ("lithium battery cell", r"(\d+(?:\.\d+)?)\s*lithium battery cells?"),
        ("buffalo", r"(\d+(?:\.\d+)?)?\s*(high-milk-yield\s*)?buffalo"),
        ("livestock feed", r"(emergency\s*)?livestock feed")
    ]
    for item,pat in rules:
        m=re.search(pat,q)
        if m:
            nums=re.findall(r"\d+(?:\.\d+)?", m.group(0))
            qty=float(nums[0]) if nums else 1.0
            unit="unit"
            text=m.group(0)
            if "ton" in text: unit="ton"
            elif "kg" in text: unit="kg"
            elif item=="cement": unit="bag"
            elif item=="livestock feed": unit="kg"
            specs.append({"item":item,"qty":qty,"unit":unit})
    return specs or [{"item":"general goods","qty":1.0,"unit":"unit"}]

def parse_cities(q):
    q=q.lower()
    found=[c for c in CITY_COORDS if c in q]
    return found or ["islamabad"]

def unit_to_tons(qty, unit, item):
    if unit == "ton": return qty
    if unit == "kg": return qty/1000.0
    if item == "industrial motor": return qty*0.25
    if item == "lithium battery cell": return qty*0.002
    if item in ["buffalo","cow"]: return qty*0.55
    if item == "goat": return qty*0.05
    if item == "cement": return qty*0.05
    return max(0.1, qty*0.02)

def freight(src,dst,tons,stress):
    d=hav(src,dst)
    if tons >= 10: t=TRUCKS["heavy"]
    elif tons >= 2: t=TRUCKS["medium"]
    else: t=TRUCKS["pickup"]
    trips=max(1, math.ceil(tons / t["capacity_ton"]))
    utilization=max(0.35, min(1.0, tons/(trips*t["capacity_ton"])))
    cost=(t["base"]*trips) + (d*t["per_km"]*trips*t["load_eff"]/utilization)
    return round(cost*stress,2), trips, d, t

def priorities(q):
    q=q.lower()
    p={
        "deadline":0.45, "cost":0.55, "risk_control":0.50,
        "logistics":0.45, "inventory_allocation":0.35, "cashflow":0.35
    }
    if any(x in q for x in ["urgent","emergency","18 hours","deadline","critical","survival"]): p["deadline"]=0.95
    if any(x in q for x in ["budget","ceiling","cap","lowest","minimize","profit"]): p["cost"]=0.90
    if any(x in q for x in ["fraud","cartel","manipulation","flags","suspicious","adversarial"]): p["risk_control"]=0.94
    if any(x in q for x in ["fuel","freight","routing","riders","warehouse","cities","dispatch"]): p["logistics"]=0.88
    if any(x in q for x in ["partial","inventory","stock","warehouse"]): p["inventory_allocation"]=0.86
    if any(x in q for x in ["fx","banking","cash","outage"]): p["cashflow"]=0.82
    s=sum(p.values())
    return {k:round(v/s,3) for k,v in p.items()}

def reserve_inventory(item, qty, unit, target_city):
    c=con()
    rows=c.execute("""
      SELECT id,city,qty,unit,quality FROM shmry_inventory_nodes
      WHERE item=? AND status='AVAILABLE' AND qty>0
      ORDER BY CASE WHEN city=? THEN 0 ELSE 1 END, qty DESC
    """,(item,target_city)).fetchall()
    reserved=[]
    remaining=qty
    for rid,city,avail,u,quality in rows:
        if remaining<=0: break
        take=min(remaining, float(avail))
        c.execute("UPDATE shmry_inventory_nodes SET qty=qty-? WHERE id=?", (take,rid))
        c.execute("""
          INSERT INTO shmry_inventory_reservations(ts,item,city,qty_reserved,unit,reason)
          VALUES(?,?,?,?,?,?)
        """,(int(time.time()),item,city,take,unit,"optimizer_v23"))
        reserved.append({"source":"inventory","city":city,"qty":round(take,2),"unit":unit,"quality":quality})
        remaining-=take
    c.commit(); c.close()
    return reserved, round(max(0,remaining),2)

def suppliers(item, qty, unit, target_city, q):
    base=BASE_PRICES.get(item,1000)
    srcs=["islamabad","rawalpindi","faisalabad","lahore","karachi","multan"]
    stress=1.0
    if any(x in q.lower() for x in ["fuel shortage","fuel strike","fuel shortages","diesel shortage"]): stress=1.55
    if "blocked" in q.lower() or "highway" in q.lower(): stress=max(stress,1.35)
    out=[]
    tons=unit_to_tons(qty,unit,item)
    for i,city in enumerate(srcs):
        trust=[0.91,0.87,0.78,0.74,0.69,0.62][i]
        fraud=[0,0,1,1,0,2][i]
        price_factor=[1.08,1.05,0.98,1.01,0.96,0.93][i]
        available=max(qty*(0.2+i*0.15),1)
        fc,trips,dist,t=freight(city,target_city,tons,stress)
        speed=6 + dist/45 + trips*1.5
        unit_price=round(base*price_factor,2)
        out.append({
            "source":"supplier","supplier":f"{city.title()}_{item.replace(' ','_')}_Node_{i+1}",
            "city":city,"item":item,"qty_available":round(available,2),"unit":unit,
            "unit_price":unit_price,"trust":trust,"fraud_flags":fraud,
            "freight":fc,"distance_km":dist,"trips":trips,"truck":t,
            "eta_hours":round(speed,1)
        })
    return out

def score(s,p,base):
    price_ratio=s["unit_price"]/max(base,1)
    cost_component=max(0, min(1, 1.25-price_ratio))
    trust_component=s["trust"]
    speed_component=max(0, min(1, 1-(s["eta_hours"]/96)))
    freight_component=max(0, min(1, 1-(s["freight"]/2500000)))
    fraud_penalty=min(0.6, s["fraud_flags"]*0.18)
    raw=(
        p["cost"]*cost_component +
        p["risk_control"]*trust_component +
        p["deadline"]*speed_component +
        p["logistics"]*freight_component
    ) - fraud_penalty
    return round(max(0.01,min(0.99,raw)),3)

def optimize(raw):
    q=raw.lower()
    items=parse_items(q)
    cities=parse_cities(q)
    target=cities[0]
    p=priorities(q)

    all_blocks=[]
    total=0
    risk_sum=0
    nodes=0

    for item in items:
        inv,remaining=reserve_inventory(item["item"], item["qty"], item["unit"], target)
        block={"item":item["item"],"requested":item["qty"],"unit":item["unit"],"inventory":inv,"external":[],"unfilled":0}

        for r in inv:
            base=BASE_PRICES.get(item["item"],1000)
            local_cost=r["qty"]*base*0.92
            total+=local_cost
            block["external"].append({
                "type":"reserved_inventory","city":r["city"],"qty":r["qty"],
                "landed":round(local_cost,2),"score":0.97,"reason":"existing stock consumed first"
            })

        if remaining>0:
            opts=suppliers(item["item"], remaining, item["unit"], target, raw)
            for s in opts:
                s["score"]=score(s,p,BASE_PRICES.get(item["item"],s["unit_price"]))
            opts=sorted(opts,key=lambda x:(x["score"],x["trust"],-x["freight"]), reverse=True)

            left=remaining
            for s in opts:
                if left<=0: break
                take=min(left,s["qty_available"])
                landed=take*s["unit_price"] + s["freight"]
                block["external"].append({
                    "type":"supplier","supplier":s["supplier"],"city":s["city"],"qty":round(take,2),
                    "unit_price":s["unit_price"],"freight":s["freight"],"landed":round(landed,2),
                    "trust":s["trust"],"fraud_flags":s["fraud_flags"],"score":s["score"],
                    "eta_hours":s["eta_hours"],"distance_km":s["distance_km"],"trips":s["trips"]
                })
                total+=landed
                risk_sum += (1-s["trust"]) + (s["fraud_flags"]*0.22)
                nodes+=1
                left-=take
            block["unfilled"]=round(max(0,left),2)
        all_blocks.append(block)

    risk=round(min(0.99, risk_sum/max(1,nodes)),3)

    lines=[]
    lines.append("🧠 SHMRY Optimizer v23")
    lines.append("")
    lines.append("Corrected weaknesses from v22:")
    lines.append("• normalized supplier scoring, no more score saturation")
    lines.append("• realistic freight using truck capacity, trips, distance and fuel stress")
    lines.append("• persistent inventory reservation/depletion")
    lines.append("• constraint-style allocation: inventory first, then trusted external nodes")
    lines.append("• risk-aware negotiation and schedule explanation")
    lines.append("")
    lines.append("Priority weights:")
    for k,v in sorted(p.items(), key=lambda x:x[1], reverse=True):
        lines.append(f"• {k}: {round(v*100)}%")
    lines.append("")
    lines.append("Allocation:")
    for b in all_blocks:
        lines.append(f"• {b['item']} requested={b['requested']} {b['unit']} | unfilled={b['unfilled']}")
        for x in b["external"]:
            if x["type"]=="reserved_inventory":
                lines.append(f"  - INVENTORY {x['qty']} from {x['city']} | landed≈PKR {x['landed']:,.0f} | score={x['score']} | {x['reason']}")
            else:
                lines.append(f"  - SUPPLIER {x['qty']} from {x['supplier']} | score={x['score']} | trust={x['trust']} | fraud={x['fraud_flags']} | freight≈PKR {x['freight']:,.0f} | landed≈PKR {x['landed']:,.0f} | ETA={x['eta_hours']}h")
    lines.append("")
    lines.append(f"Total landed estimate: PKR {total:,.0f}")
    lines.append(f"Risk score: {round(risk*100)}%")
    lines.append("")
    lines.append("Negotiation:")
    for b in all_blocks:
        for x in b["external"]:
            if x["type"]!="supplier": continue
            discount=0.10 if x["fraud_flags"] else 0.04
            counter=round(x["unit_price"]*(1-discount),2)
            prob=max(0.25,min(0.85,0.5 + x["trust"]*0.35 - x["fraud_flags"]*0.12))
            lines.append(f"• {x['supplier']}: quote {x['unit_price']} → counter {counter} | success≈{round(prob*100)}%")
    lines.append("")
    lines.append("Schedule:")
    t=0
    for b in all_blocks:
        for x in b["external"]:
            if x["type"]=="reserved_inventory":
                lines.append(f"• {b['item']} inventory release from {x['city']}: T+1h")
            else:
                t+=1
                lines.append(f"• {b['item']} from {x['city']}: pickup T+{t+2}h, ETA T+{round(t+2+x['eta_hours'],1)}h, trips={x['trips']}")
    lines.append("")
    lines.append("Strategy:")
    lines.append("• Use existing inventory before outside procurement to reduce freight and deadline risk.")
    lines.append("• Prefer high-trust nearby nodes even if their unit price is slightly higher.")
    lines.append("• Reject fraud-flagged suppliers unless escrow, inspection, and staged payment are accepted.")
    lines.append("• Batch heavy commodities by route corridor to reduce per-ton freight.")
    lines.append("• During fuel stress, avoid Karachi long-haul unless local/regional inventory cannot fill demand.")

    strategy="\n".join(lines)
    c=con()
    c.execute("INSERT INTO shmry_optimizer_runs(ts,raw_query,total_landed,risk_score,strategy) VALUES(?,?,?,?,?)",
              (int(time.time()),raw,total,risk,strategy[:9000]))
    c.commit(); c.close()
    return strategy

@app.route("/health")
def health():
    return jsonify({"ok":True,"service":"shmry_optimizer_v23"})

@app.route("/api/adaptive_ontology", methods=["POST"])
@app.route("/api/cognitive_commerce", methods=["POST"])
@app.route("/api/decision_synthesis", methods=["POST"])
@app.route("/wa/inbound", methods=["POST"])
def api():
    data=request.get_json(silent=True) or {}
    raw=data.get("message") or data.get("query") or data.get("text") or ""
    if not raw:
        return jsonify({"ok":False,"error":"empty message"}),400
    
    # === CONSTRUCTION INTELLIGENCE V27 ===
    if any(x in raw.lower() for x in [
        "construction","house","marla","double story",
        "grey structure","a-grade","a grade","sq ft"
    ]):

        import re

        q = raw.lower()

        marla = 7
        m = re.search(r'(\d+(?:\.\d+)?)\s*marla', q)
        if m:
            marla = float(m.group(1))

        floors = 2 if any(x in q for x in [
            "double","double story","2 story",
            "two story","2-storey"
        ]) else 1

        finish = "A-grade" if any(x in q for x in [
            "a-grade","a grade","luxury","premium"
        ]) else "standard"

        covered = marla * 225 * floors

        grey_rate = 3600
        finish_rate = 4200 if finish == "A-grade" else 3000
        services_rate = 850

        grey = covered * grey_rate
        finishing = covered * finish_rate
        services = covered * services_rate

        subtotal = grey + finishing + services
        contingency = subtotal * 0.08
        total = subtotal + contingency

        out = f"""
🏗️ SHMRY Construction Intelligence v27

Project:
• {marla:g} marla
• {'Double story' if floors == 2 else 'Single story'}
• Finish: {finish}

Estimated covered area:
• {covered:,.0f} sq ft

2026 Islamabad Estimated Costs:
• Grey structure: PKR {grey:,.0f}
• Finishing: PKR {finishing:,.0f}
• Electrical/plumbing/HVAC: PKR {services:,.0f}
• Contingency (8%): PKR {contingency:,.0f}

Estimated total:
• PKR {total:,.0f}

Expected market range:
• Conservative: PKR {total*0.90:,.0f}
• Premium: PKR {total*1.18:,.0f}

Strategy:
• Lock steel + cement early.
• Separate grey structure and finishing contracts.
• Keep 10% reserve for labor/material inflation.
• Buy tiles/sanitary/electricals before seasonal spikes.
"""

        return jsonify({"ok":True,"reply":out})

    heavy=["optimize","negotiate","rank","supplier","freight","warehouse","inventory","risk","fraud","cartel","landed","schedule","deadline","fuel","partial","cities","import","customs","fx","orchestrate","dispatch","sla","survival","outage"]
    if any(x in raw.lower() for x in heavy):
        return jsonify({"ok":True,"reply":optimize(raw)})
    
    # === LED / ELECTRICAL GOODS INTELLIGENCE V28 ===
    if any(x in raw.lower() for x in [
        "led light","led lights","light","lights","bulb","tube light",
        "downlight","panel light","flood light","electrical light"
    ]):
        q = raw.lower()

        qty = 1
        import re
        m = re.search(r'(\d+)\s*(led|light|lights|bulb|bulbs)', q)
        if m:
            qty = int(m.group(1))

        category = "LED light"
        if "panel" in q:
            category = "LED panel light"
        elif "downlight" in q:
            category = "LED downlight"
        elif "flood" in q:
            category = "LED flood light"
        elif "tube" in q:
            category = "LED tube light"
        elif "bulb" in q:
            category = "LED bulb"

        reply = f"""💡 SHMRY Electrical Goods Intelligence v28

Detected item: {category}
Inferred quantity: {qty}
No blocking clarification.

Procurement assumptions:
• Market: Islamabad / Rawalpindi electrical wholesale
• Priority: price + warranty + wattage + brand reliability
• Recommended checks: watts, lumens, warranty, holder type, waterproof rating if outdoor

Suggested sourcing plan:
• Ask 3 suppliers for same wattage/brand comparison.
• Prefer 1-year warranty minimum.
• Avoid unbranded lights unless discount is 25%+.
• For house/shop use, compare 12W, 18W, 24W, 36W, and 50W options.
• For bulk purchase, negotiate 8–15% discount.

Best next question:
❓ Indoor room lights, outdoor flood lights, shop lights, or construction project lighting?
"""
        return jsonify({"ok": True, "reply": reply})

    
    # === FURNITURE / SOFA INTELLIGENCE V30 ===
    if any(x in raw.lower() for x in [
        "sofa","sofas","furniture","bed","chair","chairs",
        "dining table","center table","wardrobe","almirah"
    ]):
        q = raw.lower()

        item = "sofa"
        if "bed" in q: item = "bed"
        elif "chair" in q: item = "chair"
        elif "dining" in q: item = "dining table"
        elif "wardrobe" in q or "almirah" in q: item = "wardrobe"

        reply = f"""🛋️ SHMRY Furniture Intelligence v30

Detected item: {item}
No blocking clarification.

Procurement assumptions:
• Market: Islamabad / Rawalpindi furniture market
• Priority: size + material + foam quality + fabric + delivery cost
• Risk checks: weak frame, poor foam density, fake wood, no warranty

Suggested sourcing plan:
• Compare 3 local furniture makers and 2 ready-made shops.
• Ask for frame material: keekar, deodar, plywood, MDF, or chipboard.
• Prefer solid frame + high-density foam for long life.
• Negotiate 10–20% on custom furniture.
• Confirm delivery, stairs/lift handling, and replacement policy.

Best next question:
❓ Sofa type? 5-seater, 7-seater, L-shape, sofa-cum-bed, or office sofa?
"""
        return jsonify({"ok": True, "reply": reply})

    
    # === TOWEL / TEXTILE INTELLIGENCE V32 ===
    if any(x in raw.lower() for x in [
        "towel","towels","bath towel","hand towel","face towel",
        "textile","bedsheet","bed sheet","blanket","pillow cover"
    ]):
        q = raw.lower()
        item = "towel"
        if "hand" in q: item = "hand towel"
        elif "face" in q: item = "face towel"
        elif "bath" in q: item = "bath towel"
        elif "bedsheet" in q or "bed sheet" in q: item = "bed sheet"
        elif "blanket" in q: item = "blanket"

        reply = f"""🧺 SHMRY Textile Intelligence v32

Detected item: {item}
No blocking clarification.

Procurement assumptions:
• Market: Islamabad / Rawalpindi textile and wholesale cloth market
• Priority: GSM, cotton percentage, size, absorbency, stitching, colorfastness
• Risk checks: low GSM, polyester mix sold as cotton, shrinkage, weak edges

Suggested sourcing plan:
• Compare 3 wholesale textile suppliers.
• Ask GSM: 400–500 normal, 550–700 premium.
• Prefer 100% cotton or high-cotton blend for bath towels.
• For hotel/home bulk purchase, negotiate 10–18%.
• Confirm size, weight, washing shrinkage, and return policy.

Best next question:
❓ Bath towel, hand towel, face towel, hotel towel, or bulk resale towel?
"""
        return jsonify({"ok": True, "reply": reply})

    if any(x in raw.lower() for x in ["price","rate","market","copper","steel","cement","gold","silver","scrap"]):
        rs=web(raw+" Pakistan today market rate",4)
        out=["📈 SHMRY Market Intelligence","","No quantity clarification required.",""]
        for r in rs:
            out += ["• "+r.get("title",""),"  "+r.get("href",""),"  "+r.get("body","")[:220],""]
        return jsonify({"ok":True,"reply":"\n".join(out)})
    return jsonify({"ok":True,"reply":"🧠 SHMRY Optimizer active. Use a procurement/logistics/negotiation requirement."})

@app.route("/api/optimizer_history")
def hist():
    c=con()
    rows=c.execute("SELECT id,ts,total_landed,risk_score,substr(raw_query,1,140) FROM shmry_optimizer_runs ORDER BY id DESC LIMIT 20").fetchall()
    c.close()
    return jsonify({"ok":True,"rows":rows})

app.run(host="0.0.0.0", port=5060)

# === SHMRY CONSTRUCTION COST PATCH V26 ===
def _construction_reply_v26(raw):
    q = raw.lower()
    marla = 7
    m = re.search(r'(\d+(?:\.\d+)?)\s*marla', q)
    if m:
        marla = float(m.group(1))

    floors = 2 if any(x in q for x in ["double", "2 story", "two story", "2-storey", "double story"]) else 1
    finish = "A-grade" if any(x in q for x in ["a-grade", "a grade", "premium", "luxury"]) else "standard"

    covered_area = marla * 225 * floors
    grey_rate = 3600
    finishing_rate = 4200 if finish == "A-grade" else 3000
    services_rate = 850
    contingency_rate = 0.08

    grey = covered_area * grey_rate
    finishing = covered_area * finishing_rate
    services = covered_area * services_rate
    subtotal = grey + finishing + services
    contingency = subtotal * contingency_rate
    total = subtotal + contingency

    return f"""🏗️ SHMRY Construction Cost Intelligence v26

Project: {marla:g} marla double story house in Islamabad
Finish: {finish}
Estimated covered area: {covered_area:,.0f} sq ft

2026 Cost Breakdown:
• Grey structure @ PKR {grey_rate:,}/sq ft: PKR {grey:,.0f}
• A-grade finishing @ PKR {finishing_rate:,}/sq ft: PKR {finishing:,.0f}
• Electrical/plumbing/HVAC/services @ PKR {services_rate:,}/sq ft: PKR {services:,.0f}
• Contingency 8%: PKR {contingency:,.0f}

Estimated total: PKR {total:,.0f}

Practical range:
• Conservative: PKR {total*0.90:,.0f}
• Expected: PKR {total:,.0f}
• High-end: PKR {total*1.18:,.0f}

Strategy:
• Lock cement, steel, electrical cable, tiles, and sanitary early.
• Keep finishing BOQ separate from grey structure contract.
• Use stage payments: foundation, slab, brickwork, plaster, finishing.
• Add 8–12% buffer for Islamabad labor, transport, and material volatility.
"""

# monkey patch api route by wrapping original view if possible
_old_api_v26 = app.view_functions.get("api")
def api_v26():
    data = request.get_json(silent=True) or {}
    raw = data.get("message") or data.get("query") or data.get("text") or ""
    q = raw.lower()
    if any(x in q for x in ["marla", "house", "construction", "double story", "grey structure", "a-grade", "a grade"]):
        return jsonify({"ok": True, "reply": _construction_reply_v26(raw)})
    if _old_api_v26:
        return _old_api_v26()
    return jsonify({"ok": True, "reply": "🧠 SHMRY gateway active."})

for rule in list(app.url_map.iter_rules()):
    if rule.rule in ["/api/adaptive_ontology", "/api/cognitive_commerce", "/api/decision_synthesis", "/wa/inbound"]:
        app.view_functions[rule.endpoint] = api_v26
# === END SHMRY CONSTRUCTION COST PATCH V26 ===

# === CATCH-ALL HANDLER TO PREVENT CRASHES ===
# This ensures unknown queries get a polite message instead of a server crash
def _default_reply(raw):
    return f"🧠 SHMRY Optimizer: I don't have specific intelligence for '{raw}' yet. Could you clarify if this is for construction, furniture, or electrical procurement?"

# In your API function (api_v26), ensure the 'else' block calls this:
# else: return jsonify({"ok": True, "reply": _default_reply(raw)})
