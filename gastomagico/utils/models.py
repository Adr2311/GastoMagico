# utils/models.py

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from utils.database import Base
from typing import Any

class Categoria(Base):
    """
    Modelo para las categorías de gastos.
    """
    __tablename__ = 'categorias'

    id: int = Column(Integer, primary_key=True)
    nombre: str = Column(String, unique=True, nullable=False)
    created_at: Any = Column(DateTime(timezone=True), server_default=func.now())
    updated_at: Any = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self) -> str:
        return f"<Categoria(nombre='{self.nombre}')>"

class MetodoPago(Base):
    """
    Modelo para los métodos de pago.
    """
    __tablename__ = 'metodos_pago'

    id: int = Column(Integer, primary_key=True)
    nombre: str = Column(String, unique=True, nullable=False)
    created_at: Any = Column(DateTime(timezone=True), server_default=func.now())
    updated_at: Any = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self) -> str:
        return f"<MetodoPago(nombre='{self.nombre}')>"

class Gasto(Base):
    """
    Modelo para los gastos.
    """
    __tablename__ = 'gastos'

    id: int = Column(Integer, primary_key=True)
    descripcion: str = Column(String, nullable=False)
    monto: float = Column(Float, nullable=False)
    categoria_id: int = Column(Integer, ForeignKey('categorias.id'))
    metodo_pago_id: int = Column(Integer, ForeignKey('metodos_pago.id'))
    created_at: Any = Column(DateTime(timezone=True), server_default=func.now())
    updated_at: Any = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones con otras tablas
    categoria = relationship('Categoria')
    metodo_pago = relationship('MetodoPago')

    def __repr__(self) -> str:
        return f"<Gasto(descripcion='{self.descripcion}', monto={self.monto})>"

class Frase(Base):
    """
    Modelo para las frases motivacionales.
    """
    __tablename__ = 'frases'

    id: int = Column(Integer, primary_key=True)
    texto: str = Column(String, nullable=False)
    created_at: Any = Column(DateTime(timezone=True), server_default=func.now())
    updated_at: Any = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self) -> str:
        return f"<Frase(texto='{self.texto}')>"
