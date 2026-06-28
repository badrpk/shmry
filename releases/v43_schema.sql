CREATE TABLE rfqs (rfq_id TEXT PRIMARY KEY, item TEXT, quantity INTEGER, budget REAL, status TEXT DEFAULT 'open', created_at TEXT);
CREATE TABLE settlements (settlement_id TEXT PRIMARY KEY, merchant TEXT, amount REAL, status TEXT, commission REAL, created_at TEXT);
CREATE TABLE solar_quotes (quote_id TEXT PRIMARY KEY, customer TEXT, capacity_kw REAL, estimated_cost REAL, status TEXT DEFAULT 'quoted');
CREATE TABLE commissions (id INTEGER PRIMARY KEY, transaction_id TEXT, amount REAL, party TEXT, type TEXT);
CREATE TABLE bids (bid_id TEXT PRIMARY KEY, rfq_id TEXT, supplier TEXT, amount REAL, delivery_days INTEGER, status TEXT DEFAULT 'pending', created_at TEXT);
CREATE TABLE supplier_scores (supplier TEXT PRIMARY KEY, credit_score INTEGER, reliability REAL, ontime_rate REAL, total_orders INTEGER DEFAULT 0);
