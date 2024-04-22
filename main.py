from typing import Union
from fastapi import FastAPI
import pyodbc
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from model import TableName,RowData

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


@app.get("/tableName")
def read_root():
    Table_Name = ['FRMWRKCONFIG.keys','FRMWRKCONFIG.sqlserverdelta','FRMWRKCONFIG.ExcludeHash','FRMWRKCONFIG.projectorchestration','FRMWRKCONFIG.configserver','FRMWRKCONFIG.project']
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
    cursor.execute("SELECT * FROM "+tablename)
    rows = cursor.fetchall()
    tableData = []
    for row in rows:
        lis = []
        for j in row:
            lis.append(j)
        tableData.append(lis)
    cursor.close()
    conn.close()
    return JSONResponse(content={'column':Column,'tableData':tableData},status_code=200)



@app.post("/postdata")
def post_data(row_data: RowData):
    conn = pyodbc.connect(connection_string)
    print("Connected")
    cursor = conn.cursor()
    columnValue = row_data.values
    tableName = row_data.tableName
    columnCount = 0 
    rowCount = 0 
    values = []
    hash = []
    for data in columnValue:
        lis = []
        columnCount = 0 
        hashValue = {}
        count = 0 
        for i,j in data["values"].items():
            ln = len(i)
            if(tableName=="FRMWRKCONFIG.project"):
                if(i=="Project"):
                    hashValue[i] = [j,rowCount]
                elif(i=="ROWID"):
                    hashValue[i] = [j,rowCount]
            else:
                if(i=="Project"):
                    hashValue[i] = [j,rowCount]
                elif(i[ln-2:]=='ID'):
                    hashValue[i] = [j,rowCount]
            columnCount+=1
            count+=1
            lis.append(j)
        hash.append(hashValue)
        values.append(lis)
        rowCount+=1
    for i in hash:
        selectQuery = "SELECT * from "+tableName+" where "
        rowcount = 0 
        for x,y in i.items():
            selectQuery += "{}={} and ".format(x,y[0])
            rowcount = y[1]
        selectQuery = selectQuery[0:len(selectQuery)-4:]
        cursor.execute(selectQuery)
        rows = cursor.fetchall()
        if(len(rows)):
            return JSONResponse(content={'message':'Duplicate key Insertion','Rowcount':rowcount},status_code=202)
    columnValue = "(?"
    for i in range(columnCount-1):
        columnValue+=',?'
    columnValue+=')'
    insert_query = "INSERT INTO {} VALUES {}".format(tableName,columnValue)
    for row in values:
        cursor.execute(insert_query, row)
        conn.commit() 
    cursor.close()
    conn.close()
    return {"message": "Data received successfully"}



