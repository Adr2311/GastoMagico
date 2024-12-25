# Copyright 2024 Abdiel Lopez
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     https://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/bin/bash

# Script para configurar la aplicación GastoMágico

# Salir inmediatamente si un comando falla
set -e

# Nombre del directorio del proyecto (todo en minúsculas para consistencia)
PROJECT_DIR="gastomagico"

# Crear el directorio del proyecto
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# Crear subdirectorios
mkdir -p controllers models use_cases utils

# Crear archivos __init__.py
touch models/__init__.py
touch use_cases/__init__.py
touch utils/__init__.py

# Crear utils/database.py
cat <<'EOF' > utils/database.py
# gastomagico/utils/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///gasto_magico.db"

# Crear el engine de la base de datos
engine = create_engine(DATABASE_URL, echo=True)  # Cambiar a False en producción

# Crear una fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa
Base = declarative_base()

def init_db():
    """
    Inicializa la base de datos creando todas las tablas definidas en los modelos.
    También inserta datos de ejemplo si las tablas están vacías.
    """
    # Importar todos los modelos para que SQLAlchemy los registre
    from gastomagico.models.categoria import Categoria
    from gastomagico.models.metodo_pago import MetodoPago
    from gastomagico.models.gasto import Gasto
    from gastomagico.models.frase_motivacional import FraseMotivacional
    from gastomagico.models.configuracion import Configuracion

    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)

    # Insertar datos de ejemplo si las tablas están vacías
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
                FraseMotivacional(texto="El único lugar donde el éxito viene antes que el trabajo es en el diccionario.")
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
                Gasto(descripcion="Compra de comestibles", monto=50.75, categoria_id=categoria_alimentacion.id, metodo_pago_id=metodo_efectivo.id),
                Gasto(descripcion="Pasaje de autobús", monto=2.50, categoria_id=categoria_transporte.id, metodo_pago_id=metodo_tarjeta_credito.id),
                Gasto(descripcion="Cena en restaurante", monto=30.00, categoria_id=categoria_alimentacion.id, metodo_pago_id=metodo_tarjeta_credito.id),
                Gasto(descripcion="Entrada al cine", monto=12.00, categoria_id=categoria_entretenimiento.id, metodo_pago_id=metodo_efectivo.id),
            ]
            db.add_all(gastos)
            db.commit()

    except Exception as e:
        db.rollback()
        print(f"Error al inicializar la base de datos: {e}")
    finally:
        db.close()

EOF

# Crear models/categoria.py
cat <<'EOF' > models/categoria.py
# gastomagico/models/categoria.py

from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from gastomagico.utils.database import Base

class Categoria(Base):
    __tablename__ = 'categorias'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Categoria(id={self.id}, nombre='{self.nombre}')>"
EOF

# Crear models/metodo_pago.py
cat <<'EOF' > models/metodo_pago.py
# gastomagico/models/metodo_pago.py

from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from gastomagico.utils.database import Base

class MetodoPago(Base):
    __tablename__ = 'metodos_pago'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<MetodoPago(id={self.id}, nombre='{self.nombre}')>"
EOF

# Crear models/gasto.py
cat <<'EOF' > models/gasto.py
# gastomagico/models/gasto.py

from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from gastomagico.utils.database import Base

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

    categoria = relationship("Categoria")
    metodo_pago = relationship("MetodoPago")

    def __repr__(self):
        return f"<Gasto(id={self.id}, monto={self.monto}, descripcion='{self.descripcion}')>"
EOF

# Crear models/frase_motivacional.py
cat <<'EOF' > models/frase_motivacional.py
# gastomagico/models/frase_motivacional.py

from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from gastomagico.utils.database import Base

class FraseMotivacional(Base):
    __tablename__ = 'frases_motivacionales'

    id = Column(Integer, primary_key=True, index=True)
    texto = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<FraseMotivacional(id={self.id}, texto='{self.texto}')>"
EOF

# Crear models/configuracion.py
cat <<'EOF' > models/configuracion.py
# gastomagico/models/configuracion.py

from sqlalchemy import Column, Integer, Float, DateTime
from datetime import datetime
from gastomagico.utils.database import Base

