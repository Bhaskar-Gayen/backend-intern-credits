from typing import List
from app.schemas.schemas import ColumnDefinition


class SQLGenerator:
    postgres_types_with_size = {"CHAR", "VARCHAR", "BIT", "VARBIT"}
    @staticmethod
    def add_column(table_name: str, column_def: ColumnDefinition) -> str:
        col_type = column_def.type.upper()

        if column_def.size and col_type in SQLGenerator.postgres_types_with_size:
            col_type = f"{col_type}({column_def.size})"

        sql = f"ALTER TABLE {table_name} ADD COLUMN {column_def.name} {col_type}"

        if not column_def.nullable:
            sql += " NOT NULL"

        if column_def.default is not None:
            sql += f" DEFAULT {column_def.default}"

        return sql

    @staticmethod
    def drop_column(table_name: str, column_name: str) -> str:
        return f"ALTER TABLE {table_name} DROP COLUMN {column_name}"

    @staticmethod
    def create_table(table_name: str, columns: List[ColumnDefinition]) -> str:
        """
        Generate CREATE TABLE statement dynamically.
        """
        col_defs = []
        for col in columns:
            col_sql = f"{col.name} {col.type}"
            if col.size:
                col_sql = f"{col.name} {col.type}({col.size})"
            if not col.nullable:
                col_sql += " NOT NULL"
            if col.default is not None:
                col_sql += f" DEFAULT {col.default}"
            col_defs.append(col_sql)

        col_defs_str = ", ".join(col_defs)
        return f"CREATE TABLE {table_name} ({col_defs_str});"
