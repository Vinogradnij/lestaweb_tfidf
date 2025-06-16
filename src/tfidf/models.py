from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import UniqueConstraint

from database import Base
from tfidf.mixins import UserRelationMixin, DocumentRelationMixin, CollectionRelationMixin


class Document(UserRelationMixin, Base):
    _user_back_populates = 'documents'

    path: Mapped[str]
    title: Mapped[str]

    statistics: Mapped[list['Statistic']] = relationship(back_populates='document')
    collection_documents: Mapped[list['Collection_Document']] = relationship(back_populates='document')


class Collection(UserRelationMixin, Base):
    _user_back_populates = 'collections'

    statistics: Mapped[list['Statistic']] = relationship(back_populates='collection')
    collection_documents: Mapped[list['Collection_Document']] = relationship(back_populates='collection')


class Collection_Document(DocumentRelationMixin, CollectionRelationMixin, Base):
    _document_back_populates = 'collection_documents'
    _collection_back_populates = 'collection_documents'

    __table_args__ = (
        UniqueConstraint('document_id', 'collection_id', name='unique_document_collection'),
    )


class Statistic(DocumentRelationMixin, CollectionRelationMixin, Base):
    _document_back_populates = 'statistics'
    _collection_back_populates = 'statistics'

    word: Mapped[str]
    tf: Mapped[float]
    idf: Mapped[float]

    __table_args__ = (
        UniqueConstraint('document_id', 'collection_id', 'word', name='unique_document_collection_word'),
    )