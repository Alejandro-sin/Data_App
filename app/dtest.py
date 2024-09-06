import psycopg2


# Conéctate a la base de datos usando psycopg2
conn = psycopg2.connect(
    dbname="api_db", 
    user='postgres',  
    password='12345678',  
    host='localhost',  
    port='5432'
)



# Crea un cursor para ejecutar consultas
cursor = conn.cursor()
print(cursor)