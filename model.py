from pydantic import BaseModel



class TableName(BaseModel):
     tablename : str



class RowData(BaseModel):
    values: list
    tableName : str
