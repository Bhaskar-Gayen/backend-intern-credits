from typing import Union, Dict, Any, List, Optional

from pydantic import BaseModel
from enum import Enum


class OperationType(str, Enum):
    ADD_COLUMN = "add_column"
    DROP_COLUMN = "drop_column"
    CREATE_TABLE = "create_table"
    GET_SCHEMA = "get_schema"

class PostgreSQLType(str, Enum):
    INTEGER = "INTEGER"
    VARCHAR = "VARCHAR"
    TEXT = "TEXT"
    BOOLEAN = "BOOLEAN"
    TIMESTAMP = "TIMESTAMP"
    DECIMAL = "DECIMAL"

class SchemaResponse(BaseModel):
    success: bool
    message: str
    operation: str
    data: Union[Dict[str, Any], List[Dict], str, None] = None
    sql_executed: Optional[str] = None
    warnings: List[str] = []

class AddColumnResponse(BaseModel):
    success: bool
    message: str
    table_name: str
    column_added: str
    sql_executed: str

class TableInfoResponse(BaseModel):
    success: bool
    table_name: str
    columns: List[Dict[str, Any]]
    indexes: List[str]


class ColumnDefinition(BaseModel):
    name: str
    type: PostgreSQLType
    size: Optional[int] = None
    nullable: bool = True
    default: Optional[Union[str, int, bool]] = None
    unique: bool = False

class SchemaUpdateRequest(BaseModel):
    operation: OperationType
    table_name: str
    column_definition: Optional[ColumnDefinition] = None
    column_name: Optional[str] = None