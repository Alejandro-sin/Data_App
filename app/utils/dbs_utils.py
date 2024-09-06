'''


This module aims to serve as function tool tulities for SQL and Graph Databases operations


'''
import os
import pandas as pd
from sqlalchemy import create_engine



def save_dataframe_to_sql(dataframe, db_name, table_name):
    db_folder = 'db'
    if not os.path.exists(db_folder):
        os.makedirs(db_folder)
    
    # Ruta de la base de datos
    db_path = os.path.join(db_folder, f'{db_name}.sqlite')

    # Crear la conexión a la base de datos SQLite
    engine = create_engine(f'sqlite:///{db_path}')

    # Guardar el DataFrame en SQL
    dataframe.to_sql(table_name, con=engine, index=False, if_exists='replace')

    print(f'Tabla {table_name} guardada en la base de datos {db_name}.sqlite en la carpeta {db_folder}.')