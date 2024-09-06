# %%
import pandas as pd
from pipe.preprocess import impute_and_clean

# %%
# Cargar los datos de empleados contratados
df_ = pd.read_csv("../data/bronce/hired_employees.csv", index_col=0)

# Verificación rápida de valores nulos antes de la imputación
print("Valores nulos antes de la limpieza:")
print(df_.isnull().sum())

# %%
# Limpieza e imputación de datos
cleaned_df = impute_and_clean(df_, nan_threshold=0.5)

# Verificación rápida de valores nulos después de la imputación
print("Valores nulos después de la limpieza:")
print(cleaned_df.isnull().sum())

# %%
# Verificación de los tipos de datos
print("Tipos de datos después de la limpieza:")
print(cleaned_df.dtypes)

# %%
# Convertir la columna 'datetime' a formato de fecha y extraer año y trimestre
cleaned_df['datetime'] = pd.to_datetime(cleaned_df['datetime'], errors='coerce')
cleaned_df['year'] = cleaned_df['datetime'].dt.year
cleaned_df['quarter'] = cleaned_df['datetime'].dt.to_period('Q')

# Filtrar empleados contratados en 2021
cleaned_df_hired_2021 = cleaned_df[cleaned_df['year'] == 2021]

# %%
# Rellenar los valores nulos en 'department_id' y 'job_id' con -1 y convertirlos a enteros
cleaned_df['department_id'] = cleaned_df['department_id'].fillna(-1).astype(int)
cleaned_df['job_id'] = cleaned_df['job_id'].fillna(-1).astype(int)

# Asegurarse de que la columna 'year' esté en formato entero
cleaned_df['year'] = cleaned_df['datetime'].dt.year.fillna(-1).astype(int)

# %%
# Verificación final de los tipos de datos en el DataFrame de empleados contratados en 2021
print("Tipos de datos en el DataFrame de empleados contratados en 2021:")
print(cleaned_df_hired_2021.dtypes)

# %%
# Pregunta de negocio 1: Número de empleados contratados por trabajo y departamento en 2021, dividido por trimestre
grouped_df = cleaned_df_hired_2021.groupby(['department_id', 'job_id', 'quarter']).size().reset_index(name='num_employees')

# Ordenar por departamento y trabajo en orden alfabético
grouped_df_sorted = grouped_df.sort_values(by=['department_id', 'job_id', 'quarter'])
print("Número de empleados contratados por trabajo y departamento en 2021:")
print(grouped_df_sorted)

# %%
# Pregunta de negocio 2: Lista de departamentos que contrataron más empleados que la media en 2021
# Calcular el número medio de empleados contratados por departamento en 2021
mean_employees_per_dept = cleaned_df_hired_2021.groupby('department_id').size().mean()

# Filtrar departamentos que contrataron más empleados que la media
above_avg_depts = cleaned_df_hired_2021.groupby('department_id').size().reset_index(name='num_employees')
above_avg_depts = above_avg_depts[above_avg_depts['num_employees'] > mean_employees_per_dept]

# Unir con la información de nombres de los departamentos y ordenar por número de empleados contratados
above_avg_depts_sorted = above_avg_depts.sort_values(by='num_employees', ascending=False)
print("Departamentos que contrataron más empleados que la media en 2021:")
print(above_avg_depts_sorted)

# %%