class Configuracion(Base):
    __tablename__ = 'configuraciones'

    id = Column(Integer, primary_key=True, index=True)
    limite_gasto = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Configuracion(id={self.id}, limite_gasto={self.limite_gasto})>"
EOF

# Crear use_cases/tabla_use_case.py
cat <<'EOF' > use_cases/tabla_use_case.py
# gastomagico/use_cases/tabla_use_case.py

from sqlalchemy.orm import Session
from gastomagico.models import Categoria, MetodoPago, FraseMotivacional
from gastomagico.utils.database import SessionLocal

class TablaUseCase:
    @staticmethod
    def agregar_categoria(nombre: str) -> None:
        db: Session = SessionLocal()
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
        db: Session = SessionLocal()
        try:
            return db.query(Categoria).all()
        finally:
            db.close()

    @staticmethod
    def eliminar_categoria(id_categoria: int) -> None:
        db: Session = SessionLocal()
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
        db: Session = SessionLocal()
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
        db: Session = SessionLocal()
        try:
            return db.query(MetodoPago).all()
        finally:
            db.close()

    @staticmethod
    def eliminar_metodo_pago(id_metodo: int) -> None:
        db: Session = SessionLocal()
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
        db: Session = SessionLocal()
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
        db: Session = SessionLocal()
        try:
            return db.query(FraseMotivacional).all()
        finally:
            db.close()
EOF

# Crear use_cases/gasto_use_case.py
cat <<'EOF' > use_cases/gasto_use_case.py
# gastomagico/use_cases/gasto_use_case.py

from sqlalchemy.orm import Session
from gastomagico.models import Gasto
from gastomagico.utils.database import SessionLocal

class GastoUseCase:
    @staticmethod
    def agregar_gasto(descripcion: str, monto: float, categoria_id: int, metodo_pago_id: int, fecha=None) -> None:
        db: Session = SessionLocal()
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
        db: Session = SessionLocal()
        try:
            return db.query(Gasto).all()
        finally:
            db.close()

    @staticmethod
    def eliminar_gasto(id_gasto: int) -> None:
        db: Session = SessionLocal()
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
EOF

# Crear use_cases/reporte_use_case.py
cat <<'EOF' > use_cases/reporte_use_case.py
# gastomagico/use_cases/reporte_use_case.py

from sqlalchemy.orm import Session
from gastomagico.models import Gasto, Configuracion, Categoria, MetodoPago
from gastomagico.utils.database import SessionLocal
import pandas as pd

class ReporteUseCase:
    @staticmethod
    def generar_reporte_excel(filepath: str) -> None:
        db: Session = SessionLocal()
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
            df.to_excel(filepath, index=False)
        except Exception as e:
            raise e
        finally:
            db.close()

    @staticmethod
    def importar_reporte_excel(filepath: str) -> None:
        db: Session = SessionLocal()
        try:
            df = pd.read_excel(filepath)
            for _, row in df.iterrows():
                # Obtener IDs de categoría y método de pago por nombre
                categoria = db.query(Categoria).filter(Categoria.nombre == row['Categoría']).first()
                metodo_pago = db.query(MetodoPago).filter(MetodoPago.nombre == row['Método de Pago']).first()

                if not categoria or not metodo_pago:
                    continue  # O maneja esto como un error

                gasto = Gasto(
                    descripcion=row['Descripción'],
                    monto=row['Monto'],
                    categoria_id=categoria.id,
                    metodo_pago_id=metodo_pago.id,
                    fecha=pd.to_datetime(row['Fecha'])
                )
                db.add(gasto)
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    @staticmethod
    def gastos_mensuales():
        db: Session = SessionLocal()
        try:
            from sqlalchemy import func
            resumen = db.query(
                func.strftime('%Y-%m', Gasto.fecha).label('mes'),
                func.sum(Gasto.monto).label('monto_total')
            ).group_by('mes').all()
            return {mes: monto for mes, monto in resumen}
        finally:
            db.close()

    @staticmethod
    def dia_menor_gasto():
        db: Session = SessionLocal()
        try:
            from sqlalchemy import func
            resumen = db.query(
                func.strftime('%Y-%m-%d', Gasto.fecha).label('dia'),
                func.sum(Gasto.monto).label('monto_total')
            ).group_by('dia').order_by('monto_total').first()
            return resumen.dia if resumen else None
        finally:
            db.close()

    @staticmethod
    def establecer_limite_gasto(limite: float) -> None:
        db: Session = SessionLocal()
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
EOF

