from sqlalchemy import Column, Integer, String, DateTime
from db.database import Base


class HiredEmployee(Base):
    __tablename__ = "hired_employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    datetime = Column(DateTime)
    department_id = Column(Integer)
    job_id = Column(Integer)


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    department = Column(String)

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    job = Column(String)