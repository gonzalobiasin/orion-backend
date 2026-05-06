from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DATABASE
conn = sqlite3.connect("db.db", check_same_thread=False)
cursor = conn.cursor()

# USERS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    password TEXT
)
""")

# TRADES TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS trades (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER,

    activo TEXT,
    tipo TEXT,
    mercado TEXT,

    estado TEXT,

    capital REAL,
    apalancamiento REAL,

    tp REAL,
    sl REAL,
    be REAL,

    riesgo REAL,
    rr REAL,

    pnl REAL,
    porcentaje REAL,

    timeframe TEXT,
    sesion TEXT,

    notas TEXT,
    screenshot TEXT,

    fecha TEXT,
    hora TEXT
)
""")

conn.commit()

# ======================================================
# MODELS
# ======================================================

class User(BaseModel):
    email: str
    password: str

class Trade(BaseModel):

    user_id: int

    activo: str
    tipo: str
    mercado: str

    estado: str

    capital: float
    apalancamiento: float

    tp: float
    sl: float
    be: float

    riesgo: float = 0
    rr: float = 0

    pnl: float
    porcentaje: float

    timeframe: str
    sesion: str

    notas: str = ""
    screenshot: str = ""

    fecha: str
    hora: str

# ======================================================
# REGISTER
# ======================================================

@app.post("/register")
def register(user: User):

    try:

        cursor.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)",
            (user.email, user.password)
        )

        conn.commit()

        return {
            "msg": "ok"
        }

    except:

        raise HTTPException(
            status_code=400,
            detail="Usuario ya existe"
        )

# ======================================================
# LOGIN
# ======================================================

@app.post("/login")
def login(user: User):

    cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (user.email, user.password)
    )

    data = cursor.fetchone()

    if not data:

        raise HTTPException(
            status_code=401,
            detail="Login incorrecto"
        )

    return {
        "user_id": data[0]
    }

# ======================================================
# GET TRADES
# ======================================================

@app.get("/trades/{user_id}")
def get_trades(user_id: int):

    cursor.execute(
        "SELECT * FROM trades WHERE user_id=? ORDER BY id DESC",
        (user_id,)
    )

    rows = cursor.fetchall()

    result = []

    for r in rows:

        result.append({

            "id": r[0],
            "user_id": r[1],

            "activo": r[2],
            "tipo": r[3],
            "mercado": r[4],

            "estado": r[5],

            "capital": r[6],
            "apalancamiento": r[7],

            "tp": r[8],
            "sl": r[9],
            "be": r[10],

            "riesgo": r[11],
            "rr": r[12],

            "pnl": r[13],
            "porcentaje": r[14],

            "timeframe": r[15],
            "sesion": r[16],

            "notas": r[17],
            "screenshot": r[18],

            "fecha": r[19],
            "hora": r[20]
        })

    return result

# ======================================================
# CREATE TRADE
# ======================================================

@app.post("/trades")
def create_trade(t: Trade):

    cursor.execute("""
    INSERT INTO trades (

        user_id,

        activo,
        tipo,
        mercado,

        estado,

        capital,
        apalancamiento,

        tp,
        sl,
        be,

        riesgo,
        rr,

        pnl,
        porcentaje,

        timeframe,
        sesion,

        notas,
        screenshot,

        fecha,
        hora

    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (

        t.user_id,

        t.activo,
        t.tipo,
        t.mercado,

        t.estado,

        t.capital,
        t.apalancamiento,

        t.tp,
        t.sl,
        t.be,

        t.riesgo,
        t.rr,

        t.pnl,
        t.porcentaje,

        t.timeframe,
        t.sesion,

        t.notas,
        t.screenshot,

        t.fecha,
        t.hora
    ))

    conn.commit()

    return {
        "msg": "ok"
    }

# ======================================================
# UPDATE TRADE
# ======================================================

@app.put("/trades/{id}")
def update_trade(id: int, t: Trade):

    cursor.execute("""
    UPDATE trades SET

        activo=?,
        tipo=?,
        mercado=?,

        estado=?,

        capital=?,
        apalancamiento=?,

        tp=?,
        sl=?,
        be=?,

        riesgo=?,
        rr=?,

        pnl=?,
        porcentaje=?,

        timeframe=?,
        sesion=?,

        notas=?,
        screenshot=?,

        fecha=?,
        hora=?

    WHERE id=?
    """, (

        t.activo,
        t.tipo,
        t.mercado,

        t.estado,

        t.capital,
        t.apalancamiento,

        t.tp,
        t.sl,
        t.be,

        t.riesgo,
        t.rr,

        t.pnl,
        t.porcentaje,

        t.timeframe,
        t.sesion,

        t.notas,
        t.screenshot,

        t.fecha,
        t.hora,

        id
    ))

    conn.commit()

    return {
        "msg": "updated"
    }

# ======================================================
# DELETE TRADE
# ======================================================

@app.delete("/trades/{id}")
def delete_trade(id: int):

    cursor.execute(
        "DELETE FROM trades WHERE id=?",
        (id,)
    )

    conn.commit()

    return {
        "ok": True
    }