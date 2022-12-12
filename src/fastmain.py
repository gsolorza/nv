from fastapi import FastAPI, Depends, HTTPException
from db import SessionLocal, engine
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from typing import Any, Union
import models
import schema
import crud

models.Base.metadata.create_all(bind=engine)


def getDb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


@app.get("/get_user", response_model=schema.UserQuery)
async def get_user(query: schema.Query, db: Session = Depends(getDb)):
    response = crud.get_user(query.column, query.value, db)
    return response


@app.get("/get_role", response_model=Any)
async def get_role(query: schema.Query, db: Session = Depends(getDb)):
    response = crud.get_role(query, db)
    return response


@app.get("/get_form", response_model=schema.Form)
async def get_form(query: schema.Query, db: Session = Depends(getDb)):
    response = crud.get_form(query.column, query.value, db)
    return response


@app.get("/display_partial_form", response_model=list[schema.DisplayForm])
async def display_partial_form(query: schema.Query, db: Session = Depends(getDb)):
    response = crud.display_partial_form(query, db)
    return response


@app.get("/display_full_form", response_model=Any)
async def display_full_form(query: schema.Query, db: Session = Depends(getDb)):
    response = crud.display_full_form(query, db)
    return response


@app.get("/get_user_role", response_model=list[schema.UserQuery])
async def get_user_role(query: schema.Id, db: Session = Depends(getDb)):
    response = crud.get_user_role(query.id, db)
    return response


@app.get("/get_customer", response_model=schema.Customer)
async def get_customer(query: schema.Query, db: Session = Depends(getDb)):
    response = crud.get_customer(query.column, query.value, db)
    return response


@app.get("/get_vendor", response_model=Union[schema.Vendor, schema.Cisco, None])
async def get_vendor(query: schema.Query, db: Session = Depends(getDb)):
    response = crud.get_vendor(query, db)
    return response


@app.post("/create_user", response_model=schema.Message)
async def create_user(users: list[schema.CreateUser], db: Session = Depends(getDb)):
    response = crud.create_user(users, db)
    return response


@app.post("/create_role", response_model=schema.Message)
async def create_role(roles: list[schema.CreateRole], db: Session = Depends(getDb)):
    response = crud.create_role(roles, db)
    return response


@app.post("/create_customer", response_model=schema.Message)
async def create_customer(
    customers: schema.CreateCustomer, db: Session = Depends(getDb)
):
    response = crud.create_customer(customers, db)
    return response


@app.post("/create_vendor", response_model=schema.Message)
async def create_vendor(vendor: Union[schema.CreateVendor, schema.CreateCisco], db: Session = Depends(getDb)):
    response = crud.create_vendor(vendor, db)
    return response


@app.post("/create_form", response_model=schema.Message)
async def create_form(form: schema.CreateForm, db: Session = Depends(getDb)):
    response = crud.create_form(form, db)
    return response


@app.post("/create_software", response_model=schema.Message)
async def create_software(software: schema.CreateSoftware, db: Session = Depends(getDb)):
    response = crud.create_software(software, db)
    return response


@app.post("/update_form", response_model=Any)
async def update_form(value: schema.UpdateForm, db: Session = Depends(getDb)):
    response = crud.update_form(value, db)
    return response


@app.post("/delete_form", response_model=schema.Message)
async def delete_form(id: schema.Id, db: Session = Depends(getDb)):
    response = crud.delete_form(id, db)
    return response
