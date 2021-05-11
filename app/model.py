from pydantic import BaseModel
from pydantic.schema import datetime


class Account(BaseModel):
    account_no: str
    customer_id: int
    balance: float
    creation_date: datetime


class AccountIn(BaseModel):
    customer_id: int
    balance: float


class Customer(BaseModel):
    name: str
    age: int


class Transfer(BaseModel):
    amount: float
    from_account: str
    to_account: str
