from ..core.db import Base
from datetime import datetime
from sqlalchemy import Boolean,Column,Integer,String,Float,Date,DateTime


from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db import Base


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    firstname: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    lastname: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    age: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )
