from sqlalchemy.orm import Session
from forms import ChecklistFormSales, Vendor, Cisco, Software
from typing import Union
from schema import MessageType
import models
import schema
from main import bcrypt


def get_user(column: str, value: Union[str, int], db: Session):
    query = (
        db.query(models.User)
        .filter(models.User.__getattribute__(models.User, column) == value)
        .first()
    )
    return query


def get_role(search: schema.Query, db: Session) -> Union[schema.RoleQuery, list, None]:
    if search.column and search.value:
        query = (
            db.query(models.Role.id, models.Role.role_name)
            .filter(models.Role.__getattribute__(models.Role, search.column) == search.value)
            .first()
        )
        if query:
            role = schema.RoleQuery.parse_obj(query)
            return role
        return None
    else:
        data = []
        query = (
            db.query(models.Role)
            .all()
        )
        if query:
            for table in query:
                role = schema.RoleQuery.parse_obj(table.__dict__)
                data.append(role)
            return data
        return None


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
    if search.value and search.column:
        query = (
            db.query(
                models.Form.id,
                models.Form.quote_direct,
                models.Form.sales_force_id,
                models.Form.purchase_order,
                models.Form.date,
                models.Form.status,
                models.Form.sale_note
            ).filter(models.Form.__getattribute__(models.Form, search.column) == search.value)
            .all()
        )
    else:
        query = (
            db.query(
                models.Form.id,
                models.Form.quote_direct,
                models.Form.sales_force_id,
                models.Form.purchase_order,
                models.Form.date,
                models.Form.status,
                models.Form.sale_note
            )
            .all()
        )
    return query


def display_full_form(search: schema.Query, db: Session):
    optional_tables = [models.Cisco, models.Vendor, models.Software]
    result = {}
    if search.column and search.value:
        query = (db.query(
            models.Form, models.Customer)
            .select_from(models.Form).filter(models.Form.__getattribute__(models.Form, search.column) == search.value)
            .join(models.Customer)
            .all()
        )
        if query:
            for item in query:
                for table in item:
                    result[table.__tablename__] = table

    for table in optional_tables:
        query = db.query(table).filter(
            table.form_id == search.value).all()
        if query:
            result[table.__tablename__] = query

    data = schema.FullForm.parse_obj(result)
    return data


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
            .filter(
                models.Cisco.__getattribute__(models.Cisco, search.column)
                == search.value
            )
            .first()
        )
        if query:
            vendor = schema.Cisco.parse_obj(query.__dict__)
            return vendor
    else:
        query = (
            db.query(models.Vendor)
            .filter(
                models.Vendor.__getattribute__(models.Vendor, search.column)
                == search.value
            )
            .first()
        )
        if query:
            vendor = schema.Vendor.parse_obj(query.__dict__)
            return vendor
    return query


def get_user_role(roleId: int, db: Session):
    query = (
        db.query(models.User.id, models.User.name, models.Role.role_name)
        .select_from(models.User)
        .join(models.Role)
        .filter(models.Role.id == roleId)
        .all()
    )
    users = [schema.UserQuery.parse_obj(x).dict() for x in query]
    return users


def update_form(data: schema.UpdateForm, db: Session):
    query = (
        db.query(models.Form)
        .filter(models.Form.id == data.id)
        .update({data.column: data.value}, synchronize_session=False)
    )
    db.commit()
    return query


def create_user(users: list[schema.CreateUser], db: Session):
    message = schema.Message()
    for user in users:
        query = get_user("name", user.name, db)
        if query:
            message.add(MessageType.alreadyExist, query)
        elif get_role(schema.Query(column="id", value=user.role_id), db):
            try:
                hash_password = bcrypt.generate_password_hash(
                    user.password).decode("utf-8")
                new_user = models.User(
                    name=user.name,
                    email=user.email,
                    password=hash_password,
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
        query = get_role(schema.Query(
            column="role_name", value=role.role_name), db)
        if query:
            message.add(MessageType.alreadyExist, query)
        else:
            try:
                print("this")
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
                purchase_order=form.purchase_order,
                quote_direct=form.quote_direct,
                client_manager_name=form.client_manager_name,
                pre_sales_name=form.pre_sales_name,
                customer_id=form.customer_id,
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
                vendor_deal_id=vendor.vendor_deal_id,
                vendor_name=vendor.vendor_name,
                account_manager_name=vendor.account_manager_name,
                account_manager_phone=vendor.account_manager_phone,
                account_manager_email=vendor.account_manager_email,
                form_id=vendor.form_id,
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
                vendor_deal_id=vendor.vendor_deal_id,
                account_manager_name=vendor.account_manager_name,
                account_manager_phone=vendor.account_manager_phone,
                account_manager_email=vendor.account_manager_email,
                smart_account=vendor.smart_account,
                virtual_account=vendor.virtual_account,
                form_id=vendor.form_id,
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
            type_of_purchase=software.type_of_purchase,
            form_id=software.form_id,
        )
        db.add(new_software)
        db.commit()
        db.refresh(new_software)
        message.add(MessageType.softwareCreated, new_software)
    except Exception as error:
        message.add(MessageType.generalError, error)
    return message


