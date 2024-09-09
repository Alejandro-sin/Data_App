from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, Path
from starlette import status
from sqlalchemy.orm import Session
from db.database import engine, SessionLocal
from models.models import HiredEmployee, Department, Job
from sqlalchemy import text


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



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# dependency injection
db_dependency = Annotated[Session, Depends(get_db)] 


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



# Retornar la data