# Crear controllers/tabla_controller.py
cat <<'EOF' > controllers/tabla_controller.py
# gastomagico/controllers/tabla_controller.py

from gastomagico.use_cases.tabla_use_case import TablaUseCase

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
EOF

# Crear controllers/gasto_controller.py
cat <<'EOF' > controllers/gasto_controller.py
# gastomagico/controllers/gasto_controller.py

from gastomagico.use_cases.gasto_use_case import GastoUseCase

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
EOF

# Crear controllers/reporte_controller.py
cat <<'EOF' > controllers/reporte_controller.py
# gastomagico/controllers/reporte_controller.py

from gastomagico.use_cases.reporte_use_case import ReporteUseCase

class ReporteController:
    @staticmethod
    def exportar_reporte_excel(filepath: str) -> None:
        ReporteUseCase.generar_reporte_excel(filepath)

    @staticmethod
    def importar_reporte_excel(filepath: str) -> None:
        ReporteUseCase.importar_reporte_excel(filepath)

    @staticmethod
    def gastos_mensuales():
        return ReporteUseCase.gastos_mensuales()

    @staticmethod
    def dia_menor_gasto():
        return ReporteUseCase.dia_menor_gasto()

    @staticmethod
    def establecer_limite_gasto(limite: float) -> None:
        ReporteUseCase.establecer_limite_gasto(limite)
EOF

# Crear utils/console.py
cat <<'EOF' > utils/console.py
# gastomagico/utils/console.py

def mostrar_frase_motivacional():
    from gastomagico.controllers.tabla_controller import TablaController
    import random
    frases = TablaController.listar_frases()
    if frases:
        return random.choice(frases).texto
    return "¡Bienvenido a GastoMágico!"
EOF

