from fastapi import FastAPI,Response, status, HTTPException, UploadFile,File,Depends, Request, Form
from process1 import data_filter,read_data
from processing import calculate_working_days,self
from concurrent.futures import ThreadPoolExecutor
from sqlalchemy.orm import Session
import models
from database import engine,get_db,SessionLocal
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import asyncio

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = [
    "http://localhost:63342",
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000/uploadfile/",
    "http://localhost:63342/",
    "http://localhost:8000/uploadfile/"

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    #allow_headers=["Content-Type"],
)

# templates = Jinja2Templates(directory="templates")
def process_file(file: UploadFile):
    df = read_data(file)
    df = df[~df['in_time'].isin([None, '', ' ', 'L', 'Leave']) & ~df['out_time'].isin([None, '', ' ', 'L', 'Leave'])]
    employee_attendance = df.groupby(['company_id', 'employee_id']).apply(
        lambda x: x[['company_id', 'employee_id', 'employee_name', 'in_time', 'out_time']].values.tolist())
    with ThreadPoolExecutor(max_workers=4) as executor:
         executor.map(data_filter, employee_attendance.items())


@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    await asyncio.sleep(5)
    process_file(file)
    self()
    response = JSONResponse(content={"filename": file.filename, "status": "uploaded successfully"})
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


