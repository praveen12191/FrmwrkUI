from typing import Union
from fastapi import FastAPI
import pyodbc
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI()
connection_string = 'Driver={SQL Server};Server=CRSDWSQLDEV02\SDW_QA;Database=STG_SRVC_WH;Trusted_Connection=yes'

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TableName(BaseModel):
     tablename : str

@app.get("/tableName")
def read_root():
    Table_Name = ['FRMWRKCONFIG.keys','FRMWRKCONFIG.sqlserverdelta','FRMWRKCONFIG.sqlserverdelta','FRMWRKCONFIG.ExcludeHash','FRMWRKCONFIG.projectorchestration','FRMWRKCONFIG.configserver']
    return Table_Name

@app.post("/columnName")
def columnName(value : TableName):
    conn = pyodbc.connect(connection_string)
    print("Connected")
    cursor = conn.cursor()
    tablename = value.tablename
    Column = []
    for column in cursor.execute("SELECT TOP 0 * FROM {}".format(tablename)).description:
        Column.append(column[0])
    cursor.close()
    conn.close()
    return JSONResponse(content=Column,status_code=200)


class RowData(BaseModel):
    values: list
    tableName : str

@app.post("/postdata")
def post_data(row_data: RowData):
    conn = pyodbc.connect(connection_string)
    print("Connected")
    cursor = conn.cursor()
    columnValue = row_data.values
    tableName = row_data.tableName
    columnCount = 0 
    print(columnValue)
    values = []
    for data in columnValue:
        lis = []
        columnCount = 0 
        for i,j in data["values"].items():
            columnCount+=1
            lis.append(j)
        values.append(lis)
    print(columnCount)
    columnValue = "(?"
    for i in range(columnCount-1):
        columnValue+=',?'
    columnValue+=')'
    insert_query = "INSERT INTO {} VALUES {}".format(tableName,columnValue)
    print(insert_query)
    print(values)
    for row in values:
        cursor.execute(insert_query, row)
        conn.commit() 
    cursor.close()
    conn.close()
    return {"message": "Data received successfully"}