# Crear main.py
cat <<'EOF' > main.py
# gastomagico/main.py

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout,
    QHBoxLayout, QWidget, QTabWidget, QLabel, QLineEdit,
    QComboBox, QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox, QDateEdit, QDoubleSpinBox, QFileDialog
)
from PyQt5.QtCore import Qt, QDate
from controllers.gasto_controller import GastoController
from controllers.tabla_controller import TablaController
from controllers.reporte_controller import ReporteController
from utils.database import init_db
from utils.console import mostrar_frase_motivacional

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GastoMágico Desktop")
        self.setMinimumSize(800, 600)

        # Crear el widget principal con pestañas
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Inicializar las pestañas
        self.init_gastos_tab()
        self.init_categorias_tab()
        self.init_metodos_pago_tab()
        self.init_reportes_tab()

        # Mostrar una frase motivacional en la barra de estado
        self.statusBar().showMessage(mostrar_frase_motivacional())

    def init_gastos_tab(self):
        gastos_widget = QWidget()
        layout = QVBoxLayout()

        # Formulario para agregar gastos
        form_layout = QHBoxLayout()

        # Lado izquierdo - Campos de entrada
        inputs_layout = QVBoxLayout()

        # Campo de fecha
        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel("Fecha:"))
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        date_layout.addWidget(self.date_edit)
        inputs_layout.addLayout(date_layout)

        # Campo de monto
        amount_layout = QHBoxLayout()
        amount_layout.addWidget(QLabel("Monto:"))
        self.amount_spin = QDoubleSpinBox()
        self.amount_spin.setRange(0, 1000000)
        self.amount_spin.setDecimals(2)
        amount_layout.addWidget(self.amount_spin)
        inputs_layout.addLayout(amount_layout)

        # Campo de descripción
        desc_layout = QHBoxLayout()
        desc_layout.addWidget(QLabel("Descripción:"))
        self.desc_edit = QLineEdit()
        desc_layout.addWidget(self.desc_edit)
        inputs_layout.addLayout(desc_layout)

        # Dropdown de categoría
        cat_layout = QHBoxLayout()
        cat_layout.addWidget(QLabel("Categoría:"))
        self.cat_combo = QComboBox()
        self.refresh_categories()
        cat_layout.addWidget(self.cat_combo)
        inputs_layout.addLayout(cat_layout)

        # Dropdown de método de pago
        pay_layout = QHBoxLayout()
        pay_layout.addWidget(QLabel("Método de pago:"))
        self.pay_combo = QComboBox()
        self.refresh_payment_methods()
        pay_layout.addWidget(self.pay_combo)
        inputs_layout.addLayout(pay_layout)

        form_layout.addLayout(inputs_layout)

        # Lado derecho - Botones
        buttons_layout = QVBoxLayout()
        add_button = QPushButton("Agregar Gasto")
        add_button.clicked.connect(self.add_expense)
        delete_button = QPushButton("Eliminar Gasto")
        delete_button.clicked.connect(self.delete_expense)
        buttons_layout.addWidget(add_button)
        buttons_layout.addWidget(delete_button)
        buttons_layout.addStretch()

        form_layout.addLayout(buttons_layout)
        layout.addLayout(form_layout)

        # Tabla para mostrar gastos
        self.expenses_table = QTableWidget()
        self.expenses_table.setColumnCount(6)
        self.expenses_table.setHorizontalHeaderLabels(
            ["ID", "Fecha", "Monto", "Descripción", "Categoría", "Método de Pago"]
        )
        header = self.expenses_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.expenses_table)

        self.refresh_expenses_table()

        gastos_widget.setLayout(layout)
        self.tabs.addTab(gastos_widget, "Gastos")

    def init_categorias_tab(self):
        cat_widget = QWidget()
        layout = QVBoxLayout()

        # Sección para agregar categoría
        input_layout = QHBoxLayout()
        self.cat_input = QLineEdit()
        self.cat_input.setPlaceholderText("Nueva categoría")
        add_cat_button = QPushButton("Agregar Categoría")
        add_cat_button.clicked.connect(self.add_category)
        input_layout.addWidget(self.cat_input)
        input_layout.addWidget(add_cat_button)
        layout.addLayout(input_layout)

        # Tabla de categorías
        self.cat_table = QTableWidget()
        self.cat_table.setColumnCount(2)
        self.cat_table.setHorizontalHeaderLabels(["ID", "Nombre"])
        header = self.cat_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.cat_table)

        self.refresh_categories_table()

        cat_widget.setLayout(layout)
        self.tabs.addTab(cat_widget, "Categorías")

    def init_metodos_pago_tab(self):
        pay_widget = QWidget()
        layout = QVBoxLayout()

        # Sección para agregar método de pago
        input_layout = QHBoxLayout()
        self.pay_input = QLineEdit()
        self.pay_input.setPlaceholderText("Nuevo método de pago")
        add_pay_button = QPushButton("Agregar Método")
        add_pay_button.clicked.connect(self.add_payment_method)
        input_layout.addWidget(self.pay_input)
        input_layout.addWidget(add_pay_button)
        layout.addLayout(input_layout)

        # Tabla de métodos de pago
        self.pay_table = QTableWidget()
        self.pay_table.setColumnCount(2)
        self.pay_table.setHorizontalHeaderLabels(["ID", "Nombre"])
        header = self.pay_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.pay_table)

        self.refresh_payment_methods_table()

        pay_widget.setLayout(layout)
        self.tabs.addTab(pay_widget, "Métodos de Pago")

    def init_reportes_tab(self):
        report_widget = QWidget()
        layout = QVBoxLayout()

        # Botón para exportar a Excel
        export_button = QPushButton("Exportar a Excel")
        export_button.clicked.connect(self.export_report)
        layout.addWidget(export_button)

        # Botón para importar desde Excel
        import_button = QPushButton("Importar desde Excel")
        import_button.clicked.connect(self.import_report)
        layout.addWidget(import_button)

        # Botón para reportes personalizados
        custom_button = QPushButton("Reportes Personalizados")
        custom_button.clicked.connect(self.custom_reports)
        layout.addWidget(custom_button)

        # Botón para establecer límite de gasto
        limite_layout = QHBoxLayout()
        self.limite_input = QDoubleSpinBox()
        self.limite_input.setRange(0, 1000000)
        self.limite_input.setDecimals(2)
        self.limite_input.setPrefix("$")
        limite_layout.addWidget(QLabel("Establecer Límite de Gasto:"))
        limite_layout.addWidget(self.limite_input)
        establecer_limite_button = QPushButton("Establecer")
        establecer_limite_button.clicked.connect(self.establecer_limite_gasto)
        limite_layout.addWidget(establecer_limite_button)
        layout.addLayout(limite_layout)

        layout.addStretch()
        report_widget.setLayout(layout)
        self.tabs.addTab(report_widget, "Reportes")

    def add_expense(self):
        try:
            fecha = self.date_edit.date().toPyDate()
            monto = self.amount_spin.value()
            descripcion = self.desc_edit.text()
            categoria_nombre = self.cat_combo.currentText()
            metodo_pago_nombre = self.pay_combo.currentText()

            if not all([monto, descripcion, categoria_nombre, metodo_pago_nombre]):
                QMessageBox.warning(self, "Error", "Todos los campos son obligatorios")
                return

            # Obtener ID de la categoría
            categorias = TablaController.listar_categorias()
            categoria = next((cat for cat in categorias if cat.nombre == categoria_nombre), None)
            if not categoria:
                QMessageBox.warning(self, "Error", "Categoría seleccionada inválida")
                return

            # Obtener ID del método de pago
            metodos_pago = TablaController.listar_metodos_pago()
            metodo_pago = next((met for met in metodos_pago if met.nombre == metodo_pago_nombre), None)
            if not metodo_pago:
                QMessageBox.warning(self, "Error", "Método de pago seleccionado inválido")
                return

            # Agregar gasto
            GastoController.agregar_gasto(
                descripcion=descripcion,
                monto=monto,
                categoria_id=categoria.id,
                metodo_pago_id=metodo_pago.id,
                fecha=fecha
            )
            self.refresh_expenses_table()
            self.clear_expense_form()
            QMessageBox.information(self, "Éxito", "Gasto agregado correctamente")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def delete_expense(self):
        current_row = self.expenses_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Error", "Seleccione un gasto para eliminar")
            return

        id_gasto_item = self.expenses_table.item(current_row, 0)
        if not id_gasto_item:
            QMessageBox.warning(self, "Error", "ID de gasto inválido")
            return

        try:
            id_gasto = int(id_gasto_item.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "ID de gasto inválido")
            return

        reply = QMessageBox.question(
            self, "Confirmar", "¿Está seguro de eliminar este gasto?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                GastoController.eliminar_gasto(id_gasto)
                self.refresh_expenses_table()
                QMessageBox.information(self, "Éxito", "Gasto eliminado correctamente")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def add_category(self):
        nombre = self.cat_input.text()
        if not nombre:
            QMessageBox.warning(self, "Error", "Ingrese un nombre para la categoría")
            return

        try:
            TablaController.agregar_categoria(nombre)
            self.refresh_categories_table()
            self.refresh_categories()
            self.cat_input.clear()
            QMessageBox.information(self, "Éxito", "Categoría agregada correctamente")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def add_payment_method(self):
        nombre = self.pay_input.text()
        if not nombre:
            QMessageBox.warning(self, "Error", "Ingrese un nombre para el método de pago")
            return

        try:
            TablaController.agregar_metodo_pago(nombre)
            self.refresh_payment_methods_table()
            self.refresh_payment_methods()
            self.pay_input.clear()
            QMessageBox.information(self, "Éxito", "Método de pago agregado correctamente")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def refresh_expenses_table(self):
        gastos = GastoController.listar_gastos()
        self.expenses_table.setRowCount(len(gastos))
        for i, gasto in enumerate(gastos):
            self.expenses_table.setItem(i, 0, QTableWidgetItem(str(gasto.id)))
            self.expenses_table.setItem(i, 1, QTableWidgetItem(gasto.fecha.strftime("%Y-%m-%d") if gasto.fecha else ""))
            self.expenses_table.setItem(i, 2, QTableWidgetItem(f"${gasto.monto:.2f}"))
            self.expenses_table.setItem(i, 3, QTableWidgetItem(gasto.descripcion))
            self.expenses_table.setItem(i, 4, QTableWidgetItem(gasto.categoria.nombre if gasto.categoria else "N/A"))
            self.expenses_table.setItem(i, 5, QTableWidgetItem(gasto.metodo_pago.nombre if gasto.metodo_pago else "N/A"))

    def refresh_categories_table(self):
        categorias = TablaController.listar_categorias()
        self.cat_table.setRowCount(len(categorias))
        for i, cat in enumerate(categorias):
            self.cat_table.setItem(i, 0, QTableWidgetItem(str(cat.id)))
            self.cat_table.setItem(i, 1, QTableWidgetItem(cat.nombre))

    def refresh_payment_methods_table(self):
        metodos = TablaController.listar_metodos_pago()
        self.pay_table.setRowCount(len(metodos))
        for i, met in enumerate(metodos):
            self.pay_table.setItem(i, 0, QTableWidgetItem(str(met.id)))
            self.pay_table.setItem(i, 1, QTableWidgetItem(met.nombre))

    def refresh_categories(self):
        self.cat_combo.clear()
        categorias = TablaController.listar_categorias()
        self.cat_combo.addItems([cat.nombre for cat in categorias])

    def refresh_payment_methods(self):
        self.pay_combo.clear()
        metodos = TablaController.listar_metodos_pago()
        self.pay_combo.addItems([met.nombre for met in metodos])

    def clear_expense_form(self):
        self.date_edit.setDate(QDate.currentDate())
        self.amount_spin.setValue(0)
        self.desc_edit.clear()
        if self.cat_combo.count() > 0:
            self.cat_combo.setCurrentIndex(0)
        if self.pay_combo.count() > 0:
            self.pay_combo.setCurrentIndex(0)

    def export_report(self):
        filepath, _ = QFileDialog.getSaveFileName(self, "Guardar Reporte Excel", "", "Excel Files (*.xlsx)")
        if filepath:
            try:
                ReporteController.exportar_reporte_excel(filepath)
                QMessageBox.information(self, "Éxito", f"Reporte exportado correctamente a {filepath}")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def import_report(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Importar Reporte Excel", "", "Excel Files (*.xlsx)")
        if filepath:
            try:
                ReporteController.importar_reporte_excel(filepath)
                self.refresh_expenses_table()
                QMessageBox.information(self, "Éxito", "Datos importados correctamente")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def custom_reports(self):
        # Mostrar gastos mensuales
        resumen = ReporteController.gastos_mensuales()
        if resumen:
            mensaje = "Gastos Mensuales:\n"
            for mes, monto in sorted(resumen.items()):
                mensaje += f"{mes}: ${monto:.2f}\n"
            QMessageBox.information(self, "Gastos Mensuales", mensaje)
        else:
            QMessageBox.information(self, "Gastos Mensuales", "No hay gastos registrados.")

        # Mostrar día con menor gasto
        dia_menor = ReporteController.dia_menor_gasto()
        if dia_menor:
            QMessageBox.information(self, "Día con Menor Gasto", f"El día con menor gasto es: {dia_menor}")
        else:
            QMessageBox.information(self, "Día con Menor Gasto", "No hay suficientes datos para determinar el día con menor gasto.")

    def establecer_limite_gasto(self):
        limite = self.limite_input.value()
        try:
            ReporteController.establecer_limite_gasto(limite)
            QMessageBox.information(self, "Éxito", f"Límite de gasto establecido en ${limite:.2f}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

def run_qt_app():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    init_db()  # Inicializa la base de datos y crea las tablas
    run_qt_app()
EOF

# Crear use_cases/reporte_use_case.py
# (Este paso ya se realizó arriba, por lo que no es necesario repetirlo)

# Crear utils/console.py
# (Este paso ya se realizó arriba, por lo que no es necesario repetirlo)

# Crear main.py
# (Este paso ya se realizó arriba, por lo que no es necesario repetirlo)

# Configurar el entorno virtual
echo "Creando el entorno virtual..."
python3 -m venv .venv

# Activar el entorno virtual

# Actualizar pip
echo "Actualizando pip..."
pip install --upgrade pip

# Instalar dependencias

# Desactivar el entorno virtual
deactivate

echo "Configuración completada exitosamente."
echo "Para ejecutar la aplicación, sigue estos pasos:"
echo "  1. Navega al directorio del proyecto:"
echo "       cd $PROJECT_DIR"
echo "  2. Activa el entorno virtual:"
echo "       source .venv/bin/activate"
echo "  3. Ejecuta la aplicación:"
echo "       python main.py"
