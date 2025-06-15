from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from database import Base
from tfidf.mixins import UserRelationMixin

if TYPE_CHECKING:
    from users.models import User


class Document(UserRelationMixin, Base):
    _user_back_populates = 'documents'

    path: Mapped[str]
    title: Mapped[str]

