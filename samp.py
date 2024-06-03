import pyodbc

# Connect to the SQL Server database
conns = 'Driver={SQL Server};Server=CRSDWSQLDEV02\SDW_QA;Database=STG_SRVC_WH;Trusted_Connection=yes'
conn = pyodbc.connect(conns)
cursor = conn.cursor()

# Function to execute a SQL command
def execute_sql(sql):
    try:
        cursor.execute(sql)
        conn.commit()
        print(f"Executed SQL: {sql}")
    except Exception as e:
        print(f"Error executing SQL:-------------------------------------------------------------------------------------------------- {sql}\n{e}")

# Read the file with DDL statements
with open(r"C:\\Users\\pr38\\Desktop\\test.txt", 'r') as file:
    content = file.read()

# Split the content into individual statements
# Note: splitting by ';\n' can ensure we capture statements that span multiple lines
ddl_statements = content.split(';\n')

# Process each statement
for statement in ddl_statements:
    statement = statement.strip()
    # Only execute CREATE TABLE statements
    if statement.startswith("CREATE TABLE"):
        # Add the semicolon back to the end of the statement if it was removed by split
        execute_sql(statement + ";")
# Close the connection
cursor.close()
conn.close()
