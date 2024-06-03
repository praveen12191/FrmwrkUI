import pyodbc


conns = 'Driver={SQL Server};Server=CRSDWSQLDEV02\SDW_QA;Database=STG_SRVC_WH;Trusted_Connection=yes'
conn = pyodbc.connect(conns)
cursor = conn.cursor()


def execute_sql(sql):
    try:
        cursor.execute(sql)
        conn.commit()
        print(f"Executed SQL:-------")
    except Exception as e:
        print(f"Error executing SQL:-------------------------------------------------------------------------------------------------- {sql}\n{e}")



with open(r"C:\\Users\\pr38\\Desktop\\dumpp.txt", 'r') as file:
    content = file.read()


ddl_statements = content.split(';\n')

for statement in ddl_statements:
    statement = statement.strip()
    if statement.startswith("CREATE TABLE"):
        execute_sql(statement + ";")
    if statement.startswith("CREATE VIEW"):
        execute_sql(statement+ ";")
cursor.close()
conn.close()
