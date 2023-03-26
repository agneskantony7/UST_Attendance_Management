from fastapi import FastAPI, status, HTTPException,Depends
from typing import List
from sqlalchemy.orm import Session
import schemas
import models
import database
from database import engine,get_db
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    #allow_headers=["Content-Type"],
)




@app.get('/record/viewattendance/{employee_id}/{company_id}/{year}', status_code=status.HTTP_302_FOUND, response_model=schemas.Response)
def get_record(employee_id: int, company_id: int, year: int, db: Session = Depends(get_db)):
    record = db.query(models.AttendanceReport).filter(models.AttendanceReport.employee_id == employee_id, models.AttendanceReport.company_id == company_id, models.AttendanceReport.year == year).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
    return record
    record_dict = record.__dict__
    record_dict.pop('_sa_instance_state')
    record_dict['company_id'] = company_id
    record_dict['year'] = year
    headers = {
        "Access-Control-Allow-Origin": "*"
    }

    return JSONResponse(content=record_dict, headers=headers)

    #return record_dict



# @app.get('/record/{id}',status_code=status.HTTP_302_FOUND,response_model=schemas.Response)
# def get_record(id: int, db:Session = Depends(get_db)):
#      record = db.query(models.AttendanceReport).filter(models.AttendanceReport.employee_id == id).first()
#      if not record:
#          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
#      return record
from fastapi.responses import JSONResponse
@app.get('/record/view/{company_id}',status_code=status.HTTP_302_FOUND,response_model=List[schemas.Response])
def get_company_record(company_id: int, db:Session = Depends(get_db)):
    record = db.query(models.AttendanceReport).filter(models.AttendanceReport.company_id == company_id).all()
   # record.headers["Access-Control-Allow-Origin"] = "*"
   # response = JSONResponse(record)
    #response.headers["Access-Control-Allow-Origin"] = "*"
    #record[0].headers["Access-Control-Allow-Origin"] = "*"
   # return record
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
    return jsonable_encoder(record)




