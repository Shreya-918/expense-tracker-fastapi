
from ..core.db import Base
from datetime import datetime
from sqlalchemy import Boolean,Column,Integer,String,Float,Date,DateTime


from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey
from datetime import datetime

from ..core.db import Base


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    title = Column(String(50), nullable=False)

    description = Column(String(50), nullable=False)

    show = Column(Boolean, default=True)

    amount = Column(Float, nullable=False)

    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )
    

