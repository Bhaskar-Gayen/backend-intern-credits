from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped

from app.core.database import Base


class Credit(Base):
    __tablename__ = "credits"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    credits: Mapped[int] = Column(Integer, default=0)
    last_updated = Column(DateTime, default=datetime.now)