from sqlalchemy.orm import Session
from typing import Union
from db import SessionLocal, engine
from pprint import pprint
from schema import MessageType
import models
import schema


db = SessionLocal()
models.Base.metadata.create_all(bind=engine)


def get_user(column: str, value: Union[str, int], db: Session):
    query = (
        db.query(models.User.id, models.User.username)
        .filter(models.User.__getattribute__(models.User, column) == value)
        .first()
    )
    user = schema.UserQuery.parse_obj(query)
    return user


def get_role(column: str, value: Union[str, int], db: Session):
    query = (
        db.query(models.Role.id, models.Role.role_name)
        .filter(models.Role.__getattribute__(models.Role, column) == value)
        .first()
    )
    role = schema.RoleQuery.parse_obj(query)
    return role


def get_form(column: str, value: Union[str, int], db: Session):
    query = (
        db.query(models.Form)
        .filter(models.Form.__getattribute__(models.Form, column) == value)
        .first()
    )
    if query:
        form = schema.Form.parse_obj(query.__dict__)
        return form
    return query


def display_partial_form(search: schema.Query, db: Session):
    query = (
        db.query(models.Form.id, models.Form.vendor_deal_id, models.Form.quote_direct,
                 models.Form.sales_force_id, models.Form.purchase_order, models.Form.date, models.Form.status)
        .filter(models.Form.__getattribute__(models.Form, search.column) == search.value)
        .first()
    )
    if query:
        form = schema.DisplayForm.parse_obj(query)
        return form
    return query


def display_full_form(search: schema.Query, db: Session):
    query = (db.query(models.Form, models.Vendor, models.Cisco, models.Software, models.Customer)
             .select_from(models.Form).filter(models.Form.__getattribute__(models.Form, search.column) == search.value)
             .join(models.Vendor, models.Software, models.Cisco, models.Customer)
             .all())
    return query


def get_customer(column: str, value: Union[str, int], db: Session):
    query = (
        db.query(models.Customer)
        .filter(models.Customer.__getattribute__(models.Customer, column) == value)
        .first()
    )
    if query:
        customer = schema.Customer.parse_obj(query.__dict__)
        return customer
    return query


def get_vendor(search: schema.Query, db: Session):
    if search.vendor_cisco:
        query = (
            db.query(models.Cisco)
            .filter(models.Cisco.__getattribute__(models.Cisco, search.column) == search.value)
            .first()
        )
        if query:
            vendor = schema.Cisco.parse_obj(query.__dict__)
            return vendor
    else:
        query = (
            db.query(models.Vendor)
            .filter(models.Vendor.__getattribute__(models.Vendor, search.column) == search.value)
            .first()
        )
        if query:
            vendor = schema.Vendor.parse_obj(query.__dict__)
            return vendor
    return query


def get_user_role(roleId: int, db: Session):
    query = (
        db.query(models.User.id, models.User.username)
        .select_from(models.User)
        .join(models.Role)
        .filter(models.Role.id == roleId)
        .all()
    )
    users = [schema.UserQuery.parse_obj(x).dict() for x in query]
    return users


def update_form_sale_note(value: schema.SaleNote, db: Session):
    query = (
        db.query(models.Form)
        .filter(models.Form.id == value.id)
        .update({models.Form.sale_note: value.sale_note}, synchronize_session=False)
    )
    db.commit()
    return query


def create_user(users: list[schema.CreateUser], db: Session):
    message = schema.Message()
    for user in users:
        query = get_user("username", user.name, db)
        if query:
            message.add(MessageType.alreadyExist, query)
        elif get_role("id", user.role_id, db):
            try:
                new_user = models.User(
                    name=user.name,
                    email=user.email,
                    password=user.password,
                    role_id=user.role_id,
                )
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
                user = schema.UserBase(
                    name=user.name, email=user.email, role_id=user.role_id
                )
                message.add(MessageType.userCreated, user)
            except Exception as error:
                message.add(MessageType.generalError, error)
        else:
            message.add(MessageType.roleNotFound, user.role_id)
    return message


