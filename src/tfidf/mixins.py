from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import declared_attr, Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from users.models import User
    from tfidf.models import Document, Collection


class UserRelationMixin:
    _user_back_populates: str | None = None

    @declared_attr
    def user_id(cls) -> Mapped[int]:
        return mapped_column(
            ForeignKey('user.id', ondelete='cascade'),
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
            ForeignKey('document.id', ondelete='cascade'),
        )

    @declared_attr
    def document(cls) -> Mapped['Document']:
        return relationship(
            'Document',
            back_populates=cls._document_back_populates
        )


class CollectionRelationMixin:
    _collection_back_populates: str | None = None

    @declared_attr
    def collection_id(cls) -> Mapped[int]:
        return mapped_column(
            ForeignKey('collection.id', ondelete='cascade'),
        )

    @declared_attr
    def collection(cls) -> Mapped['Collection']:
        return relationship(
            'Collection',
            back_populates=cls._collection_back_populates
        )
