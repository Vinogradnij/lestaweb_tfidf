from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from database import Base
from tfidf.mixins import UserRelationMixin, DocumentRelationMixin, CollectionRelationMixin



class Document(UserRelationMixin, Base):
    _user_back_populates = 'documents'

    path: Mapped[str]
    title: Mapped[str]

class Collection(UserRelationMixin, Base):
    _user_back_populates = 'collections'


class CollectionDocument(DocumentRelationMixin, CollectionRelationMixin, Base):
    _document_back_populates = 'collection_document'
    _collection_back_populates = 'collection_document'
