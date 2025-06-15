from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

if TYPE_CHECKING:
    from tfidf.models import Document, Collection

class User(Base):
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    documents: Mapped[list['Document']] = relationship(back_populates='user')
    collections: Mapped[list['Collection']] = relationship(back_populates='user')