def create_role(roles: list[schema.CreateRole], db: Session):
    message = schema.Message()
    for role in roles:
        query = get_role("role_name", role.role_name, db)
        if query:
            message.add(MessageType.alreadyExist, query)
        else:
            try:
                new_role = models.Role(
                    role_name=role.role_name,
                )
                db.add(new_role)
                db.commit()
                db.refresh(new_role)
                message.add(MessageType.userCreated, role)
            except Exception as error:
                message.add(MessageType.generalError, error)
    return message


def create_form(form: schema.CreateForm, db: Session):
    message = schema.Message()
    query = get_form("quote_direct", form.quote_direct, db)
    if query:
        message.add(MessageType.alreadyExist, query)
    else:
        try:
            new_form = models.Form(
                sales_force_id=form.sales_force_id,
                vendor_deal_id=form.vendor_deal_id,
                purchase_order=form.purchase_order,
                quote_direct=form.quote_direct,
                client_manager_name=form.client_manager_name,
                pre_sales_name=form.pre_sales_name,
                customer_id=form.customer_id,
                cisco_id=form.cisco_id,
                vendor_id=form.vendor_id,
                software_id=form.software_id,
                comments=form.comments,
                status=form.status,
                date=form.date,
                sale_note=form.sale_note,
            )
            db.add(new_form)
            db.commit()
            db.refresh(new_form)
            message.add(MessageType.formCreated, new_form)
        except Exception as error:
            message.add(MessageType.generalError, error)
    return message


def create_customer(customer: schema.CreateCustomer, db: Session):
    message = schema.Message()
    if get_customer("customer_rut", customer.customer_rut, db):
        message.add(MessageType.alreadyExist, customer.customer_rut)
    else:
        try:
            new_customer = models.Customer(
                customer_name=customer.customer_name,
                customer_rut=customer.customer_rut,
                customer_address=customer.customer_address,
                customer_contact_name=customer.customer_contact_name,
                customer_contact_phone=customer.customer_contact_phone,
                customer_contact_email=customer.customer_contact_email,
                dispatch_address=customer.dispatch_address,
                dispatch_receiver_name=customer.dispatch_receiver_name,
                dispatch_receiver_phone=customer.dispatch_receiver_phone,
                dispatch_receiver_email=customer.dispatch_receiver_email,
            )
            db.add(new_customer)
            db.commit()
            db.refresh(new_customer)
            message.add(MessageType.customerCreated, new_customer)
        except Exception as error:
            message.add(MessageType.generalError, error)
    return message


def create_vendor(vendor: Union[schema.CreateVendor, schema.CreateCisco], db: Session):
    message = schema.Message()
    if isinstance(vendor, schema.CreateVendor):
        try:
            new_vendor = models.Vendor(
                vendor_name=vendor.vendor_name,
                account_manager_name=vendor.account_manager_name,
                account_manager_phone=vendor.account_manager_phone,
                account_manager_email=vendor.account_manager_email
            )
            db.add(new_vendor)
            db.commit()
            db.refresh(new_vendor)
            message.add(MessageType.vendorCreated, new_vendor)
        except Exception as error:
            message.add(MessageType.generalError, error)
    else:
        try:
            new_vendor = models.Cisco(
                account_manager_name=vendor.account_manager_name,
                account_manager_phone=vendor.account_manager_phone,
                account_manager_email=vendor.account_manager_email,
                smart_account=vendor.smart_account,
                virtual_account=vendor.virtual_account,
            )
            db.add(new_vendor)
            db.commit()
            db.refresh(new_vendor)
            message.add(MessageType.vendorCreated, new_vendor)
        except Exception as error:
            message.add(MessageType.generalError, error)
    return message


def create_software(software: schema.CreateSoftware, db: Session):
    message = schema.Message()
    try:
        new_software = models.Software(
            software_type=software.software_type,
            duration_time=software.duration_time,
            customer_contact=software.customer_contact,
            subscription_id=software.subscription_id,
            start_date=software.start_date,
            type_of_purchase=software.type_of_purchase
        )
        db.add(new_software)
        print(db.commit())
        db.refresh(new_software)
        message.add(MessageType.softwareCreated, new_software)
    except Exception as error:
        message.add(MessageType.generalError, error)
    return message
