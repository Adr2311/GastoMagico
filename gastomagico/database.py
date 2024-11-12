from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Crear el motor de la base de datos con echo=True para imprimir las consultas SQL
engine = create_engine('sqlite:///gastomagico.db', echo=True)

# Crear una sesión de base de datos
Session = sessionmaker(bind=engine)
session = Session()
