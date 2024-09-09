from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import engine, SessionLocal
from models.models import HiredEmployee, Department, Job
from neo4j import GraphDatabase
from scripts.neo4j_scripts import persons_count, most_frequent_job, most_important_department
from streamlit_agraph import agraph, Node, Edge, Config


app = FastAPI(
    title="Mi API",
    description="API que facilita realizar consultas a una base de datos en local Postgresql, y a un grafo en AuraDB",
    version="0.0.1",
    terms_of_service="Free as infinite!",
    contact={
        "name": "Alejandro Giraldo Londoño",
        "url": "https://www.linkedin.com/in/alejandrosin/",
        "email": "alejandro.chem.io@gmail.com",
    },
    license_info={
        "name": "Licencia MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)


# SQL
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# dependency injection
db_dependency = Annotated[Session, Depends(get_db)] 



# NEO4J
def graph_session():
    URI = "neo4j+s://a575d5a9.databases.neo4j.io:7687"
    AUTH = ("neo4j", "yIjVz15ZVDbIFAyjLdA8tjacG-Re7_Cd8G_rY5YesTo")

    with GraphDatabase.driver(URI, auth=AUTH) as driver:    
        return driver


driver = graph_session()
session = driver.session(database="neo4j")


def query_graph(query, parameters=None):    
    with driver.session() as session:
        result = session.run(query, parameters)
        return [record for record in result]





# Retirnar toda la data con un path param
@app.get("/data/{table_name}",
         description="Obtain all registers from database for the input table name 'HiredEmployee', 'Department' or 'Job' ")
async def get_all_from_table(db: db_dependency, table_name: str):
    '''
    Retrieve all records from a specified table in the database.

    Args:
        db (db_dependency): Database session or dependency injected for query execution.
        table_name (str): The name of the table to query (HiredEmployee, Department, or Job).

    Returns:
        list: A list of all records from the specified table.

    Raises:
        HTTPException: 
            - 404: If the specified table name does not match the available options.
            - 400: If the table reference is invalid (None or unrecognized).

    Usage:
        - The table name should be one of the following: "HiredEmployee", "Department", or "Job".
        - If the table name does not match any of these, a 404 error is raised.
        - The function will return all records from the specified table if the query is valid.
    '''
    match table_name:
        case "HiredEmployee":
            table_db = HiredEmployee
        case "Department":
            table_db = Department
        case "Job":
            table_db = Job
        case _:
            raise HTTPException(status_code=404, detail=f"Table {table_name} not found")
    
    if not table_db:
        raise HTTPException(status_code=400, detail="Invalid table reference")

    return db.query(table_db).all()




@app.get("/employees_count", tags=["Data"],
         description="Obtain count of employees by department ")
async def get_number_employees():
    result = query_graph(persons_count)
    return result


@app.get("/most_frequent_job", tags=["Data"])
async def get_most_frequent_job():
    result = query_graph(most_frequent_job)
    return result


@app.get("/most_important_department", tags=["Data"])
async def most_important_department():
    result = query_graph(most_important_department)
    return result




@app.get("/streamlit_agraph")
async def render_streamlit():
 
    relations_and_nodes = """

    MATCH (p:Person)-[h:HOLDS]->(j:Job) RETURN p,h,j

    """
    results = query_graph(relations_and_nodes)

    return results