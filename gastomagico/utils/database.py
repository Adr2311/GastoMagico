# utils/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///gasto_magico.db"

engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

def init_db():
    from utils.models import Categoria, MetodoPago, Gasto, Frase
    Base.metadata.create_all(engine)
