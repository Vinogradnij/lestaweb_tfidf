from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from database import Base

if TYPE_CHECKING:
    from users.models import User


class Document(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    path: Mapped[str]
    title: Mapped[str]

    user: Mapped['User'] = relationship(back_populates='documents')