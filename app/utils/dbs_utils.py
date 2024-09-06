'''
Este módulo sirve como herramienta para operaciones con bases de datos SQL y Graph
'''

import os
import pandas as pd
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base


DB_FOLDER = 'db'
URL="POSTGRESQL TO DO"

Base = declarative_base()
metadata = MetaData()

def create_engine_to_sqlite():
    # Verificar si la carpeta 'db' existe, si no, crearla
    db_folder = 'db'
    if not os.path.exists(db_folder):
        os.makedirs(db_folder)

    # Ruta completa hacia la base de datos SQLite dentro de la carpeta 'db'
    database_path = os.path.join(db_folder, 'sql_db.sqlite')

    # Crear el motor de conexión
    engine = create_engine(f'sqlite:///{database_path}')
    return engine




def get_db_path(db_name):
    """
    Genera la ruta completa del archivo SQLite basado en el nombre de la base de datos.
    
    Args: db_name (str): Nombre de la base de datos sin extensión.
    Returns: str: Ruta completa de la base de datos SQLite.
    """
    if not os.path.exists(DB_FOLDER):
        os.makedirs(DB_FOLDER)
    return os.path.join(DB_FOLDER, f'{db_name}.sqlite')




def save_dataframe_to_sql(dataframe, db_name, table_name):
    """
    Guarda un DataFrame en una tabla de la base de datos SQLite.
    
    Args:
        dataframe (pd.DataFrame): El DataFrame que se desea guardar.
        db_name (str): Nombre de la base de datos sin la extensión.
        table_name (str): Nombre de la tabla donde se guardará el DataFrame.
    """
    db_path = get_db_path(db_name)
    engine = create_engine(f'sqlite:///{db_path}')
    dataframe.to_sql(table_name, con=engine, index=False, if_exists='replace')
    print(f'Tabla {table_name} guardada en la base de datos {db_name}.sqlite en la carpeta {DB_FOLDER}.')
    return "Data saved on DB!"




def init_db(db_name: str = "test"):
    """
    Inicializa la base de datos, creando el motor, la sesión y el esquema base.

    Args:
        db_name (str): Nombre de la base de datos sin la extensión. Por defecto, usa 'test'.
    
    Returns:
        engine: Motor de la base de datos.
        SessionLocal: Clase de sesión para la base de datos.
    """
    db_path = get_db_path(db_name)
    db_url = f"sqlite:///{db_path}"
    engine = create_engine(db_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine, SessionLocal
