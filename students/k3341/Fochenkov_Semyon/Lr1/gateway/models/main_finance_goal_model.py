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


class FinancialGoal(Base):
    __tablename__ = "finance_goals"
    __table_args__ = (
        UniqueConstraint("user_id", "name"),
        ForeignKeyConstraint(["user_id"], ["users.id"]),
    )

    id: Mapped[BigintPrimaryKey] = mapped_column(Sequence("finance_goals_id_seq"))
    user_id: Mapped[IntegerColumn] = mapped_column(nullable=False)
    name: Mapped[VarcharColumn] = mapped_column(nullable=False)
    target_amount: Mapped[DoubleColumn] = mapped_column(nullable=False)
    current_amount: Mapped[DoubleColumn] = mapped_column(nullable=False, default=0.0)
    deadline: Mapped[TimestampColumn] = mapped_column(nullable=True)
    status: Mapped[VarcharColumn] = mapped_column(nullable=False, default="active")

    d_create: Mapped[TimestampColumn] = mapped_column(
        nullable=False, default=func.now()
    )
