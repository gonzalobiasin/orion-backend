from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

DATABASE_URL = "sqlite:///./trades.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================= MODELO =================

class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    activo = Column(String)
    tipo = Column(String)
    resultado = Column(String)
    pnl = Column(Float)
    nota = Column(String)

Base.metadata.create_all(bind=engine)

# ================= SCHEMA =================

class TradeCreate(BaseModel):
    user_id: int
    activo: str
    tipo: str
    resultado: str
    pnl: float
    nota: str

# ================= DB =================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ================= LOGIN =================

@app.post("/login")
def login(data: dict):
    return {"user_id": 1}

# ================= TRADES =================

@app.get("/trades/{user_id}")
def get_trades(user_id: int, db: Session = Depends(get_db)):
    return db.query(Trade).filter(Trade.user_id == user_id).all()

@app.post("/trades")
def create_trade(trade: TradeCreate, db: Session = Depends(get_db)):
    db_trade = Trade(**trade.dict())
    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)
    return db_trade

@app.put("/trades/{trade_id}")
def update_trade(trade_id: int, trade: TradeCreate, db: Session = Depends(get_db)):
    db_trade = db.query(Trade).filter(Trade.id == trade_id).first()

    if not db_trade:
        return {"error": "No existe"}

    db_trade.activo = trade.activo
    db_trade.tipo = trade.tipo
    db_trade.resultado = trade.resultado
    db_trade.pnl = trade.pnl
    db_trade.nota = trade.nota

    db.commit()
    db.refresh(db_trade)

    return db_trade

@app.delete("/trades/{trade_id}")
def delete_trade(trade_id: int, db: Session = Depends(get_db)):
    db_trade = db.query(Trade).filter(Trade.id == trade_id).first()

    if not db_trade:
        return {"error": "No existe"}

    db.delete(db_trade)
    db.commit()

    return {"ok": True}