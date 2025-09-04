from typing import Dict, Any, List

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.schemas import ColumnDefinition


class SchemaValidator:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def table_exists(self, table_name: str) -> bool:
        """
        Check if a table exists in the current database schema.
        """
        result = await self.db.execute(
            text("""
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.tables
                WHERE table_name = :table_name
            )
            """)
            ,{"table_name": table_name}
        )
        return result.scalar()

    async def column_exists(self, table_name: str, column_name: str) -> bool:
        """
        Check if a column exists in a given table.
        """
        result = await self.db.execute(
            text("""
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.columns
                WHERE table_name = :table_name
                AND column_name = :column_name
            )
            """),
            {"table_name": table_name, "column_name": column_name}
        )
        return result.scalar()

    async def is_critical_column(self, table_name: str, column_name: str) -> bool:
        """
        Determine if a column is critical (PK or FK).
        """
        # Check primary key
        pk_check = await self.db.execute( text("""
            SELECT kcu.column_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
              ON tc.constraint_name = kcu.constraint_name
            WHERE tc.table_name = :table_name
              AND tc.constraint_type = 'PRIMARY KEY'
              AND kcu.column_name = :column_name
            """),
            {"table_name": table_name, "column_name": column_name}
        )
        if pk_check.first():
            return True

        # Check foreign key
        fk_check = await self.db.execute(
            text("""
            SELECT kcu.column_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
              ON tc.constraint_name = kcu.constraint_name
            WHERE tc.table_name = :table_name
              AND tc.constraint_type = 'FOREIGN KEY'
              AND kcu.column_name = :column_name
            """),
            {"table_name": table_name, "column_name": column_name}
        )
        return bool(fk_check.first())

    async def validate_data_type(self, data_type: str) -> bool:
        """
        Validate if the provided data type is a valid PostgreSQL type.
        """
        result = await self.db.execute( text("""
            SELECT EXISTS (
                SELECT 1
                FROM pg_type
                WHERE typname = :dtype
            )
            """,
            {"dtype": data_type.lower()})
        )
        return result.scalar()

    async def get_table_info(self, table_name: str) -> Dict[str, Any]:
        """
        Get complete information of a table (all columns and their details).
        """
        result = await self.db.execute( text("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_name = :table_name
            """),
            {"table_name": table_name}
        )
        rows = result.fetchall()
        return {
            "table": table_name,
            "columns": [
                {
                    "name": row[0],
                    "type": row[1],
                    "nullable": row[2],
                    "default": row[3],
                }
                for row in rows
            ],
        }

    async def validate_column_definitions(self, columns: List[ColumnDefinition]) -> bool:
        column_names = [col.name for col in columns]
        if len(column_names) != len(set(column_names)):
            raise ValueError("Duplicate column names found")

        for column in columns:
            if not await self.validate_data_type(column.type.value):
                raise ValueError(f"Invalid data type: {column.type.value}")

        return True

    async def get_table_columns(self, table_name: str) -> List[Dict[str, Any]]:
        result = await self.db.execute(
           text( """
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_name = :table_name
            ORDER BY ordinal_position
            """),
            {"table_name": table_name}
        )
        rows = result.fetchall()
        return [
            {
                "name": row[0],
                "type": row[1],
                "nullable": row[2] == "YES",
                "default": row[3]
            }
            for row in rows
        ]

    async def get_table_indexes(self, table_name: str) -> List[str]:
        result = await self.db.execute(
           text( """
            SELECT indexname
            FROM pg_indexes
            WHERE tablename = :table_name
            """),
            {"table_name": table_name}
        )
        rows = result.fetchall()
        return [row[0] for row in rows]

    async def get_table_constraints(self, table_name: str) -> List[Dict[str, Any]]:
        result = await self.db.execute(
            text("""
            SELECT tc.constraint_name, tc.constraint_type, kcu.column_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
              ON tc.constraint_name = kcu.constraint_name
            WHERE tc.table_name = :table_name
            """),
            {"table_name": table_name}
        )
        rows = result.fetchall()
        return [
            {
                "name": row[0],
                "type": row[1],
                "column": row[2]
            }
            for row in rows
        ]

    async def get_all_tables(self) -> List[Dict[str, str]]:
        query = text("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        result = await self.db.execute(query)
        tables = result.scalars().all()
        return [{"table_name": t} for t in tables]

    async def get_column_count(self, table_name: str) -> int:
        query=text(
            """
                       SELECT COUNT(*)
                       FROM information_schema.columns
                       WHERE table_name = :table_name
                       """,
        )
        result = await self.db.execute(query, {"table_name": table_name})
        return result.scalar()

    async def has_primary_key(self, table_name: str) -> bool:
        query = text("""
                    SELECT EXISTS (
                        SELECT 1
                        FROM information_schema.table_constraints
                        WHERE table_name = :table_name
                        AND constraint_type = 'PRIMARY KEY'
                    )
                """)
        result = await self.db.execute(query, {"table_name": table_name})
        return result.scalar()
