from pydantic import BaseModel
from typing import List,Any



class TableName(BaseModel):
     tablename : str



class RowData(BaseModel):
    values: list
    tableName : str


class UpdateValue(BaseModel):
     TableName : str 
     ColumnName : list
     key : list
     datas: List[Any]


