import pandas as pd
import streamlit as st


def review_dataset(df):
    st.header("Fast EDA Report:")
    # Display number of missing values per column
    st.html("<hr>")
    st.markdown("""## Number of missing values per column:""")
    st.html("<hr>")
    missing_values = df.isnull().sum()
    st.dataframe(missing_values, width=1000,)
        
    # Display descriptive statistics
    st.html("<hr>")
    st.markdown("## Descriptive Statistics:")
    st.html("<hr>")
    st.dataframe(df.describe(include='all'), width=1000)

    # Display number of duplicate rows
    st.html("<hr>")
    st.markdown("## Number of Duplicate Rows:")
    st.html("<hr>")
    st.write(df.duplicated().sum())

    # Display data types of each column
    st.html("<hr>")
    st.markdown("## Data Types of Each Column:")
    st.html("<hr>")
    st.dataframe(df.dtypes, width=1000)

    # Display number of unique values per column
    st.html("<hr>")
    st.markdown("## Unique Values per Column:")
    st.html("<hr>")
    st.dataframe(df.nunique(), width=1000)
