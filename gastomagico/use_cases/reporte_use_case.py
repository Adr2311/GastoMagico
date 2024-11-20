# use_cases/reporte_use_case.py

import pandas as pd
from typing import List, Dict, Optional
from utils.database import session
from utils.models import Gasto
from datetime import datetime


class ReporteUseCase:
    @staticmethod
    def generar_reporte_excel(filepath: str) -> None:
        gastos = session.query(Gasto).all()
        data = [{
            "ID": gasto.id,
            "Descripción": gasto.descripcion,
            "Monto": gasto.monto,
            "Categoría": gasto.categoria.nombre if gasto.categoria else "N/A",
            "Método de Pago": gasto.metodo_pago.nombre if gasto.metodo_pago else "N/A",
            "Fecha de Creación": gasto.created_at.strftime("%Y-%m-%d %H:%M:%S") if gasto.created_at else "N/A"
        } for gasto in gastos]
        df = pd.DataFrame(data)
        df.to_excel(filepath, index=False)

    @staticmethod
    def importar_reporte_excel(filepath: str) -> None:
        df = pd.read_excel(filepath)
        for _, row in df.iterrows():
            descripcion = row.get("Descripción", "")
            monto = row.get("Monto", 0.0)
            categoria_nombre = row.get("Categoría", "")
            metodo_pago_nombre = row.get("Método de Pago", "")

            categoria = session.query(Categoria).filter_by(nombre=categoria_nombre).first()
            metodo_pago = session.query(MetodoPago).filter_by(nombre=metodo_pago_nombre).first()

            if not categoria or not metodo_pago:
                continue  # Saltar si la categoría o método de pago no existe

            gasto = Gasto(
                descripcion=descripcion,
                monto=monto,
                categoria_id=categoria.id,
                metodo_pago_id=metodo_pago.id,
                created_at=row.get("Fecha de Creación", datetime.utcnow())
            )
            session.add(gasto)
        session.commit()

    @staticmethod
    def gastos_mensuales() -> Dict[str, float]:
        gastos = session.query(Gasto).filter(Gasto.created_at.isnot(None)).all()
        data = [{
            "mes": gasto.created_at.strftime("%Y-%m"),
            "monto": gasto.monto
        } for gasto in gastos]
        df = pd.DataFrame(data)
        if df.empty:
            return {}
        resumen = df.groupby("mes")["monto"].sum().to_dict()
        return resumen

    @staticmethod
    def dia_menor_gasto() -> Optional[str]:
        gastos = session.query(Gasto).filter(Gasto.created_at.isnot(None)).all()
        data = [{
            "dia": gasto.created_at.strftime("%Y-%m-%d"),
            "monto": gasto.monto
        } for gasto in gastos]
        df = pd.DataFrame(data)
        if df.empty:
            return None
        resumen = df.groupby("dia")["monto"].sum()
        dia_menor = resumen.idxmin()
        return dia_menor

    @staticmethod
    def establecer_limite_gasto(limite: float) -> None:
        # Puedes implementar esta función según tus necesidades, por ejemplo, guardar el límite en una configuración
        # Por simplicidad, se muestra un mensaje
        print(f"Límite de gasto establecido en: ${limite:.2f}")
