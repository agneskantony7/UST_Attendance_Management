from pydantic import BaseModel
from datetime import datetime

class Employee_Details(BaseModel):
    company_id: int
    employee_id: int
    employee_name: str
    in_time: datetime
    out_time: datetime

    class Config:
        orm_mode = True

