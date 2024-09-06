from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from models import HiredEmployee, Department, Job

def get_hired_employees_by_quarter(db: Session):
    
    result = (
        db.query(
            Department.department,
            Job.job,
            extract('quarter', HiredEmployee.datetime).label('quarter'),
            func.count(HiredEmployee.id).label('employee_count')
        )
        .join(HiredEmployee, Department.id == HiredEmployee.department_id)
        .join(Job, Job.id == HiredEmployee.job_id)
        .filter(func.strftime('%Y', HiredEmployee.datetime) == "2021")
        .group_by(Department.department, Job.job, 'quarter')
        .order_by(Department.department, Job.job)
        .all()
    )
    return result
