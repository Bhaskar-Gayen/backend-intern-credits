from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.schemas.schemas import SchemaUpdateRequest, OperationType, ColumnDefinition, SchemaResponse, AddColumnResponse, \
    TableInfoResponse
from app.services.schema_service import SchemaService

router = APIRouter(prefix="/api/schema", tags=["schema"])


@router.post("/update")
async def update_schema(
        request: SchemaUpdateRequest,
        db: AsyncSession = Depends(get_db)
):
    service = SchemaService(db)

    try:
        if request.operation == OperationType.ADD_COLUMN:
            if not request.column_definition:
                raise HTTPException(status_code=400, detail="column_definition required for add_column")

            result = await service.add_column(request.table_name, request.column_definition)
            return AddColumnResponse(
                success=True,
                message="Column added successfully",
                table_name=request.table_name,
                column_added=request.column_definition.name,
                sql_executed=result["sql_executed"]
            )

        elif request.operation == OperationType.DROP_COLUMN:
            if not request.column_name:
                raise HTTPException(status_code=400, detail="column_name required for drop_column")

            result = await service.drop_column(request.table_name, request.column_name)
            return SchemaResponse(
                success=True,
                message="Column dropped successfully",
                operation="drop_column",
                data={"table": request.table_name, "column": request.column_name},
                sql_executed=result["sql_executed"]
            )

        elif request.operation == OperationType.CREATE_TABLE:
            if not request.columns:
                raise HTTPException(status_code=400, detail="columns required for create_table")

            result = await service.create_table(request.table_name, request.columns)
            return SchemaResponse(
                success=True,
                message="Table created successfully",
                operation="create_table",
                data={"table": request.table_name, "columns_count": len(request.columns)},
                sql_executed=result["sql_executed"]
            )

        elif request.operation == OperationType.GET_SCHEMA:
            result = await service.get_table_info(request.table_name)
            return TableInfoResponse(
                success=True,
                table_name=request.table_name,
                columns=result["columns"],
                indexes=result["indexes"]
            )
        return None

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@router.delete("/table/{table_name}/column/{column_name}", response_model=SchemaResponse)
async def drop_column(
        table_name: str,
        column_name: str,
        db: AsyncSession = Depends(get_db)
):
    service = SchemaService(db)

    try:
        result = await service.drop_column(table_name, column_name)
        return SchemaResponse(
            success=True,
            message=f"Column {column_name} dropped from {table_name}",
            operation="drop_column",
            data={"table": table_name, "dropped_column": column_name},
            sql_executed=result["sql_executed"]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tables", response_model=SchemaResponse)
async def get_all_tables(db: AsyncSession = Depends(get_db)):
    service = SchemaService(db)

    try:
        result = await service.get_all_tables()
        return SchemaResponse(
            success=True,
            message="Tables retrieved successfully",
            operation="get_all_tables",
            data={"tables": result["tables"]}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/table/{table_name}", response_model=TableInfoResponse)
async def get_table_schema(
        table_name: str,
        db: AsyncSession = Depends(get_db)
):
    service = SchemaService(db)

    try:
        result = await service.get_table_info(table_name)
        return TableInfoResponse(
            success=True,
            table_name=table_name,
            columns=result["columns"],
            indexes=result["indexes"]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))