def delete_form(id: schema.Id, db: Session):
    optional_tables = [models.Cisco, models.Vendor, models.Software]
    message = schema.Message()

    for table in optional_tables:
        queryList = (
            db.query(table)
            .filter(table.form_id == id.id)
            .all()
        )
        for query in queryList:
            db.delete(query)

    form = (
        db.query(models.Form)
        .filter(models.Form.id == id.id)
        .first()
    )
    if form:
        db.delete(form)
        message.add(MessageType.deletedObject, form)

    db.commit()

    return message


def encap_form(form: Union[ChecklistFormSales, Vendor, Cisco, Software], data: schema.FullForm):
    if isinstance(form, ChecklistFormSales):
        if data.form and data.customer:
            form.sale_note.data = data.form.sale_note
            form.sales_force_id.data = data.form.sales_force_id
            form.purchase_order.data = data.form.purchase_order
            form.quote_direct.data = data.form.quote_direct
            form.client_manager_name.data = data.form.client_manager_name
            form.pre_sales_name.data = data.form.pre_sales_name
            form.customer_name.data = data.customer.customer_name
            form.customer_rut.data = data.customer.customer_rut
            form.customer_address.data = data.customer.customer_address
            form.customer_contact_name.data = data.customer.customer_contact_name
            form.customer_contact_phone.data = data.customer.customer_contact_phone
            form.customer_contact_email.data = data.customer.customer_contact_email
            form.dispatch_address.data = data.customer.dispatch_address
            form.dispatch_receiver_name.data = data.customer.dispatch_receiver_name
            form.dispatch_receiver_phone.data = data.customer.dispatch_receiver_phone
            form.dispatch_receiver_email.data = data.customer.dispatch_receiver_email
            form.comments.data = data.form.comments
            return form
        else:
            return None
    elif isinstance(form, Vendor):
        if data.vendor:
            vendor_list: list[Vendor] = []
            for vendor in data.vendor:
                form_vendor = Vendor()
                form_vendor.vendor_deal_id.data = vendor.vendor_deal_id
                form_vendor.vendor_name.data = vendor.vendor_name
                form_vendor.account_manager_name.data = vendor.account_manager_name
                form_vendor.account_manager_phone.data = vendor.account_manager_phone
                form_vendor.account_manager_email.data = vendor.account_manager_email
                vendor_list.append(form_vendor)
            return vendor_list
        else:
            return data.vendor
    elif isinstance(form, Cisco):
        if data.cisco:
            cisco_list: list[Cisco] = []
            for cisco in data.cisco:
                form_cisco = Cisco()
                form_cisco.vendor_deal_id.data = cisco.vendor_deal_id
                form_cisco.account_manager_name.data = cisco.account_manager_name
                form_cisco.account_manager_phone.data = cisco.account_manager_phone
                form_cisco.account_manager_email.data = cisco.account_manager_email
                form_cisco.smart_account.data = cisco.smart_account
                form_cisco.virtual_account.data = cisco.virtual_account
                cisco_list.append(form_cisco)
            return cisco_list
        else:
            return data.cisco
    elif isinstance(form, Software):
        if data.software:
            software_list: list[Software] = []
            for software in data.software:
                form_software = Software()
                form_software.software_type.data = software.software_type
                form_software.duration_time.data = software.duration_time
                form_software.customer_contact.data = software.customer_contact
                form_software.subscription_id.data = software.subscription_id
                form_software.start_date.data = software.start_date
                form_software.type_of_purchase.data = software.type_of_purchase
                software_list.append(form_software)
            return software_list
        else:
            return data.software
