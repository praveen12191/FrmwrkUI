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

# try:
#     conn = pyodbc.connect(connection_string)
#     print("Connected")
#     cursor = conn.cursor()

#     FRMWRKCONFIG_keys_Column = []
#     Keys_Column = cursor.execute("SELECT TOP 0 * FROM FRMWRKCONFIG.keys")
#     for column in Keys_Column.description:
#         FRMWRKCONFIG_keys_Column.append(column)
    
#     FRMWRKCONFIG_sqlserverdelta_Column = []
#     Sqlserverdelta_Column = cursor.execute("SELECT TOP 0 * FROM FRMWRKCONFIG.sqlserverdelta")
#     for column in Sqlserverdelta_Column.description:
#         FRMWRKCONFIG_sqlserverdelta_Column.append(column)
    
#     FRMWRKCONFIG_filter_Column = []
#     Filter_Column = cursor.execute("SELECT TOP 0 * FROM FRMWRKCONFIG.sqlserverdelta")
#     for column in Filter_Column.description:
#         FRMWRKCONFIG_filter_Column.append(column)
    
#     FRMWRKCONFIG_ExcludeHash_Column = []
#     ExcludeHash_Column = cursor.execute("SELECT TOP 0 * FROM FRMWRKCONFIG.ExcludeHash")
#     for column in ExcludeHash_Column.description:
#         FRMWRKCONFIG_ExcludeHash_Column.append(column)
    
#     FRMWRKCONFIG_projectorchestration_Column = []
#     projectorchestration_Column = cursor.execute("SELECT TOP 0 * FROM FRMWRKCONFIG.projectorchestration")
#     for column in projectorchestration_Column.description:
#         FRMWRKCONFIG_projectorchestration_Column.append(column)
    
#     FRMWRKCONFIG_configserver_Column = []
#     configserver_Column = cursor.execute("SELECT TOP 0 * FROM FRMWRKCONFIG.configserver")
#     for column in configserver_Column.description:
#         FRMWRKCONFIG_configserver_Column.append(column)




    # Don't forget to close the cursor and connection when you're done
#     cursor.close()
#     conn.close()

# except pyodbc.Error as e:
#     print(f"Error connecting to SQL Server: {str(e)}")



@app.get("/tableName")
def read_root():
    Table_Name = ['FRMWRKCONFIG.keys','FRMWRKCONFIG.sqlserverdelta','FRMWRKCONFIG.sqlserverdelta','FRMWRKCONFIG.ExcludeHash','FRMWRKCONFIG.projectorchestration','FRMWRKCONFIG.configserver']
    return Table_Name


