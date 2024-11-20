# use_cases/tabla_use_case.py

from typing import List
from utils.database import session
from utils.models import Categoria, MetodoPago, Frase
from utils.console import mostrar_frase_motivacional


class TablaUseCase:
    @staticmethod
    def agregar_categoria(nombre: str) -> None:
        if session.query(Categoria).filter_by(nombre=nombre).first():
            raise ValueError("La categoría ya existe.")
        categoria = Categoria(nombre=nombre)
        session.add(categoria)
        session.commit()
        mostrar_frase_motivacional()

    @staticmethod
    def listar_categorias() -> List[Categoria]:
        return session.query(Categoria).all()

    @staticmethod
    def eliminar_categoria(id_categoria: int) -> None:
        categoria = session.query(Categoria).filter_by(id=id_categoria).first()
        if not categoria:
            raise ValueError("Categoría no encontrada.")
        session.delete(categoria)
        session.commit()
        mostrar_frase_motivacional()

    @staticmethod
    def agregar_metodo_pago(nombre: str) -> None:
        if session.query(MetodoPago).filter_by(nombre=nombre).first():
            raise ValueError("El método de pago ya existe.")
        metodo_pago = MetodoPago(nombre=nombre)
        session.add(metodo_pago)
        session.commit()
        mostrar_frase_motivacional()

    @staticmethod
    def listar_metodos_pago() -> List[MetodoPago]:
        return session.query(MetodoPago).all()

    @staticmethod
    def eliminar_metodo_pago(id_metodo: int) -> None:
        metodo_pago = session.query(MetodoPago).filter_by(id=id_metodo).first()
        if not metodo_pago:
            raise ValueError("Método de pago no encontrado.")
        session.delete(metodo_pago)
        session.commit()
        mostrar_frase_motivacional()

    @staticmethod
    def agregar_frase(texto: str) -> None:
        frase = Frase(texto=texto)
        session.add(frase)
        session.commit()
        mostrar_frase_motivacional()

    @staticmethod
    def listar_frases() -> List[Frase]:
        return session.query(Frase).all()
