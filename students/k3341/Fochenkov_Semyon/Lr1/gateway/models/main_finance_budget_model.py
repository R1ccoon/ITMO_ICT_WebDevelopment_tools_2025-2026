from sqlalchemy import Sequence, UniqueConstraint, func
from sqlalchemy.schema import ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column

from models._annotations import (
    BigintPrimaryKey,
    DoubleColumn,
    IntegerColumn,
    TimestampColumn,
    VarcharColumn,
)
from models._base_class import Base


class Budget(Base):
    __tablename__ = "finance_budgets"
    __table_args__ = (
        UniqueConstraint("user_id", "category_id", "period"),
        ForeignKeyConstraint(["user_id"], ["users.id"]),
        ForeignKeyConstraint(["category_id"], ["finance_categories.id"]),
    )

    id: Mapped[BigintPrimaryKey] = mapped_column(Sequence("finance_budgets_id_seq"))
    user_id: Mapped[IntegerColumn] = mapped_column(nullable=False)
    category_id: Mapped[IntegerColumn] = mapped_column(nullable=False)
    period: Mapped[VarcharColumn] = mapped_column(nullable=False)  # monthly/weekly
    limit_amount: Mapped[DoubleColumn] = mapped_column(nullable=False)
    spent_amount: Mapped[DoubleColumn] = mapped_column(nullable=False, default=0.0)

    d_create: Mapped[TimestampColumn] = mapped_column(
        nullable=False, default=func.now()
    )
