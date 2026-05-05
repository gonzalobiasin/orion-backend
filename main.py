from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# permitir conexión con frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# base en memoria (simple)
trades = []
trade_id = 1

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/trades")
def get_trades():
    return trades

@app.post("/trades")
def create_trade(trade: dict):
    global trade_id

    trade["id"] = trade_id
    trade_id += 1

    trades.append(trade)
    return trade

@app.put("/trades/{id}")
def update_trade(id: int, updated: dict):
    for i, t in enumerate(trades):
        if t["id"] == id:
            trades[i] = {**t, **updated}
            return trades[i]
    return {"error": "not found"}

@app.delete("/trades/{id}")
def delete_trade(id: int):
    global trades
    trades = [t for t in trades if t["id"] != id]
    return {"ok": True}