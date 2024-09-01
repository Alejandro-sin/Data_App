'''
 

La idea es que aquí corra


'''

import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from io import StringIO




options = ["DataBox","InsigthsBox", "KnowledgeBox"]


with st.sidebar:
    select = option_menu(
        menu_title="DataApp",
        options=options,
        icons=["box", "bar-chart","robot"],
        menu_icon="cast",
        default_index=0,
    )



if select =="DataBox":
    st.markdown("""
        # Feed with data
        """)
    uploaded_file = st.file_uploader(" ")
    if uploaded_file is not None:
          # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        st.write(bytes_data)

        # To convert to a string based IO:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        st.write(stringio)

        # To read file as string:
        string_data = stringio.read()
        st.write(string_data)

        # Can be used wherever a "file-like" object is accepted:
        dataframe = pd.read_csv(uploaded_file)
        st.write(dataframe)

elif select =="InsigthsBox":
    st.markdown("""
        # InsigthsBox
        """)
    
    col1, col2 = st.columns(2)

    
    col1.header("Graficos")
    original = st.write("Graficos por construir")

    
    col2.header("AI Suggestions")
    col2.write("Cuadro de respuestas de la AI")




    st.chat_input()
elif select =="KnowledgeBox":
    st.markdown("""
        # KnowledgeBox
        """)
    

    col1, col2 = st.columns(2)

    
    col2.header("Graficos")
    original = st.write("Graficos por construir")

    
    col1.header("Knowledge Interaction")
    col1.write("C....")





    st.chat_input()


def main():
    pass


if __name__ == "__main__":
    main()