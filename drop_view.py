import pyodbc

conns = 'Driver={SQL Server};Server=CRSDWSQLDEV02\SDW_QA;Database=STG_SRVC_WH;Trusted_Connection=yes'
conn = pyodbc.connect(conns)
cursor = conn.cursor()

def execute_sql(sql):
    try:
        cursor.execute(sql)
        conn.commit()
        print(f"Executed SQL:")
    except Exception as e:
        print(f"Error executing SQL:---------------------------------------------------------------------------- {sql}\n{e}")

def drop_view(view_name):
    drop_sql = f"DROP VIEW {view_name};"
    execute_sql(drop_sql)

def drop_tbl(tbl_name):
    drop_tbl = f"DROP table {tbl_name};"
    execute_sql(drop_tbl)

def alter_tbl(tbl_name):
    sql = 'alter tabel CDF.{} rename column EFFECTIVE_DATE TO EFF_DTTM'.format(tbl_name)
    print(sql)
    # try:
    #     cursor.execute(sql)
    #     conn.commit()
    #     print(f"Executed SQL: {sql}")
    # except Exception as e:
    #     print(f"Error executing SQL:---------------------------------------------------------------------------- {sql}\n{e}")
with open(r"C:\\Users\\pr38\\Desktop\\dumpp.txt", 'r') as file:
    content = file.read()

ddl_statements = content.split('\n')
count = 0 
for statement in ddl_statements:
    statements = statement.strip()
    # if statement.startswith("CREATE VIEW"):
    #     view_name = statement.split()[2]
    #     drop_view(view_name)
    if statement.startswith("CREATE TABLE"):
        Tbl_name = statement.split()[2]
        if(Tbl_name[-1]=='('):
            Tbl_name = Tbl_name[0:len(Tbl_name)-1]
        drop_tbl(Tbl_name)
        count+=1
        
        # drop_tbl(Tbl_name)
        # drop_view(view_name)
        # execute_sql(statement + ";")
print(count)
cursor.close()
conn.close()
