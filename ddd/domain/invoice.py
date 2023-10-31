from dataclasses import asdict, dataclass
from typing import Annotated, TypedDict


class Description(TypedDict):
    key: str
    value: Annotated[str, 20]


@dataclass
class Invoice:
    amount: int
    tax_id: str
    name: str
    descriptions: Annotated[list[Description], 15]

    def __repr__(self) -> str:
        return f'Invoice<name="{self.name}", amount={self.amount}, tax_id="{self.tax_id}", descriptions={self.descriptions}>'

    def asdict(self) -> dict:
        return asdict(self)
