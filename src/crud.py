from sqlalchemy.orm import Session
from src.schema import MessageType
from src import models, schema, bcrypt
from typing import Any, Union
from pprint import pprint

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


def display_partial_form(search: schema.Query, db: Session) -> Union[list[schema.PartialForm], list]:
    result = []
    if search.value and search.column:
        query = (
            db.query(
                models.Form.id,
                models.Form.quote_direct,
                models.Form.sales_force_id,
                models.Form.purchase_order,
                models.Form.date,
                models.Form.status,
                models.Form.sale_note,
                models.Form.client_manager_name,
                models.Form.pre_sales_name,
                models.Customer.customer_name
            ).select_from(models.Form)
            .filter(models.Form.__getattribute__(models.Form, search.column) == search.value)
            .join(models.Customer)
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
                models.Form.sale_note,
                models.Form.client_manager_name,
                models.Form.pre_sales_name,
                models.Customer.customer_name
            ).select_from(models.Form).join(models.Customer).all()
        )
    if query:
        for form in query:
            result.append(schema.PartialForm.parse_obj(form))
        return result
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


def get_customer(search: schema.Query, db: Session) -> Union[list[schema.Customer], None]:
    data = []
    if search.column and search.value:
        query = (
            db.query(models.Customer)
            .filter(models.Customer.__getattribute__(models.Customer, search.column) == search.value)
            .first()
        )
        if query:
            customer = schema.Customer.parse_obj(query.__dict__)
            data.append(query)
            return data
        return None
    else:
        query = (
            db.query(models.Customer)
            .all()
        )
        if query:
            for table in query:
                customer = schema.Customer.parse_obj(table.__dict__)
                data.append(customer)
            return data
        return None


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
    users = [schema.UserQuery.parse_obj(x) for x in query]
    return users


def update_form(data: schema.UpdateForm, db: Session):
    if data.form_type == schema.FormTypes.checklist:
        query = (
            db.query(models.Form)
            .filter(models.Form.id == data.id)
            .update({data.column: data.value}, synchronize_session=False)
        )
        db.commit()
        return query
    elif data.form_type == schema.FormTypes.cisco:
        query = (
            db.query(models.Cisco)
            .filter(models.Cisco.id == data.id)
            .update({data.column: data.value}, synchronize_session=False)
        )
        db.commit()
        return query
    elif data.form_type == schema.FormTypes.vendor:
        query = (
            db.query(models.Vendor)
            .filter(models.Vendor.id == data.id)
            .update({data.column: data.value}, synchronize_session=False)
        )
        db.commit()
        return query
    elif data.form_type == schema.FormTypes.software:
        query = (
            db.query(models.Software)
            .filter(models.Software.id == data.id)
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
                customer_address = form.customer_address,
                customer_contact_name = form.customer_contact_name,
                customer_contact_phone = form.customer_contact_phone,
                customer_contact_email = form.customer_contact_email,
                dispatch_address=form.dispatch_address,
                dispatch_receiver_name=form.dispatch_receiver_name,
                dispatch_receiver_phone=form.dispatch_receiver_phone,
                dispatch_receiver_email=form.dispatch_receiver_email,
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
    if get_customer(schema.Query(column="customer_rut", value=customer.customer_rut), db):
        message.add(MessageType.alreadyExist, customer.customer_rut)
    else:
        try:
            new_customer = models.Customer(
                customer_name=customer.customer_name,
                customer_rut=customer.customer_rut
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
                vendor_account_manager_name=vendor.vendor_account_manager_name,
                vendor_account_manager_phone=vendor.vendor_account_manager_phone,
                vendor_account_manager_email=vendor.vendor_account_manager_email,
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
                cisco_deal_id=vendor.cisco_deal_id,
                cisco_account_manager_name=vendor.cisco_account_manager_name,
                cisco_account_manager_phone=vendor.cisco_account_manager_phone,
                cisco_account_manager_email=vendor.cisco_account_manager_email,
                cisco_smart_account=vendor.cisco_smart_account,
                cisco_virtual_account=vendor.cisco_virtual_account,
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

def apply_form_changes(form_data: schema.FullForm, input_data: dict[str, str], db:Session) -> Any:
    for label, form_value in dict(form_data.form).items():
        input_value = input_data.get(label)
        if input_value:
            if str(form_value).lower() != str(input_value).lower():
                new_data = schema.UpdateForm(form_type=schema.FormTypes.checklist, column=label, value=input_value, id=form_data.form.id)
                update_form(new_data, db)

    forms = [(schema.FormTypes.cisco, form_data.cisco), 
    (schema.FormTypes.vendor, form_data.vendor),
    (schema.FormTypes.software, form_data.software)]
    for form_type, form in forms:
        if form:
            i = 0
            while i < len(form):
                for label, form_value in dict(form[i]).items():
                    input_value = input_data.get(label+str(i))
                    if input_value:
                        # print(f"{label} -> {form_value} and {input_value}")
                        # print(form[i].id)
                        if str(form_value).lower() != str(input_value).lower():
                            new_data = schema.UpdateForm(form_type=form_type, column=label, value=input_value, id=form[i].id)
                            pprint(new_data)
                            update_form(new_data, db)
                i += 1