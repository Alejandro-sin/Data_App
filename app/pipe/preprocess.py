
'''

Módulo para imputar y limpair el dataset, 
en valore snumericos inputaremos con el promedio
En valor del texto se ususará u nvalor fijo
Y un treshold para dropear los datos si la fila tiene más NaN

'''
# %%
import pandas as pd
from pipe.preprocess import impute_and_clean

def process_employees(df):
    print("Valores nulos antes de la limpieza:")
    print(df.isnull().sum())

    # limpiar
    cleaned_df = impute_and_clean(df, nan_threshold=0.5)

    # Cambiar tipos de datos y extraer el año para los quarters
    cleaned_df['datetime'] = pd.to_datetime(cleaned_df['datetime'], errors='coerce')
    cleaned_df['year'] = cleaned_df['datetime'].dt.year
    cleaned_df['quarter'] = cleaned_df['datetime'].dt.to_period('Q')

    # Filtrar la data para el año 2021 y fillear los NA con un valor fijo
    cleaned_df_hired_2021 = cleaned_df[cleaned_df['year'] == 2021]
    cleaned_df['department_id'] = cleaned_df['department_id'].fillna(-1).astype(int)
    cleaned_df['job_id'] = cleaned_df['job_id'].fillna(-1).astype(int)
    cleaned_df['year'] = cleaned_df['datetime'].dt.year.fillna(-1).astype(int)

    # Agregaciones por departamen
    grouped_df = cleaned_df_hired_2021.groupby(['department_id', 'job_id', 'quarter']).size().reset_index(name='num_employees')
    grouped_df_sorted = grouped_df.sort_values(by=['department_id', 'job_id', 'quarter'])

    print("Número de empleados contratados por trabajo y departamento en 2021:")
    print(grouped_df_sorted)

    mean_employees_per_dept = cleaned_df_hired_2021.groupby('department_id').size().mean()
    above_avg_depts = cleaned_df_hired_2021.groupby('department_id').size().reset_index(name='num_employees')
    above_avg_depts = above_avg_depts[above_avg_depts['num_employees'] > mean_employees_per_dept]
    above_avg_depts_sorted = above_avg_depts.sort_values(by='num_employees', ascending=False)


    print("Departamentos que contrataron más empleados que la media en 2021:")
    print(above_avg_depts_sorted)







def impute_and_clean(df, nan_threshold=0.5, impute_value_text="Not Specified"):
    """
    Imputes missing values and cleans the dataset according to a threshold for allowed NaN values.

    Parameters:
    df (pd.DataFrame): The DataFrame to impute and clean.
    nan_threshold (float): The threshold for allowed NaN values per row (as a percentage of columns).
    impute_value_text (str): The value to use for imputing text columns.

    Returns:
    pd.DataFrame: The imputed and cleaned DataFrame.
    """
    
    # Impute numeric columns with the mean
    numeric_df = df.select_dtypes(include=["number"])
    df[numeric_df.columns] = numeric_df.fillna(numeric_df.mean())

    # Impute text columns with a fixed value
    text_df = df.select_dtypes(include=["object"])
    df[text_df.columns] = text_df.fillna(impute_value_text)

    # Drop rows with more NaN values than the threshold
    nan_threshold_columns = int(len(df.columns) * nan_threshold)
    cleaned_df = df.dropna(thresh=nan_threshold_columns)

    return cleaned_df