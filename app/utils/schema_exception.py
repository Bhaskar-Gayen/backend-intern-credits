from fastapi import HTTPException


class SchemaException(HTTPException):
    pass

class TableNotFound(SchemaException):
    def __init__(self, table_name: str):
        super().__init__(
            status_code=404,
            detail=f"Table '{table_name}' does not exist"
        )


class ColumnNotFound(HTTPException):
    def __init__(self, column_name: str):
        super().__init__(
            status_code=404,
            detail=f"Column '{column_name}' not found"
        )


class ColumnAlreadyExists(SchemaException):
    def __init__(self, column_name: str):
        super().__init__(
            status_code=409,
            detail=f"Column '{column_name}' already exists"
        )

class CriticalColumnError(SchemaException):
    def __init__(self, column_name: str):
        super().__init__(
            status_code=403,
            detail=f"Cannot drop critical column '{column_name}'"
        )

class TableAlreadyExists(HTTPException):
    def __init__(self, table_name: str):
        super().__init__(
            status_code=409,
            detail=f"Table '{table_name}' already exists"
        )