from uuid import uuid4

from databases import Database
from sqlalchemy import Table, Column, Integer, ForeignKey, Float, DateTime, func, String, create_engine, MetaData

metadata = MetaData()
DATABASE_URL = "sqlite:///./test.db"
database = Database(DATABASE_URL)


def generate_uuid():
    return str(uuid4())


customers_table = Table(
    "customer",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
    Column("age", Integer)
)

accounts_table = Table(
    "account",
    metadata,
    Column("account_no", String(50), primary_key=True),
    Column("customer_id", Integer, ForeignKey('customer.id')),
    Column("balance", Float),
    Column("creation_date", DateTime, default=func.now(), nullable=False),
)

transfers_table = Table(
    "transfer",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("amount", Float),
    Column("from_account", Integer, ForeignKey('account.account_no')),
    Column("to_account", Integer, ForeignKey('account.account_no')),
    Column("date", DateTime, default=func.now(), nullable=False),
)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
