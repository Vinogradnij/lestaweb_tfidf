from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import declared_attr, Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from users.models import User

class UserRelationMixin:
    _user_back_populates: str | None = None

    @declared_attr
    def user_id(cls) -> Mapped[int]:
        return mapped_column(
            ForeignKey('user.id'),
        )

    @declared_attr
    def user(cls) -> Mapped['User']:
        return relationship(
            'User',
            back_populates=cls._user_back_populates
        )

class DocumentRelationMixin:
    _document_back_populates: str | None = None

    @declared_attr
    def document_id(cls) -> Mapped[int]:
        return mapped_column(
            ForeignKey('document.id'),
        )

    @declared_attr
    def document(cls) -> Mapped['User']:
        return relationship(
            'Document',
            back_populates=cls._document_back_populates
        )