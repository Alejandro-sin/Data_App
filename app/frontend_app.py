'''
 

La idea es que aquí corra


'''

import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from io import StringIO
import requests as rq
from sqlalchemy import create_engine
from utils import dbs_utils, eda_utils
from pipe.preprocess import process_employees
import os
import time





API_URL = "http://127.0.0.1:8000/data"


options = ["DataBox", "KnowledgeBox"]


with st.sidebar:
    select = option_menu(
        menu_title="DataApp",
        options=options,
        icons=["box", "bar-chart","robot"],
        menu_icon="cast",
        default_index=0,
    )

#response =  rq.get(API_URL)
#st.write(response.content)
engine = create_engine('sqlite:///:memory:')
db_name = "data_db"



def clean_filename(filename):
    name = os.path.splitext(filename)[0]  # Elimina la extensión
    return name.replace(" ", "_")  # Reemplaza espacios con guiones bajos para que sea válido como nombre de tabla

        
def process_chunks(file, columns, table_name, chunksize=1000):
    for chunk in pd.read_csv(file, 
                             sep=",", 
                             header=None, 
                             names=columns, 
                             encoding="utf-8", 
                             index_col=0, 
                             chunksize=chunksize):
        
        dbs_utils.save_dataframe_to_sql(chunk, db_name='sql_db', table_name=table_name)


engine = dbs_utils.create_engine_to_sqlite()

if select == "DataBox":
    st.markdown("""
        # Feed with data
    """)

    
    uploaded_file = st.file_uploader(" ")

    if uploaded_file is not None:
        # Limpiar el nombre del archivo y usarlo como nombre de tabla
        table_name = clean_filename(uploaded_file.name)

        # Definir columnas dependiendo del nombre de la tabla
        if table_name == 'jobs':
            columns = ["id", "job"]
        elif table_name == "departments":
            columns = ["id", "department"]
        elif table_name == "hired_employees":
            columns = ["id", "name", "datetime", "department_id", "job_id"]
        else:
            st.warning('The headers of data can be inferred', icon="⚠️")
            table_name = "No table Name"
            columns = None  # Se infiere el encabezado manual


        BRONZE_PATH = f"../data/bronce/{table_name}.csv"
        SILVER_PATH = f"../data/silver/{table_name}.csv"
        GOLD_PATH = f"../data/gold/{table_name}.csv"



        dataframe = pd.read_csv(uploaded_file,
                                    sep=",",
                                    header= None,
                                    names = columns,
                                    encoding="utf-8",
                                    index_col=0
                                    )
        
        # EDA exploration
        eda_utils.review_dataset(dataframe)


        # Persist in bronce
        dataframe.to_csv(BRONZE_PATH)


        # PROCESAMIENTO:
        df = process_employees(dataframe)


        #


        st.write("______________________________________________________")
        with st.spinner('Wait for it...'):

            time.sleep(1.5)
            st.markdown(f"""#### Processing Batch of: :green[{len(cleaned_df)}] rows for table: :green['{table_name}']""")
            st.write("Data Persisted: ")
            st.dataframe(cleaned_df,width=1000)

            time.sleep(1.5)

            df_persited = pd.read_sql(table_name, con=engine)
        if table_name != "No table Name":
            # Procesar el archivo por lotes de 1000 filas
            process_chunks(uploaded_file, columns, table_name)
        else:
            # Si no se puede determinar el nombre de la tabla o las columnas
            st.error("Invalid name for table!")


elif select =="KnowledgeBox":
    st.markdown("""
        # KnowledgeBox
        """)

    col1, col2 = st.columns(2)    
    col2.header("Graficos")
    original = st.write("Graficos por construir")
    col1.header("Knowledge Interaction")
    col1.write("C....")


    # Funcionalidad de Chat que puedo crear para que responda.
    st.chat_input()


def main():
    pass


if __name__ == "__main__":
    main()