from pydantic import BaseModel
from typing import Any, Union
import datetime
from enum import Enum, auto


class MessageType(Enum):
    userNotFound = "Username not found"
    invalidCredentials = "Incorrect username or password"
    successfullLogin = "Access granted"
    userNotActive = "User is not active"
    userCreated = "The following user(s) have been created"
    alreadyExist = "The following object(s) already exist"
    roleCreated = "The following role have been created"
    noActionNeeded = "No Action is needed based on the provided parameters"
    deletedObject = "The following object(s) have been deleted"
    associationCreated = "The following association have been created"
    roleNotFound = "role not found"
    generalError = "Error details"
    formCreated = "Form have been created successfully"
    customerCreated = "Customer have been created successfully"
    vendorCreated = "Vendor have been created successfully"
    softwareCreated = "Software have been created successfully"
    data = "data"

class Status(Enum):
    completed = "Completed"

class FormTypes(Enum):
    checklist = "Checklist"
    cisco = "Cisco"
    vendor = "Vendor"
    software = "Software"

class Query(BaseModel):
    column: Union[str, None] = None
    value: Union[str, int, None] = None
    vendor_cisco: bool = True

    class Config:
        orm_mode = True


class Id(BaseModel):
    id: int


class UserQuery(BaseModel):
    id: int
    name: str
    
    class Config:
        orm_mode = True

class RoleQuery(BaseModel):
    id: int
    role_name: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str
    email: str
    role_id: str


class CreateUser(UserBase):
    password: str


class CreateRole(BaseModel):
    role_name: str


class CreateForm(BaseModel):
    sales_force_id: str
    purchase_order: str = "No PO"
    quote_direct: str
    client_manager_name: str
    pre_sales_name: str
    customer_id: int
    comments: str
    status: str
    sale_note: Union[str, None] = None
    date: datetime.date = datetime.date.today()
    customer_address: str
    customer_contact_name: str
    customer_contact_phone: str
    customer_contact_email: str
    dispatch_address: str
    dispatch_receiver_name: str
    dispatch_receiver_phone: str
    dispatch_receiver_email: str

    class Config:
        orm_mode = True


class Form(CreateForm):
    id: int


class DisplayForm(BaseModel):
    id: int
    quote_direct: str
    sales_force_id: str
    purchase_order: str
    date: datetime.date
    status: str
    sale_note: Union[str, None]


class UpdateForm(BaseModel):
    id: int
    value: str
    column: str
    form_type: FormTypes


class CreateCustomer(BaseModel):
    customer_name: str
    customer_rut: str

    class Config:
        orm_mode = True


class Customer(CreateCustomer):
    id: int

    class Config:
        orm_mode = True


class CreateVendor(BaseModel):
    form_id: int
    vendor_deal_id: str
    vendor_name: str
    vendor_account_manager_name: str
    vendor_account_manager_phone: str
    vendor_account_manager_email: str

    class Config:
        orm_mode = True


class Vendor(CreateVendor):
    id: int


class CreateCisco(BaseModel):
    form_id: int
    vendor_name: str = "Cisco"
    cisco_deal_id: str
    cisco_account_manager_name: str
    cisco_account_manager_phone: str
    cisco_account_manager_email: str
    cisco_smart_account: str = ""
    cisco_virtual_account: str = ""

    class Config:
        orm_mode = True

class Cisco(CreateCisco):
    id: int

class CreateSoftware(BaseModel):
    form_id: int
    software_type: str
    duration_time: str
    customer_contact: str
    subscription_id: Union[str, None]
    start_date: str
    type_of_purchase: str

    class Config:
        orm_mode = True


class Software(CreateSoftware):
    id: int


class FullForm(BaseModel):
    form: Form
    customer: Customer
    vendor: Union[list[Vendor], None] = None
    cisco: Union[list[Cisco], None] = None
    software: Union[list[Software], None] = None

class PartialForm(BaseModel):
    id: str
    quote_direct: str
    sales_force_id: str
    purchase_order: Union[str, None]
    date: datetime.date
    status: str
    sale_note: Union[str, None]
    client_manager_name: str
    pre_sales_name: str
    customer_name: str

    class Config:
        orm_mode = True

class Message(BaseModel):
    message: dict[MessageType, list] = {}

    def add(self, messageType: MessageType, object: Any):
        if not self.message.get(messageType):
            self.message[messageType] = []

        self.message[messageType].append(object)
    
    class Config:
        orm_mode = True
