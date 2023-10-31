from dataclasses import dataclass, asdict
from enum import Enum


class AccountType(Enum):
    CHECKING = "checking"
    PAYMENT = "payment"
    SAVINGS = "savings"
    SALARY = "salary"


@dataclass
class Transfer:
    amount: int
    name: str
    tax_id: str
    bank_code: str
    branch_code: str
    account_number: str
    account_type: AccountType

    def asdict(self) -> dict:
        return asdict(self)
