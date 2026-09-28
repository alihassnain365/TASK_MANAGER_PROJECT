from sqlalchemy.orm import DeclarativeBase,Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from database import engine

class Base(DeclarativeBase):
    pass

class User(Base):
    """Models user's table"""
    __tablename__ = "users"

    # coulumns
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str]
    user_name: Mapped[str] = mapped_column(unique=True) 
    hashed_password: Mapped[str]

    # relationshipp columns
    tasks: Mapped[list["Task"]] = relationship(back_populates="user")


class Task(Base):
    """Models tasks table"""
    __tablename__ = "tasks"
    # columns
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    status: Mapped[bool]

    # fk columns
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id))

    # relationship columns
    user: Mapped["User"] = relationship(back_populates="tasks")


Base.metadata.create_all(engine) 
