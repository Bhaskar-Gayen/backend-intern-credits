from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db
from app.schemas import CreditUpdate
from app.services.credit_service import CreditService
from app.schemas.credit import CreditAmount, CreditResponse
from app.schemas.response import  ApiResponse

router = APIRouter(prefix="/api/credits", tags=["credits"])

@router.get("/{user_id}", response_model=CreditResponse)
async def get_credit_balance(user_id: int, db: AsyncSession = Depends(get_db)):
    service = CreditService(db)
    return await service.get_credit_balance(user_id)

@router.post("/{user_id}/add", response_model=ApiResponse)
async def add_credits(user_id: int, amount_data: CreditAmount, db: AsyncSession = Depends(get_db)):
    service = CreditService(db)
    credit = await service.add_credits(user_id, amount_data.amount)
    credit_schema=CreditUpdate.model_validate(credit)
    return ApiResponse(success=True, message="Credits added successfully", data=credit_schema)

@router.post("/{user_id}/deduct", response_model=ApiResponse)
async def deduct_credits(user_id: int, amount_data: CreditAmount, db: AsyncSession = Depends(get_db)):
    service = CreditService(db)
    credit = await service.deduct_credits(user_id, amount_data.amount)
    credit_schema = CreditUpdate.model_validate(credit)
    return ApiResponse(success=True, message="Credits deducted successfully", data=credit_schema)

@router.patch("/{user_id}/reset", response_model=ApiResponse)
async def reset_credits(user_id: int, db: AsyncSession = Depends(get_db)):
    service = CreditService(db)
    credit = await service.reset_credits(user_id)
    credit_schema = CreditUpdate.model_validate(credit)
    return ApiResponse(success=True, message="Credits reset successfully", data=credit_schema)