# use_cases/gasto_use_case.py

from typing import List
from utils.database import session
from utils.models import Gasto, Categoria, MetodoPago
from utils.console import mostrar_frase_motivacional


class GastoUseCase:
    @staticmethod
    def agregar_gasto(descripcion: str, monto: float, categoria_id: int, metodo_pago_id: int) -> None:
        categoria = session.query(Categoria).filter_by(id=categoria_id).first()
        metodo_pago = session.query(MetodoPago).filter_by(id=metodo_pago_id).first()

        if not categoria:
            raise ValueError("Categoría inválida.")
        if not metodo_pago:
            raise ValueError("Método de pago inválido.")

        gasto = Gasto(
            descripcion=descripcion,
            monto=monto,
            categoria_id=categoria_id,
            metodo_pago_id=metodo_pago_id
        )
        session.add(gasto)
        session.commit()
        mostrar_frase_motivacional()

    @staticmethod
    def listar_gastos() -> List[Gasto]:
        return session.query(Gasto).order_by(Gasto.created_at.desc()).all()

    @staticmethod
    def eliminar_gasto(id_gasto: int) -> None:
        gasto = session.query(Gasto).filter_by(id=id_gasto).first()
        if not gasto:
            raise ValueError("Gasto no encontrado.")
        session.delete(gasto)
        session.commit()
        mostrar_frase_motivacional()
