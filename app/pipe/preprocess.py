
'''

Módulo para imputar y limpair el dataset, 
en valore snumericos inputaremos con el promedio
En valor del texto se ususará u nvalor fijo
Y un treshold para dropear los datos si la fila tiene más NaN

'''

import pandas as pd
from pathlib import Path




def process_employees(df, path_to_persist=None):
    '''
    Tiene como proósito limpiar el dataset relizar transformaicones

    args: 
        df
        path_to_persist

    '''
    # Cambio columna
    df.rename(
        columns={
            "id" :"employee_id"
        }, inplace=True)   
    
    # Quiero imputar fechas vacías
    fecha_dummy = pd.to_datetime('2000-01-01')
    df_employees_1 = impute_and_clean(df, nan_threshold=0.5)
    df_hired_employees_c = df_employees_1.fillna(fecha_dummy)

    # Imputar valores vacíos de camplos clave
    df_hired_employees_c['department_id'] = df_hired_employees_c['department_id'].fillna(-1).astype(int)
    df_hired_employees_c['job_id'] = df_hired_employees_c['job_id'].fillna(-1).astype(int)
    
    # Transformaciones del dataset para fecha
    df_hired_employees_c['datetime'] = pd.to_datetime(df_hired_employees_c['datetime'], errors='coerce')
    df_hired_employees_c['year'] = df_hired_employees_c['datetime'].dt.year
    df_hired_employees_c['quarter'] = df_hired_employees_c['datetime'].dt.to_period('Q')
    
    # Persistir en Silver
    df_hired_employees_c.to_csv(path_to_persist)

    return df_hired_employees_c





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


def get_employees_count(df_hired_employees_c, data_dir="D:/_Projects/Data_App/data/silver"):
    # Definir las rutas de los archivos de manera dinámica
    jobs_file = Path(data_dir) / "cleaned_jobs.csv"
    departments_file = Path(data_dir) / "cleaned_departments.csv"
    
    # Verificar si los archivos existen
    if not jobs_file.exists():
        raise FileNotFoundError(f"El archivo {jobs_file} no existe.")
    if not departments_file.exists():
        raise FileNotFoundError(f"El archivo {departments_file} no existe.")
    
    # Leer los archivos CSV
    jobs_df = pd.read_csv(jobs_file)
    departments_df = pd.read_csv(departments_file)

    # Filtrar empleados contratados en 2021
    df_hired_employees_c_filtered = df_hired_employees_c[df_hired_employees_c["datetime"].dt.year == 2021]

    # Join con jobs y departments
    merged_df = pd.merge(df_hired_employees_c_filtered, jobs_df, on="job_id")
    merged_df = pd.merge(merged_df, departments_df, on="department_id")

    # Agrupar por department, job y quarter, y contar el número de empleados contratados
    result = merged_df.groupby(['department_name', 'job_name', 'quarter']).size().reset_index(name='num_employees_hired')
    
    # Ordenar el resultado por department, job y quarter
    result_df = result.sort_values(by=['department_name', 'job_name', 'quarter'])

    return result_df



def get_most_hired_by_departments(df_hired_employees_c, data_dir="D:/_Projects/Data_App/data/silver"):
    # Definir la ruta del archivo de departamentos
    departments_file = Path(data_dir) / "cleaned_departments.csv"
    
    # Verificar si el archivo de departamentos existe
    if not departments_file.exists():
        raise FileNotFoundError(f"El archivo {departments_file} no existe.")
    
    # Leer el archivo de departamentos
    departments_df = pd.read_csv(departments_file)
    
    # Filtrar empleados contratados en 2021
    df_hired_employees_c_filtered = df_hired_employees_c[df_hired_employees_c["datetime"].dt.year == 2021]
    
    # Agrupar por department_id y contar el número de empleados contratados
    df_hired_employees_grouped = df_hired_employees_c_filtered.groupby(by=["department_id"]).size().reset_index(name='num_employees_hired')
    
    # Calcular la media de empleados contratados
    mean_hired = df_hired_employees_grouped["num_employees_hired"].mean()  # valor escalar
    
    # Filtrar departamentos con contrataciones por encima de la media
    departments_df_above_mean = df_hired_employees_grouped[df_hired_employees_grouped["num_employees_hired"] > mean_hired]
    
    # Hacer el join con el archivo de departamentos
    result = departments_df_above_mean.merge(departments_df, on="department_id")
    
    # Ordenar y seleccionar columnas necesarias
    result_df = result[['department_id', 'department_name', 'num_employees_hired']].sort_values(by='num_employees_hired', ascending=False)
    
    return result_df

