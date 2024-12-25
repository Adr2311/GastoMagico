# app.py

import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, joinedload
from datetime import datetime, date
import pandas as pd
import matplotlib.pyplot as plt
import random
import os
import io

# Configuración de la Base de Datos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'gasto_magico.db')}"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Definición de Modelos
class Categoria(Base):
    __tablename__ = 'categorias'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    gastos = relationship("Gasto", back_populates="categoria")

    def __repr__(self):
        return f"<Categoria(id={self.id}, nombre='{self.nombre}')>"


class MetodoPago(Base):
    __tablename__ = 'metodos_pago'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    gastos = relationship("Gasto", back_populates="metodo_pago")

    def __repr__(self):
        return f"<MetodoPago(id={self.id}, nombre='{self.nombre}')>"


class Gasto(Base):
    __tablename__ = 'gastos'

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime, default=datetime.utcnow)
    monto = Column(Float, nullable=False)
    descripcion = Column(String, nullable=False)
    categoria_id = Column(Integer, ForeignKey('categorias.id'))
    metodo_pago_id = Column(Integer, ForeignKey('metodos_pago.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    categoria = relationship("Categoria", back_populates="gastos")
    metodo_pago = relationship("MetodoPago", back_populates="gastos")

    def __repr__(self):
        return f"<Gasto(id={self.id}, monto={self.monto}, descripcion='{self.descripcion}')>"


class FraseMotivacional(Base):
    __tablename__ = 'frases_motivacionales'

    id = Column(Integer, primary_key=True, index=True)
    texto = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<FraseMotivacional(id={self.id}, texto='{self.texto}')>"


class Configuracion(Base):
    __tablename__ = 'configuraciones'

    id = Column(Integer, primary_key=True, index=True)
    limite_gasto = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Configuracion(id={self.id}, limite_gasto={self.limite_gasto})>"


# Inicialización de la Base de Datos
def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Insertar categorías de ejemplo
        if not db.query(Categoria).first():
            categorias = [
                Categoria(nombre="Alimentación"),
                Categoria(nombre="Transporte"),
                Categoria(nombre="Entretenimiento"),
                Categoria(nombre="Salud"),
                Categoria(nombre="Educación")
            ]
            db.add_all(categorias)
            db.commit()

        # Insertar métodos de pago de ejemplo
        if not db.query(MetodoPago).first():
            metodos_pago = [
                MetodoPago(nombre="Efectivo"),
                MetodoPago(nombre="Tarjeta de Crédito"),
                MetodoPago(nombre="Tarjeta de Débito"),
                MetodoPago(nombre="Transferencia Bancaria")
            ]
            db.add_all(metodos_pago)
            db.commit()

        # Insertar frases motivacionales de ejemplo
        if not db.query(FraseMotivacional).first():
            frases = [
                FraseMotivacional(texto="El éxito es la suma de pequeños esfuerzos repetidos día tras día."),
                FraseMotivacional(texto="No cuentes los días, haz que los días cuenten."),
                FraseMotivacional(texto="La mejor manera de predecir el futuro es creándolo."),
                FraseMotivacional(texto="No dejes para mañana lo que puedes hacer hoy."),
                FraseMotivacional(
                    texto="El único lugar donde el éxito viene antes que el trabajo es en el diccionario.")
            ]
            db.add_all(frases)
            db.commit()

        # Insertar configuración de ejemplo
        if not db.query(Configuracion).first():
            configuracion = Configuracion(limite_gasto=500.0)
            db.add(configuracion)
            db.commit()

        # Insertar gastos de ejemplo
        if not db.query(Gasto).first():
            # Obtener IDs de categorías y métodos de pago
            categoria_alimentacion = db.query(Categoria).filter(Categoria.nombre == "Alimentación").first()
            categoria_transporte = db.query(Categoria).filter(Categoria.nombre == "Transporte").first()
            categoria_entretenimiento = db.query(Categoria).filter(Categoria.nombre == "Entretenimiento").first()
            metodo_efectivo = db.query(MetodoPago).filter(MetodoPago.nombre == "Efectivo").first()
            metodo_tarjeta_credito = db.query(MetodoPago).filter(MetodoPago.nombre == "Tarjeta de Crédito").first()

            gastos = [
                Gasto(descripcion="Compra de comestibles", monto=50.75, categoria_id=categoria_alimentacion.id,
                      metodo_pago_id=metodo_efectivo.id),
                Gasto(descripcion="Pasaje de autobús", monto=2.50, categoria_id=categoria_transporte.id,
                      metodo_pago_id=metodo_tarjeta_credito.id),
                Gasto(descripcion="Cena en restaurante", monto=30.00, categoria_id=categoria_alimentacion.id,
                      metodo_pago_id=metodo_tarjeta_credito.id),
                Gasto(descripcion="Entrada al cine", monto=12.00, categoria_id=categoria_entretenimiento.id,
                      metodo_pago_id=metodo_efectivo.id),
            ]
            db.add_all(gastos)
            db.commit()

    except Exception as e:
        db.rollback()
        print(f"Error al inicializar la base de datos: {e}")
    finally:
        db.close()


# Casos de Uso
class TablaUseCase:
    @staticmethod
    def agregar_categoria(nombre: str) -> None:
        db = SessionLocal()
        try:
            categoria = Categoria(nombre=nombre)
            db.add(categoria)
            db.commit()
            db.refresh(categoria)
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    @staticmethod
    def listar_categorias():
        db = SessionLocal()
        try:
            return db.query(Categoria).all()
        finally:
            db.close()

    @staticmethod
    def eliminar_categoria(id_categoria: int) -> None:
        db = SessionLocal()
        try:
            categoria = db.query(Categoria).filter(Categoria.id == id_categoria).first()
            if not categoria:
                raise ValueError("Categoría no encontrada.")
            db.delete(categoria)
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    @staticmethod
    def agregar_metodo_pago(nombre: str) -> None:
        db = SessionLocal()
        try:
            metodo_pago = MetodoPago(nombre=nombre)
            db.add(metodo_pago)
            db.commit()
            db.refresh(metodo_pago)
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    @staticmethod
    def listar_metodos_pago():
        db = SessionLocal()
        try:
            return db.query(MetodoPago).all()
        finally:
            db.close()

    @staticmethod
    def eliminar_metodo_pago(id_metodo: int) -> None:
        db = SessionLocal()
        try:
            metodo_pago = db.query(MetodoPago).filter(MetodoPago.id == id_metodo).first()
            if not metodo_pago:
                raise ValueError("Método de pago no encontrado.")
            db.delete(metodo_pago)
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    @staticmethod
    def agregar_frase(texto: str) -> None:
        db = SessionLocal()
        try:
            frase = FraseMotivacional(texto=texto)
            db.add(frase)
            db.commit()
            db.refresh(frase)
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    @staticmethod
    def listar_frases():
        db = SessionLocal()
        try:
            return db.query(FraseMotivacional).all()
        finally:
            db.close()


class GastoUseCase:
    @staticmethod
    def agregar_gasto(descripcion: str, monto: float, categoria_id: int, metodo_pago_id: int, fecha=None) -> None:
        db = SessionLocal()
        try:
            gasto = Gasto(
                descripcion=descripcion,
                monto=monto,
                categoria_id=categoria_id,
                metodo_pago_id=metodo_pago_id,
                fecha=fecha
            )
            db.add(gasto)
            db.commit()
            db.refresh(gasto)
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    @staticmethod
    def listar_gastos():
        db = SessionLocal()
        try:
            return db.query(Gasto).options(
                joinedload(Gasto.categoria),
                joinedload(Gasto.metodo_pago)
            ).all()
        finally:
            db.close()

    @staticmethod
    def eliminar_gasto(id_gasto: int) -> None:
        db = SessionLocal()
        try:
            gasto = db.query(Gasto).filter(Gasto.id == id_gasto).first()
            if not gasto:
                raise ValueError("Gasto no encontrado.")
            db.delete(gasto)
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    @staticmethod
    def actualizar_gasto(id_gasto: int, descripcion: str, monto: float, categoria_id: int, metodo_pago_id: int,
                         fecha=None) -> None:
        db = SessionLocal()
        try:
            gasto = db.query(Gasto).filter(Gasto.id == id_gasto).first()
            if not gasto:
                raise ValueError("Gasto no encontrado.")
            gasto.descripcion = descripcion
            gasto.monto = monto
            gasto.categoria_id = categoria_id
            gasto.metodo_pago_id = metodo_pago_id
            gasto.fecha = fecha
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    @staticmethod
    def filtrar_gastos(fecha_desde, fecha_hasta, categoria, metodo_pago):
        db = SessionLocal()
        try:
            query = db.query(Gasto).join(Categoria).join(MetodoPago)
            if categoria != "Todas":
                query = query.filter(Categoria.nombre == categoria)
            if metodo_pago != "Todos":
                query = query.filter(MetodoPago.nombre == metodo_pago)
            if fecha_desde and fecha_hasta:
                query = query.filter(Gasto.fecha >= fecha_desde, Gasto.fecha <= fecha_hasta)
            return query.all()
        finally:
            db.close()


class ReporteUseCase:
    @staticmethod
    def generar_reporte_excel() -> bytes:
        db = SessionLocal()
        try:
            gastos = db.query(Gasto).all()
            data = [{
                'ID': gasto.id,
                'Fecha': gasto.fecha.strftime("%Y-%m-%d %H:%M:%S") if gasto.fecha else "",
                'Monto': gasto.monto,
                'Descripción': gasto.descripcion,
                'Categoría': gasto.categoria.nombre if gasto.categoria else "",
                'Método de Pago': gasto.metodo_pago.nombre if gasto.metodo_pago else ""
            } for gasto in gastos]
            df = pd.DataFrame(data)
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Gastos')
            processed_data = output.getvalue()
            return processed_data
        except Exception as e:
            raise e
        finally:
            db.close()

    @staticmethod
    def importar_reporte_excel(file) -> None:
        db = SessionLocal()
        try:
            df = pd.read_excel(file)
            for _, row in df.iterrows():
                categoria = db.query(Categoria).filter(Categoria.nombre == row['Categoría']).first()
                metodo_pago = db.query(MetodoPago).filter(MetodoPago.nombre == row['Método de Pago']).first()
                if not categoria or not metodo_pago:
                    st.warning(
                        f"Categoría o método de pago no encontrados para la fila con descripción '{row['Descripción']}'.")
                    continue
                fecha = datetime.strptime(row['Fecha'], "%Y-%m-%d %H:%M:%S") if pd.notna(
                    row['Fecha']) else datetime.utcnow()
                gasto = Gasto(
                    descripcion=row['Descripción'],
                    monto=row['Monto'],
                    categoria_id=categoria.id,
                    metodo_pago_id=metodo_pago.id,
                    fecha=fecha
                )
                db.add(gasto)
            db.commit()
            st.success("Reporte importado correctamente.")
        except Exception as e:
            db.rollback()
            st.error(f"Error al importar el reporte: {e}")
            raise e
        finally:
            db.close()

    @staticmethod
    def gastos_mensuales():
        db = SessionLocal()
        try:
            resumen = db.query(
                func.strftime('%Y-%m', Gasto.fecha).label('mes'),
                func.sum(Gasto.monto).label('monto_total')
            ).group_by('mes').all()
            return {mes: monto for mes, monto in resumen}
        finally:
            db.close()

    @staticmethod
    def dia_menor_gasto():
        db = SessionLocal()
        try:
            resumen = db.query(
                func.strftime('%Y-%m-%d', Gasto.fecha).label('dia'),
                func.sum(Gasto.monto).label('monto_total')
            ).group_by('dia').order_by('monto_total').first()
            return resumen.dia if resumen else None
        finally:
            db.close()

    @staticmethod
    def establecer_limite_gasto(limite: float) -> None:
        db = SessionLocal()
        try:
            configuracion = db.query(Configuracion).first()
            if configuracion:
                configuracion.limite_gasto = limite
            else:
                configuracion = Configuracion(limite_gasto=limite)
                db.add(configuracion)
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()


# Controladores
class TablaController:
    @staticmethod
    def agregar_categoria(nombre: str) -> None:
        TablaUseCase.agregar_categoria(nombre)

    @staticmethod
    def listar_categorias():
        return TablaUseCase.listar_categorias()

    @staticmethod
    def eliminar_categoria(id_categoria: int) -> None:
        TablaUseCase.eliminar_categoria(id_categoria)

    @staticmethod
    def agregar_metodo_pago(nombre: str) -> None:
        TablaUseCase.agregar_metodo_pago(nombre)

    @staticmethod
    def listar_metodos_pago():
        return TablaUseCase.listar_metodos_pago()

    @staticmethod
    def eliminar_metodo_pago(id_metodo: int) -> None:
        TablaUseCase.eliminar_metodo_pago(id_metodo)

    @staticmethod
    def agregar_frase(texto: str) -> None:
        TablaUseCase.agregar_frase(texto)

    @staticmethod
    def listar_frases():
        return TablaUseCase.listar_frases()


class GastoController:
    @staticmethod
    def agregar_gasto(descripcion: str, monto: float, categoria_id: int, metodo_pago_id: int, fecha=None) -> None:
        GastoUseCase.agregar_gasto(descripcion, monto, categoria_id, metodo_pago_id, fecha)

    @staticmethod
    def listar_gastos():
        return GastoUseCase.listar_gastos()

    @staticmethod
    def eliminar_gasto(id_gasto: int) -> None:
        GastoUseCase.eliminar_gasto(id_gasto)

    @staticmethod
    def actualizar_gasto(id_gasto: int, descripcion: str, monto: float, categoria_id: int, metodo_pago_id: int,
                         fecha=None) -> None:
        GastoUseCase.actualizar_gasto(id_gasto, descripcion, monto, categoria_id, metodo_pago_id, fecha)

    @staticmethod
    def filtrar_gastos(fecha_desde, fecha_hasta, categoria, metodo_pago):
        return GastoUseCase.filtrar_gastos(fecha_desde, fecha_hasta, categoria, metodo_pago)


class ReporteController:
    @staticmethod
    def exportar_reporte_excel() -> bytes:
        return ReporteUseCase.generar_reporte_excel()

    @staticmethod
    def importar_reporte_excel(file) -> None:
        ReporteUseCase.importar_reporte_excel(file)

    @staticmethod
    def gastos_mensuales():
        return ReporteUseCase.gastos_mensuales()

    @staticmethod
    def dia_menor_gasto():
        return ReporteUseCase.dia_menor_gasto()

    @staticmethod
    def establecer_limite_gasto(limite: float) -> None:
        ReporteUseCase.establecer_limite_gasto(limite)


# Utilidades
def mostrar_frase_motivacional(frase):
    return frase


# Inicializar la Base de Datos al inicio
init_db()

# Configuración de la Aplicación
st.set_page_config(page_title="💰 GastoMágico", layout="wide", page_icon="💰")


# Estilos CSS personalizados para el tema oscuro y acentos verdes
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


# Estilos CSS en línea
st.markdown("""
    <style>
        body {
            background-color: #121212;
            color: #ffffff;
        }
        .css-1d391kg {
            background-color: #1e1e1e;
        }
        .css-1aumxhk {
            background-color: #2c2c2c;
        }
        .css-1y4p8pa {
            color: #27ae60;
        }
        .css-1q8dd3e {
            background-color: #27ae60;
            color: #121212;
        }
        .css-1q8dd3e:hover {
            background-color: #2ecc71;
        }
        .css-1y4p8pa:hover {
            color: #2ecc71;
        }
        table {
            background-color: #1e1e1e;
            color: #ffffff;
        }
        th {
            background-color: #27ae60;
            color: #121212;
        }
        tr:nth-child(even) {
            background-color: #2c2c2c;
        }
        tr:hover {
            background-color: #27ae60;
            color: #121212;
        }
        .stButton>button {
            background-color: #27ae60;
            color: #121212;
            border: none;
            padding: 8px 16px;
            border-radius: 5px;
            font-size: 13px;
            min-width: 100px;
            height: 35px;
        }
        .stButton>button:hover {
            background-color: #2ecc71;
        }
        .stButton>button#deleteButton {
            background-color: #e74c3c;
        }
        .stButton>button#deleteButton:hover {
            background-color: #c0392b;
        }
        .stButton>button#editButton {
            background-color: #2980b9;
        }
        .stButton>button#editButton:hover {
            background-color: #3498db;
        }
        .stButton>button#filterButton {
            background-color: #8e44ad;
        }
        .stButton>button#filterButton:hover {
            background-color: #9b59b6;
        }
        .banner {
            background-color: #1a1a1a;
            border-top: 2px solid #27ae60;
            padding: 10px;
            text-align: center;
            color: #27ae60;
            font-size: 16px;
        }
    
    </style>
""", unsafe_allow_html=True)


# Banner Inferior
def display_banner():
    st.markdown("""
        <div class="banner">
            💰 GastoMágico - Control de Gastos Personal
        </div>
    """, unsafe_allow_html=True)


# Función para obtener una frase motivacional aleatoria
def get_random_frase():
    frases = TablaController.listar_frases()
    if frases:
        return random.choice(frases).texto
    return "¡Bienvenido a GastoMágico!"


# Interfaz de Usuario
def main():
    st.title("💰 GastoMágico - Control de Gastos Personal")

    # Frase Motivacional
    frase = get_random_frase()
    st.sidebar.markdown(f"## 💡 {frase}")

    # Navegación por pestañas
    pestañas = ["💰 Gastos", "🏷️ Categorías", "💳 Métodos de Pago", "📈 Reportes"]
    seleccion = st.sidebar.radio("Navegación", pestañas)

    if seleccion == "💰 Gastos":
        gastos_tab()
    elif seleccion == "🏷️ Categorías":
        categorias_tab()
    elif seleccion == "💳 Métodos de Pago":
        metodos_pago_tab()
    elif seleccion == "📈 Reportes":
        reportes_tab()

    # Banner Inferior
    display_banner()


def gastos_tab():
    st.header("📊 Registro de Gastos")

    # Formulario para agregar gasto
    with st.form(key='agregar_gasto'):
        col1, col2 = st.columns(2)
        with col1:
            fecha = st.date_input("📅 Fecha", value=date.today())
            categoria = st.selectbox("🏷️ Categoría", [cat.nombre for cat in TablaController.listar_categorias()])
            metodo_pago = st.selectbox("💳 Método de Pago",
                                       [met.nombre for met in TablaController.listar_metodos_pago()])
        with col2:
            monto = st.number_input("💵 Monto ($)", min_value=0.0, step=0.01)
            descripcion = st.text_input("📝 Descripción")

        submit_button = st.form_submit_button(label='➕ Agregar Gasto')

        if submit_button:
            if descripcion and monto > 0:
                # Obtener IDs de categoría y método de pago
                categorias = TablaController.listar_categorias()
                categorias_dict = {cat.nombre: cat.id for cat in categorias}
                metodos = TablaController.listar_metodos_pago()
                metodos_dict = {met.nombre: met.id for met in metodos}

                categoria_id = categorias_dict.get(categoria)
                metodo_pago_id = metodos_dict.get(metodo_pago)

                GastoController.agregar_gasto(
                    descripcion=descripcion,
                    monto=monto,
                    categoria_id=categoria_id,
                    metodo_pago_id=metodo_pago_id,
                    fecha=fecha
                )
                st.success("Gasto agregado correctamente.")
            else:
                st.error("Por favor, complete todos los campos correctamente.")

    st.markdown("---")

    # Opciones para editar y eliminar
    st.subheader("Lista de Gastos")
    gastos = GastoController.listar_gastos()
    if gastos:
        df_gastos = pd.DataFrame([{
            'ID': gasto.id,
            'Fecha': gasto.fecha.strftime("%Y-%m-%d") if gasto.fecha else "",
            'Monto': gasto.monto,
            'Descripción': gasto.descripcion,
            'Categoría': gasto.categoria.nombre if gasto.categoria else "N/A",
            'Método de Pago': gasto.metodo_pago.nombre if gasto.metodo_pago else "N/A"
        } for gasto in gastos])

        st.dataframe(df_gastos, use_container_width=True)

        # Botones para editar y eliminar
        with st.expander("Acciones"):
            id_seleccionado = st.selectbox("Seleccione el ID del gasto para editar/eliminar", df_gastos['ID'])
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✏️ Editar Gasto"):
                    editar_gasto(id_seleccionado)
            with col2:
                if st.button("🗑️ Eliminar Gasto"):
                    eliminar_gasto(id_seleccionado)
    else:
        st.info("No hay gastos registrados.")


def editar_gasto(id_gasto):
    gastos = GastoController.listar_gastos()
    gasto = next((g for g in gastos if g.id == id_gasto), None)
    if gasto:
        st.subheader("Editar Gasto")

        with st.form(key='editar_gasto'):
            col1, col2 = st.columns(2)
            with col1:
                fecha = st.date_input("📅 Fecha", value=gasto.fecha.date() if gasto.fecha else date.today())
                categorias = TablaController.listar_categorias()
                categorias_nombres = [cat.nombre for cat in categorias]
                if gasto.categoria:
                    index_categoria = categorias_nombres.index(gasto.categoria.nombre)
                else:
                    index_categoria = 0
                categoria = st.selectbox("🏷️ Categoría", categorias_nombres, index=index_categoria)

                metodos = TablaController.listar_metodos_pago()
                metodos_nombres = [met.nombre for met in metodos]
                if gasto.metodo_pago:
                    index_metodo = metodos_nombres.index(gasto.metodo_pago.nombre)
                else:
                    index_metodo = 0
                metodo_pago = st.selectbox("💳 Método de Pago", metodos_nombres, index=index_metodo)
            with col2:
                monto = st.number_input("💵 Monto ($)", min_value=0.0, step=0.01, value=gasto.monto)
                descripcion = st.text_input("📝 Descripción", value=gasto.descripcion)

            submit_button = st.form_submit_button(label='✅ Guardar Cambios')

            if submit_button:
                if descripcion and monto > 0:
                    # Obtener IDs de categoría y método de pago
                    categoria_id = next(cat.id for cat in categorias if cat.nombre == categoria)
                    metodo_pago_id = next(met.id for met in metodos if met.nombre == metodo_pago)

                    GastoController.actualizar_gasto(
                        id_gasto=id_gasto,
                        descripcion=descripcion,
                        monto=monto,
                        categoria_id=categoria_id,
                        metodo_pago_id=metodo_pago_id,
                        fecha=fecha
                    )
                    st.success("Gasto actualizado correctamente.")
                else:
                    st.error("Por favor, complete todos los campos correctamente.")
    else:
        st.error("Gasto no encontrado.")


def eliminar_gasto(id_gasto):
    confirm = st.checkbox("¿Está seguro de eliminar este gasto?")
    if confirm:
        try:
            GastoController.eliminar_gasto(id_gasto)
            st.success("Gasto eliminado correctamente.")
        except Exception as e:
            st.error(f"Error al eliminar el gasto: {e}")


def categorias_tab():
    st.header("🏷️ Gestión de Categorías")

    # Formulario para agregar categoría
    with st.form(key='agregar_categoria'):
        nombre = st.text_input("Nombre de la nueva categoría")
        submit_button = st.form_submit_button(label='➕ Agregar Categoría')

        if submit_button:
            if nombre:
                try:
                    TablaController.agregar_categoria(nombre)
                    st.success("Categoría agregada correctamente.")
                except Exception as e:
                    st.error(f"Error al agregar categoría: {e}")
            else:
                st.error("Por favor, ingrese un nombre para la categoría.")

    st.markdown("---")

    # Lista de categorías
    st.subheader("Lista de Categorías")
    categorias = TablaController.listar_categorias()
    if categorias:
        df_categorias = pd.DataFrame([{
            'ID': cat.id,
            'Nombre': cat.nombre
        } for cat in categorias])
        st.dataframe(df_categorias, use_container_width=True)

        # Botón para eliminar categoría
        id_seleccionado = st.selectbox("Seleccione el ID de la categoría para eliminar", df_categorias['ID'])
        if st.button("🗑️ Eliminar Categoría"):
            confirm = st.checkbox("¿Está seguro de eliminar esta categoría? (Se eliminarán todos los gastos asociados)")
            if confirm:
                try:
                    TablaController.eliminar_categoria(id_seleccionado)
                    st.success("Categoría eliminada correctamente.")
                except Exception as e:
                    st.error(f"Error al eliminar categoría: {e}")
    else:
        st.info("No hay categorías registradas.")


def metodos_pago_tab():
    st.header("💳 Gestión de Métodos de Pago")

    # Formulario para agregar método de pago
    with st.form(key='agregar_metodo_pago'):
        nombre = st.text_input("Nombre del nuevo método de pago")
        submit_button = st.form_submit_button(label='➕ Agregar Método')

        if submit_button:
            if nombre:
                try:
                    TablaController.agregar_metodo_pago(nombre)
                    st.success("Método de pago agregado correctamente.")
                except Exception as e:
                    st.error(f"Error al agregar método de pago: {e}")
            else:
                st.error("Por favor, ingrese un nombre para el método de pago.")

    st.markdown("---")

    # Lista de métodos de pago
    st.subheader("Lista de Métodos de Pago")
    metodos = TablaController.listar_metodos_pago()
    if metodos:
        df_metodos = pd.DataFrame([{
            'ID': met.id,
            'Nombre': met.nombre
        } for met in metodos])
        st.dataframe(df_metodos, use_container_width=True)

        # Botón para eliminar método de pago
        id_seleccionado = st.selectbox("Seleccione el ID del método de pago para eliminar", df_metodos['ID'])
        if st.button("🗑️ Eliminar Método de Pago"):
            confirm = st.checkbox(
                "¿Está seguro de eliminar este método de pago? (Se eliminarán todos los gastos asociados)")
            if confirm:
                try:
                    TablaController.eliminar_metodo_pago(id_seleccionado)
                    st.success("Método de pago eliminado correctamente.")
                except Exception as e:
                    st.error(f"Error al eliminar método de pago: {e}")
    else:
        st.info("No hay métodos de pago registrados.")


def reportes_tab():
    st.header("📈 Reportes y Configuración")

    # Opciones de Reportes
    st.subheader("Generar Reportes")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Exportar a Excel"):
            reporte = ReporteController.exportar_reporte_excel()
            st.download_button(
                label="✅ Descargar Reporte Excel",
                data=reporte,
                file_name='reporte_gastos.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
    with col2:
        if st.button("📥 Importar desde Excel"):
            file = st.file_uploader("Selecciona el archivo Excel", type=["xlsx"])
            if file:
                try:
                    ReporteController.importar_reporte_excel(file)
                except Exception as e:
                    st.error(f"Error al importar reporte: {e}")

    st.markdown("---")

    # Reportes Personalizados
    st.subheader("Reportes Personalizados")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 Gastos Mensuales"):
            gastos_mensuales = ReporteController.gastos_mensuales()
            if gastos_mensuales:
                meses = sorted(gastos_mensuales.keys())
                montos = [gastos_mensuales[mes] for mes in meses]

                fig, ax = plt.subplots()
                ax.bar(meses, montos, color='#27ae60')
                ax.set_title("Gastos Mensuales")
                ax.set_xlabel("Mes")
                ax.set_ylabel("Monto ($)")
                plt.xticks(rotation=45)
                st.pyplot(fig)
            else:
                st.info("No hay datos para mostrar.")

    with col2:
        if st.button("📊 Día con Menor Gasto"):
            dia_menor = ReporteController.dia_menor_gasto()
            if dia_menor:
                gastos = GastoUseCase.filtrar_gastos(
                    fecha_desde=datetime.strptime(dia_menor, "%Y-%m-%d").date(),
                    fecha_hasta=datetime.strptime(dia_menor, "%Y-%m-%d").date(),
                    categoria="Todas",
                    metodo_pago="Todos"
                )
                if gastos:
                    dias = [gasto.fecha.strftime("%Y-%m-%d") for gasto in gastos]
                    montos = [gasto.monto for gasto in gastos]

                    fig, ax = plt.subplots()
                    ax.bar(dias, montos, color='#e74c3c')
                    ax.set_title("Gasto por Día")
                    ax.set_xlabel("Día")
                    ax.set_ylabel("Monto ($)")
                    plt.xticks(rotation=45)
                    st.pyplot(fig)
                else:
                    st.info("No hay suficientes datos para mostrar.")
            else:
                st.info("No hay suficientes datos para mostrar.")

    st.markdown("---")

    # Configuración
    st.subheader("Configuración")

    configuracion = None
    db = SessionLocal()
    try:
        configuracion = db.query(Configuracion).first()
    finally:
        db.close()

    with st.form(key='configuracion'):
        limite_gasto = st.number_input("📉 Establecer Límite de Gasto ($)", min_value=0.0, step=0.01,
                                       value=configuracion.limite_gasto if configuracion else 0.0)
        submit_button = st.form_submit_button(label='✅ Establecer')

        if submit_button:
            try:
                ReporteController.establecer_limite_gasto(limite_gasto)
                st.success(f"Límite de gasto establecido en ${limite_gasto:.2f}")
            except Exception as e:
                st.error(f"Error al establecer límite de gasto: {e}")

    st.markdown("---")

    # Gráficos Automáticos
    st.subheader("Gráficos Automáticos")

    col1, col2 = st.columns(2)
    with col1:
        gastos_mensuales = ReporteController.gastos_mensuales()
        if gastos_mensuales:
            meses = sorted(gastos_mensuales.keys())
            montos = [gastos_mensuales[mes] for mes in meses]

            fig, ax = plt.subplots()
            ax.bar(meses, montos, color='#27ae60')
            ax.set_title("Gastos Mensuales")
            ax.set_xlabel("Mes")
            ax.set_ylabel("Monto ($)")
            plt.xticks(rotation=45)
            st.pyplot(fig)
        else:
            st.info("No hay datos para mostrar.")

    with col2:
        dia_menor = ReporteController.dia_menor_gasto()
        if dia_menor:
            gastos = GastoUseCase.filtrar_gastos(
                fecha_desde=datetime.strptime(dia_menor, "%Y-%m-%d").date(),
                fecha_hasta=datetime.strptime(dia_menor, "%Y-%m-%d").date(),
                categoria="Todas",
                metodo_pago="Todos"
            )
            if gastos:
                dias = [gasto.fecha.strftime("%Y-%m-%d") for gasto in gastos]
                montos = [gasto.monto for gasto in gastos]

                fig, ax = plt.subplots()
                ax.bar(dias, montos, color='#e74c3c')
                ax.set_title("Gasto por Día")
                ax.set_xlabel("Día")
                ax.set_ylabel("Monto ($)")
                plt.xticks(rotation=45)
                st.pyplot(fig)
            else:
                st.info("No hay suficientes datos para mostrar.")
        else:
            st.info("No hay suficientes datos para mostrar.")


# Ejecutar la Aplicación
if __name__ == "__main__":
    main()
