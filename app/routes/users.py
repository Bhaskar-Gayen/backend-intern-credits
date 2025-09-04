from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.schemas.response import ApiResponse
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService

router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("/", response_model=ApiResponse)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    user = await service.create_user(user_data)
    user_schema = UserResponse.model_validate(user)
    return ApiResponse(success=True, message="User created successfully", data=user_schema)

@router.get("/{user_id}", response_model=ApiResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    user = await service.get_user(user_id)
    user_schema = UserResponse.model_validate(user)
    return ApiResponse(success=True, message="User retrieved successfully", data=user_schema)