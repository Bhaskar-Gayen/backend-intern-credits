from pydantic import BaseModel
from typing import Any, Optional, TypeVar, Generic

T=TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    data: Optional[Any] = None
    error: Optional[str] = None

