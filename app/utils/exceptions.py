from fastapi import HTTPException, status
from pydantic import EmailStr


class UserNotFound(HTTPException):
    def __init__(self, user_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
class EmailIdAlreadyExist(HTTPException):
    def __init__(self, email:EmailStr):
        super().__init__(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"Email Id {email} already exist"
        )

class InsufficientCredits(HTTPException):
    def __init__(self, current_credits: int, requested: int):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient credits. Current: {current_credits}, Requested: {requested}"
        )

class InvalidAmount(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Amount must be positive"
        )

