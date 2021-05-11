from typing import List

import uvicorn
from fastapi import FastAPI
from sqlalchemy import text, select, or_

from app.db import database, engine, metadata, accounts_table, customers_table, generate_uuid, transfers_table
from app.model import Account, Customer, Transfer, AccountIn

metadata.create_all(engine)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello banking api"}


@app.get("/accounts", response_model=List[Account])
async def get_all_accounts():
    query = accounts_table.select()
    return await database.fetch_all(query)


@app.post("/accounts")
async def create_accounts(account: AccountIn):
    query = accounts_table.insert().values(
        account_no=generate_uuid(),
        balance=account.balance,
        customer_id=account.customer_id)
    last_record_id = await database.execute(query)
    return {**account.dict(), "id": last_record_id}


@app.get("/accounts/balance/{account_no}")
async def get_account_balance(account_no: str):
    q = select([accounts_table.c.balance]).where(accounts_table.c.account_no == account_no)
    result = await database.fetch_one(q)
    return result


@app.post("/customer")
async def create_customer(customer: Customer):
    query = customers_table.insert().values(name=customer.name, age=customer.age)
    last_record_id = await database.execute(query)
    return {**customer.dict(), "id": last_record_id}


@app.get("/customer", response_model=List[Customer])
async def get_all_customer():
    query = customers_table.select()
    return await database.fetch_all(query)


@app.get("/accounts/balance/{account_no}")
async def get_account_balance(account_no: str):
    q = select([accounts_table.c.balance]).where(accounts_table.c.account_no == account_no)
    result = await database.fetch_one(q)
    return result


@app.get("/transfer", response_model=List[Transfer])
async def get_all_transfer():
    query = transfers_table.select()
    return await database.fetch_all(query)


@app.post("/transfer")
async def create_transfer(transfer: Transfer):
    query = transfers_table.insert().values(amount=transfer.amount,
                                            to_account=transfer.to_account,
                                            from_account=transfer.from_account)
    last_record_id = await database.execute(query)
    return {**transfer.dict(), "id": last_record_id}


@app.get("/transfer/history/{account_no}")
async def get_transfer_history(account_no):
    q = transfers_table.select().where(or_(transfers_table.c.to_account == account_no, transfers_table.c.from_account == account_no))
    return await database.fetch_all(q)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


if __name__ == '__main__':
    uvicorn.run(app, port=8000)
