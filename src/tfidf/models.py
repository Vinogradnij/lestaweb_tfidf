from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from database import Base
from tfidf.mixins import UserRelationMixin, DocumentRelationMixin, CollectionRelationMixin



class Document(UserRelationMixin, Base):
    _user_back_populates = 'documents'

    path: Mapped[str]
    title: Mapped[str]

    statistics: Mapped[list['Statistic']] = relationship(back_populates='Document')
    collection_document: Mapped[list['Collection_Document']] = relationship(back_populates='Document')

class Collection(UserRelationMixin, Base):
    _user_back_populates = 'collections'


class Collection_Document(DocumentRelationMixin, CollectionRelationMixin, Base):
    _document_back_populates = 'collection_documents'
    _collection_back_populates = 'collection_documents'


class Statistic(DocumentRelationMixin, CollectionRelationMixin, Base):
    _document_back_populates = 'statistics'
    _collection_back_populates = 'statistics'

    word: Mapped[str]
    tf: Mapped[float]
    idf: Mapped[float]