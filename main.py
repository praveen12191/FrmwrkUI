from typing import Union
from fastapi import FastAPI
import pyodbc
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from model import TableName,RowData,UpdateValue

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

# columnValue = []

# @app.get("/tableName")
# def read_root():
#     Table_Name = ['FRMWRKCONFIG.keys','FRMWRKCONFIG.sqlserverdelta','FRMWRKCONFIG.ExcludeHash','FRMWRKCONFIG.projectorchestration','FRMWRKCONFIG.configserver','FRMWRKCONFIG.project']
#     return Table_Name

# @app.post("/columnName")
# def columnName(value : TableName):
#     conn = pyodbc.connect(connection_string)
#     print("Connected")
#     cursor = conn.cursor()
#     tablename = value.tablename
#     Column,columnDic,ctr = [],{},0
#     for column in cursor.execute("SELECT TOP 0 * FROM {}".format(tablename)).description:
#         columnDic[ctr] = column[0] 
#         ctr+=1
#         Column.append(column[0])
#     print(columnDic)
#     cursor.execute("SELECT * FROM "+tablename)
#     rows = cursor.fetchall()
#     tableData,dic = [],{}
#     for row in rows:
#         lis,ctr = [],0
#         for j in row:
#             if(columnDic[ctr] not in dic and j):
#                 dic[columnDic[ctr]] = [j]
#             else:
#                 if(j not in dic[columnDic[ctr]] and j):
#                     dic[columnDic[ctr]].append(j)
#             ctr+=1
#             lis.append(j)
#         tableData.append(lis)
#     cursor.close()
#     conn.close()
#     return JSONResponse(content={'column':Column,'tableData':tableData,'uniqueDate':dic},status_code=200)



# @app.post("/postdata")
# def post_data(row_data: RowData):
#     conn = pyodbc.connect(connection_string)
#     cursor = conn.cursor()
#     columnValue = row_data.values
#     tableName = row_data.tableName
#     columnCount = 0 
#     rowCount = 0 
#     values = []
#     hash = []
#     for data in columnValue:
#         lis = []
#         columnCount = 0 
#         hashValue = {}
#         count = 0 
#         for i,j in data["values"].items():
#             ln = len(i)
#             if(tableName=="FRMWRKCONFIG.project"):
#                 if(i=="Project"):
#                     hashValue[i] = [j,rowCount]
#                 elif(i=="ROWID"):
#                     hashValue[i] = [j,rowCount]
#             else:
#                 if(i=="Project"):
#                     hashValue[i] = [j,rowCount]
#                 elif(i[ln-2:]=='ID'):
#                     hashValue[i] = [j,rowCount]
    
#             columnCount+=1
#             count+=1
#             lis.append(j)
#         hash.append(hashValue)
#         values.append(lis)
#         rowCount+=1
#     columnValue = []
#     for i in hash:
#         selectQuery = "SELECT * from "+tableName+" where "
#         rowcount = 0 
#         key = []
#         for x,y in i.items():
#             selectQuery += "{}='{}' and ".format(x,y[0])
#             key.append(y[0])
#             rowcount = y[1]
#         selectQuery = selectQuery[0:len(selectQuery)-4:]
#         val = []
#         for data in values:
#             for x in key:
#                 if(x in data):
#                     val = data
#         cursor.execute(selectQuery)
#         rows = cursor.fetchall()
#         if(rows):
#             return JSONResponse(content={'message':'Duplicate key Insertion','Rowcount':rowcount,'keys':key,'datas':val},status_code=202)
#     for i in hash:
#         columnValue = "(?"
#         for i in range(columnCount-1):
#             columnValue+=',?'
#         columnValue+=')'
#         insert_query = "INSERT INTO {} VALUES {}".format(tableName,columnValue)
#         for row in values:
#             cursor.execute(insert_query, row)
#             conn.commit() 
#         cursor.close()
#         conn.close()
#         return {"message": "Data received successfully"}
    


# @app.post('/updatedata')
# def updateData(data : UpdateValue):
#     tableName = data.TableName
#     columnName = data.ColumnName
#     key = data.key
#     val = data.datas
#     print(tableName,columnName,key,val)
  
#     conn = pyodbc.connect(connection_string)
#     cursor = conn.cursor()
#     ctr = 0 
#     query = "update {} set ".format(tableName)
#     for cl in columnName:
#         query+= cl +"=" + "'"+str(val[ctr])+"'" +" , "
#         ctr+=1
#     server = val[0]
#     dbID = val[1]
#     l = len(query)
#     query = query[0:l-3]
#     query+=" where Project = '{}' and keyID = {}".format(server,dbID)
#     print(query)
#     try:
#         cursor.execute(query)
#         conn.commit()  # Don't forget to commit changes
#         return JSONResponse(content={'message':'Data get updated'},status_code=200)
#     except Exception as e:
#         print("Error:", e)
#         return JSONResponse(content={'message':'Error updating data'},status_code=500)  # Provide feedback about the error




import pyodbc



# Connect to the SQL Server database
conn = 'Driver={SQL Server};Server=CRSDWSQLDEV02\SDW_QA;Database=STG_SRVC_WH;Trusted_Connection=yes'
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

# Function to execute a SQL command
def execute_sql(sql):
    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print(f"Error executing SQL: {sql}\n{e}")

# Function to drop a view if it exists
def drop_view(view_name):
    drop_sql = f"IF OBJECT_ID('{view_name}', 'V') IS NOT NULL DROP VIEW {view_name};"
    execute_sql(drop_sql)

# Read the file with DDL statements
with open('path_to_your_file.txt', 'r') as file:
    content = file.read()

# Split the content into sets of DDL statements (assuming sets are separated by a delimiter)
ddl_sets = content.split('---')  # Assuming '---' is used to separate the sets in your file

# Process each set of DDL statements
for ddl_set in ddl_sets:
    statements = ddl_set.strip().split(';')  # Split statements by semicolon
    if len(statements) < 3:
        print(f"Skipping invalid DDL set: {ddl_set}")
        continue
    
    ddl1 = statements[0].strip()
    ddl2 = statements[1].strip()
    view_creation = statements[2].strip()

    # Execute the two DDL statements
    execute_sql(ddl1)
    execute_sql(ddl2)

    # Extract the view name from the creation statement (assuming a simple CREATE VIEW statement)
    view_name = view_creation.split()[2]

    # Drop the view if it exists and then create the view
    drop_view(view_name)
    execute_sql(view_creation)

# Close the connection
cursor.close()
conn.close()
