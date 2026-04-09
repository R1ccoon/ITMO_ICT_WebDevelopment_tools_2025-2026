from enum import Enum


class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


class BudgetPeriod(str, Enum):
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class GoalStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
