from sqlalchemy.orm import Mapped, mapped_column

from database import Base

class User(Base):
    login: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]