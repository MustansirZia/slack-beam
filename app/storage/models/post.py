from enum import Enum

from sqlalchemy import TEXT, VARCHAR
from sqlalchemy.orm import mapped_column, Mapped

from app.storage.models import Base


class PostType(Enum):
    X = 'X'
    LINKEDIN = 'LI'


class Post(Base):
    __tablename__ = "post"

    id: Mapped[str] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(type_=TEXT, nullable=False)
    type: Mapped[PostType] = mapped_column(type_=VARCHAR(2), nullable=False)

