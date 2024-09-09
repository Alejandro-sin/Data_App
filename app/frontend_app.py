'''
 

La idea es que aquí corra


'''

import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_agraph import agraph, Node, Edge, Config
from streamlit_agraph.config import Config, ConfigBuilder



from neo4j import GraphDatabase

import pandas as pd
from io import StringIO
import requests as rq
from sqlalchemy import create_engine
from utils import dbs_utils, eda_utils
from pipe.preprocess import process_employees, get_employees_count, get_most_hired_by_departments
from db.database import engine
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


def clean_filename(filename):
    name = os.path.splitext(filename)[0]  
    return name.replace(" ", "_")  


# To Batch Upload
def process_chunks(file, columns, table_name, chunksize=1000):
    for chunk in pd.read_csv(file, 
                             sep=",", 
                             header=None, 
                             names=columns, 
                             encoding="utf-8", 
                             index_col=0, 
                             chunksize=chunksize):
        
        dbs_utils.save_dataframe_to_sql(chunk, db_name='sql_db', table_name=table_name)




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
            columns = ["job_id", "job_name"]
        elif table_name == "departments":
            columns = ["department_id", "department_name"]
        elif table_name == "hired_employees":
            columns = ["employee_id", "name", "datetime", "department_id", "job_id"]
        else:
            st.warning('The headers of data can be inferred', icon="⚠️")
            table_name = "No table Name"
            columns = None  # Se infiere el encabezado manual


        BRONZE_PATH = f"./data/bronce/{table_name}.csv"
        SILVER_PATH = f"data/silver/{table_name}.csv"
        GOLD_PATH = f"data/gold/{table_name}.csv"



        dataframe = pd.read_csv(uploaded_file,
                                    sep=",",
                                    header= None,
                                    names = columns,
                                    encoding="utf-8",
                                    index_col=0
                                    )
        
        # EDA exploration
        # eda_utils.review_dataset(dataframe)

        os.makedirs(os.path.dirname(BRONZE_PATH), exist_ok=True)
        # Persist in bronce Landing
        dataframe.to_csv(BRONZE_PATH)

        
        if st.button("Process", type="primary"):
            st.write("______________________________________________________")
            
            with st.spinner('Wait for it...'):
                time.sleep(1.5)
                #Process to silver
                if table_name == "hired_employees":
                    st.markdown("#### Análisis de Contrataciones por Departamento y Puesto en 2021")
                    df = process_employees(dataframe, SILVER_PATH)
                    # get_employees_count, get_most_hired_by_departments
                    df_1 = get_employees_count(df)
                    st.dataframe(df_1, width=1000)
                    st.markdown("#### Análisis Departamento por encima de la media")
                    df_2 = get_most_hired_by_departments(df)
                    st.dataframe(df_2, width=1000)
                else:
                    st.dataframe(dataframe, width=1000)
        
        # When file needs to be batched

        #if table_name != "No table Name":
            # Procesar el archivo por lotes de 1000 filas
        #    process_chunks(uploaded_file, columns, table_name)
        #else:
            # Si no se puede determinar el nombre de la tabla o las columnas
            #st.error("Invalid name for table!")

        


### 
elif select =="KnowledgeBox":
        
    import requests
    # NEO4J
    response = requests.get("http://127.0.0.1:8000/streamlit_agraph")
    results = response.content

    nodes = []
    edges = []

    id = results[0].data()["p"]['id']
    id

    for _, result in enumerate(results):
        id = results[_].data()["p"]['id']
        name = results[_].data()["p"]['name']
        relation =results[_].data()["h"][1]
        target = results[_].data()["j"]["name"]
        nodes.append(Node(id=id, label=name, size=25))
        edges.append(Edge(source=name, label=relation, target=target,))


    config = Config(width=750,
                        height=950,
                        directed=True, 
                        physics=True, 
                        hierarchical=False,
                        # **kwargs
                        ) 

    return_value = agraph(nodes=nodes[:3], 
                            edges=edges[:3], 
                            config=config)


def main():
    pass


if __name__ == "__main__":
    main()