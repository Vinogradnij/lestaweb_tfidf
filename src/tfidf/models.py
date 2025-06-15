from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from database import Base



class Document(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    path: Mapped[str]
    title: Mapped[str]
