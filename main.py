from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 🚀 HABILITAR CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # después lo hacemos más seguro
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- USERS ----------------

users = []

@app.post("/register")
def register(data: dict):
    for u in users:
        if u["email"] == data["email"]:
            return {"detail": "Usuario ya existe"}
    
    user = {
        "id": len(users) + 1,
        "email": data["email"],
        "password": data["password"]
    }
    users.append(user)
    return {"msg": "ok"}

@app.post("/login")
def login(data: dict):
    for u in users:
        if u["email"] == data["email"] and u["password"] == data["password"]:
            return {"user_id": u["id"]}
    
    return {"detail": "Credenciales incorrectas"}

# ---------------- TRADES ----------------

trades = []

@app.post("/trades")
def create_trade(data: dict):
    trade = {
        "id": len(trades) + 1,
        "user_id": data["user_id"],
        "activo": data["activo"],
        "tipo": data["tipo"],
        "resultado": data["resultado"]
    }
    trades.append(trade)
    return {"msg": "trade guardado"}

@app.get("/trades/{user_id}")
def get_trades(user_id: int):
    return [t for t in trades if t["user_id"] == user_id]

@app.get("/")
def root():
    return {"msg": "Orion backend funcionando 🚀"}