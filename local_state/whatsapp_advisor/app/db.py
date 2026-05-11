import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Tuple

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "advisor.sqlite3"

SCHEMA = """
PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  wa_id TEXT UNIQUE NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  wa_id TEXT NOT NULL,
  direction TEXT NOT NULL, -- in|out
  body TEXT NOT NULL,
  ts TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS portfolio (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  wa_id TEXT NOT NULL,
  symbol TEXT NOT NULL,
  qty REAL NOT NULL DEFAULT 0,
  avg_price REAL NOT NULL DEFAULT 0,
  updated_at TEXT NOT NULL,
  UNIQUE(wa_id, symbol)
);

CREATE TABLE IF NOT EXISTS notes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  wa_id TEXT NOT NULL,
  note TEXT NOT NULL,
  ts TEXT NOT NULL
);
"""

def connect() -> sqlite3.Connection:
  DB_PATH.parent.mkdir(parents=True, exist_ok=True)
  con = sqlite3.connect(str(DB_PATH))
  con.row_factory = sqlite3.Row
  return con

def init_db() -> None:
  con = connect()
  try:
    con.executescript(SCHEMA)
    con.commit()
  finally:
    con.close()

def exec_one(sql: str, params: Tuple[Any, ...] = ()) -> None:
  con = connect()
  try:
    con.execute(sql, params)
    con.commit()
  finally:
    con.close()

def fetch_all(sql: str, params: Tuple[Any, ...] = ()) -> List[Dict[str, Any]]:
  con = connect()
  try:
    cur = con.execute(sql, params)
    return [dict(r) for r in cur.fetchall()]
  finally:
    con.close()
