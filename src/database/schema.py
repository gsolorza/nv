from pydantic import BaseModel
from typing import Any, Union
import datetime
from enum import Enum


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


class Status(Enum):
    preSalesValidation = "Pre Sales Validation"
    insidePreSalesValidation = "Inside Pre Sales Validation"
    plValidation = "P&L Valdiation"
    approved = "Approved"


class Query(BaseModel):
    column: str
    value: Union[str, int]
    vendor_cisco: bool = True


class Id(BaseModel):
    id: int


class UserQuery(BaseModel):
    id: int
    username: str


class RoleQuery(BaseModel):
    id: int
    role_name: str


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
    vendor_deal_id: str = "No Deal ID"
    purchase_order: str = "No PO"
    quote_direct: str
    client_manager_name: str
    pre_sales_name: str
    customer_id: int
    vendor_id: Union[int, None] = None
    cisco_id: Union[int, None] = None
    software_id: Union[int, None] = None
    comments: str
    status: str = Status.preSalesValidation.value
    sale_note: Union[str, None] = None
    date: datetime.date = datetime.date.today()


class Form(CreateForm):
    id: int


class DisplayForm(BaseModel):
    id: int
    vendor_deal_id: str
    quote_direct: str
    sales_force_id: str
    purchase_order: str
    date: datetime.date
    status: str


class SaleNote(BaseModel):
    id: int
    sale_note: str


class CreateCustomer(BaseModel):
    customer_name: str
    customer_rut: str
    customer_address: str
    customer_contact_name: str
    customer_contact_phone: str
    customer_contact_email: str
    dispatch_address: str
    dispatch_receiver_name: str
    dispatch_receiver_phone: str
    dispatch_receiver_email: str


class Customer(CreateCustomer):
    id: int


class CreateVendor(BaseModel):
    vendor_name: str
    account_manager_name: str
    account_manager_phone: str
    account_manager_email: str


class Vendor(CreateVendor):
    id: int


class CreateCisco(BaseModel):
    account_manager_name: str
    account_manager_phone: str
    account_manager_email: str
    smart_account: str = ""
    virtual_account: str = ""


class Cisco(CreateVendor):
    id: int


class CreateSoftware(BaseModel):
    software_type: str
    duration_time: str
    customer_contact: str
    subscription_id: str
    start_date: str
    type_of_purchase: str


class Software(CreateSoftware):
    id: int


class Message(BaseModel):
    message: dict[MessageType, list] = {}

    def add(self, messageType: MessageType, object: Any):
        if not self.message.get(messageType):
            self.message[messageType] = []

        self.message[messageType].append(object)

    class Config:
        orm_mode = True
