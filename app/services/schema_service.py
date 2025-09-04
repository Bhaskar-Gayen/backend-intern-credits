from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any

from app.schemas.schemas import ColumnDefinition
from app.utils import TableAlreadyExists
from app.utils.schema_exception import TableNotFound, ColumnAlreadyExists, ColumnNotFound, CriticalColumnError
from app.utils.schema_validator import SchemaValidator
from app.utils.sql_generator import SQLGenerator


class SchemaService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.validator = SchemaValidator(db)
        self.generator = SQLGenerator()

    async def add_column(self, table_name: str, column_def: ColumnDefinition):

        if not await self.validator.table_exists(table_name):
            raise TableNotFound(table_name)


        if await self.validator.column_exists(table_name, column_def.name):
            raise ColumnAlreadyExists(column_def.name)


        sql = self.generator.add_column(table_name, column_def)
        await self.db.execute(text(sql))
        await self.db.commit()

        return {"sql_executed": sql, "table_name": table_name}

    async def drop_column(self, table_name: str, column_name: str):
        # 1. Validate table exists
        if not await self.validator.table_exists(table_name):
            raise TableNotFound(table_name)

        # 2. Validate column exists
        if not await self.validator.column_exists(table_name, column_name):
            raise ColumnNotFound(column_name)

        # 3. Check if column is critical (primary key, foreign key)
        if await self.validator.is_critical_column(table_name, column_name):
            raise CriticalColumnError(column_name)

        # 4. Generate and execute SQL
        sql = self.generator.drop_column(table_name, column_name)
        await self.db.execute(text(sql))
        await self.db.commit()

        return {"sql_executed": sql, "table_name": table_name, "column_name": column_name}

    async def create_table(self, table_name: str, columns: List[ColumnDefinition]):
        # 1. Validate table doesn't exist
        if await self.validator.table_exists(table_name):
            raise TableAlreadyExists(table_name)

        # 2. Validate column definitions
        await self.validator.validate_column_definitions(columns)

        # 3. Generate and execute SQL
        sql = self.generator.create_table(table_name, columns)
        await self.db.execute(text(sql))
        await self.db.commit()

        return {"sql_executed": sql, "table_name": table_name, "columns_count": len(columns)}


    async def get_table_info(self, table_name: str) -> Dict[str, Any]:

        if not await self.validator.table_exists(table_name):
            raise TableNotFound(table_name)


        columns = await self.validator.get_table_columns(table_name)


        indexes = await self.validator.get_table_indexes(table_name)


        constraints = await self.validator.get_table_constraints(table_name)

        return {
            "table_name": table_name,
            "columns": columns,
            "indexes": indexes,
            "constraints": constraints
        }

    async def get_all_tables(self) -> Dict[str, Any]:

        tables = await self.validator.get_all_tables()

        table_list = []
        for table in tables:
            table_info = {
                "table_name": table["table_name"],
                "column_count": await self.validator.get_column_count(table["table_name"]),
                "has_primary_key": await self.validator.has_primary_key(table["table_name"])
            }
            table_list.append(table_info)

        return {"tables": table_list}

