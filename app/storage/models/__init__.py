from datetime import datetime

from sqlalchemy import DATETIME
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(type_=DATETIME, default=datetime.now)

