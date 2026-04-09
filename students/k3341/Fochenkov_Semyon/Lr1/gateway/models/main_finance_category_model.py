from sqlalchemy import Sequence, UniqueConstraint, func
from sqlalchemy.schema import ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column

from models._annotations import (
    BigintPrimaryKey,
    BoolColumn,
    IntegerColumn,
    TimestampColumn,
    VarcharColumn,
)
from models._base_class import Base


class Category(Base):
    __tablename__ = "finance_categories"
    __table_args__ = (
        UniqueConstraint("user_id", "name", "direction"),
        ForeignKeyConstraint(["user_id"], ["users.id"]),
    )

    id: Mapped[BigintPrimaryKey] = mapped_column(Sequence("finance_categories_id_seq"))
    user_id: Mapped[IntegerColumn] = mapped_column(nullable=False)
    name: Mapped[VarcharColumn] = mapped_column(nullable=False)
    direction: Mapped[VarcharColumn] = mapped_column(nullable=False)  # income/expense
    is_system: Mapped[BoolColumn] = mapped_column(nullable=False, default=False)

    d_create: Mapped[TimestampColumn] = mapped_column(
        nullable=False, default=func.now()
    )
