from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base

class User(Base):
    login: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]