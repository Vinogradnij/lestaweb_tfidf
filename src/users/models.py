from sqlalchemy.orm import Mapped, mapped_column

from database import Base

class User(Base):
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]