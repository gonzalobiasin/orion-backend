from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 DB
conn = sqlite3.connect("db.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    activo TEXT,
    tipo TEXT,
    estado TEXT,
    capital REAL,
    apalancamiento REAL,
    tp REAL,
    sl REAL,
    be REAL,
    pnl REAL,
    porcentaje REAL,
    fecha TEXT,
    hora TEXT,
    sesion TEXT
)
""")

conn.commit()

# 🔹 MODELOS

class User(BaseModel):
    email: str
    password: str

class Trade(BaseModel):
    user_id: int
    activo: str
    tipo: str
    estado: str
    capital: float
    apalancamiento: float
    tp: float
    sl: float
    be: float | None = None
    pnl: float
    porcentaje: float
    fecha: str
    hora: str
    sesion: str

# 🔐 AUTH

@app.post("/register")
def register(user: User):
    try:
        cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (user.email, user.password))
        conn.commit()
        return {"msg": "ok"}
    except:
        raise HTTPException(status_code=400, detail="Usuario ya existe")

@app.post("/login")
def login(user: User):
    cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (user.email, user.password))
    data = cursor.fetchone()
    if not data:
        raise HTTPException(status_code=401, detail="Login incorrecto")
    return {"user_id": data[0]}

# 📊 TRADES

@app.get("/trades/{user_id}")
def get_trades(user_id: int):
    cursor.execute("SELECT * FROM trades WHERE user_id=?", (user_id,))
    rows = cursor.fetchall()

    result = []
    for r in rows:
        result.append({
            "id": r[0],
            "activo": r[2],
            "tipo": r[3],
            "estado": r[4],
            "capital": r[5],
            "apalancamiento": r[6],
            "tp": r[7],
            "sl": r[8],
            "be": r[9],
            "pnl": r[10],
            "porcentaje": r[11],
            "fecha": r[12],
            "hora": r[13],
            "sesion": r[14]
        })

    return result

@app.post("/trades")
def create_trade(t: Trade):
    cursor.execute("""
    INSERT INTO trades (user_id, activo, tipo, estado, capital, apalancamiento, tp, sl, be, pnl, porcentaje, fecha, hora, sesion)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        t.user_id, t.activo, t.tipo, t.estado,
        t.capital, t.apalancamiento, t.tp, t.sl, t.be,
        t.pnl, t.porcentaje, t.fecha, t.hora, t.sesion
    ))
    conn.commit()
    return {"msg": "ok"}

@app.delete("/trades/{id}")
def delete_trade(id: int):
    cursor.execute("DELETE FROM trades WHERE id=?", (id,))
    conn.commit()
    return {"ok": True}