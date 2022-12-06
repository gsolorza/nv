from db import Base
from sqlalchemy import Column, String, ForeignKey, Integer, Boolean, Date
from sqlalchemy.orm import relationship


class User(Base):

    __tablename__ = "user"

    id = Column(Integer, index=True, primary_key=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    role_id = Column(Integer, ForeignKey("role.id"),
                     nullable=False)
    role = relationship("Role", back_populates="user")


class Role(Base):

    __tablename__ = "role"
    id = Column(Integer, index=True, primary_key=True, nullable=False)
    role_name = Column(String, unique=True, nullable=False)
    user = relationship("User", back_populates="role")


class Form(Base):

    __tablename__ = "form"
    id = Column(Integer, index=True, primary_key=True,
                unique=True, nullable=False)
    sales_force_id = Column(String, index=True, nullable=False)
    purchase_order = Column(String, index=True, nullable=False)
    quote_direct = Column(String, unique=True)
    client_manager_name = Column(String, nullable=False)
    pre_sales_name = Column(String, nullable=False)
    sale_note = Column(String, nullable=True, default=None)
    customer_id = Column(Integer, ForeignKey("customer.id"), nullable=False)
    comments = Column(String, nullable=False)
    customer = relationship("Customer", back_populates="form")
    vendor = relationship("Vendor", back_populates="form",
                          cascade="all, delete", passive_deletes=True)
    cisco = relationship("Cisco", back_populates="form",
                         cascade="all, delete", passive_deletes=True)
    software = relationship(
        "Software", back_populates="form", cascade="all, delete", passive_deletes=True)
    status = Column(String, nullable=False)
    date = Column(Date, nullable=False)


class Cisco(Base):

    __tablename__ = "cisco"
    id = Column(
        Integer, index=True, primary_key=True, unique=True, nullable=False
    )
    vendor_deal_id = Column(String, nullable=False)
    vendor_name = Column(String, nullable=False, default="Cisco")
    account_manager_name = Column(String, nullable=False)
    account_manager_phone = Column(String, nullable=False)
    account_manager_email = Column(String, nullable=False)
    smart_account = Column(String, default="")
    virtual_account = Column(String, default="")
    form_id = Column(Integer, ForeignKey("form.id", ondelete="CASCADE"))
    form = relationship("Form", back_populates="cisco")


class Vendor(Base):

    __tablename__ = "vendor"
    id = Column(
        Integer, index=True, primary_key=True, unique=True, nullable=False
    )
    vendor_deal_id = Column(String, nullable=False)
    vendor_name = Column(String, nullable=False)
    account_manager_name = Column(String, nullable=False)
    account_manager_phone = Column(String, nullable=False)
    account_manager_email = Column(String, nullable=False)
    form_id = Column(Integer, ForeignKey("form.id", ondelete="CASCADE"))
    form = relationship("Form", back_populates="vendor")


class Customer(Base):

    __tablename__ = "customer"
    id = Column(Integer, index=True, primary_key=True,
                unique=True, nullable=False)
    customer_name = Column(String, unique=True, nullable=False)
    customer_rut = Column(String, unique=True, nullable=False)
    customer_address = Column(String, unique=True, nullable=False)
    customer_contact_name = Column(String, nullable=False)
    customer_contact_phone = Column(String, nullable=False)
    customer_contact_email = Column(String, nullable=False)
    dispatch_address = Column(String, unique=True, nullable=False)
    dispatch_receiver_name = Column(String, nullable=False)
    dispatch_receiver_phone = Column(String, nullable=False)
    dispatch_receiver_email = Column(String, nullable=False)
    form = relationship("Form", back_populates="customer")


class Software(Base):
    __tablename__ = "software"
    id = Column(Integer, index=True, primary_key=True,
                unique=True, nullable=False)
    software_type = Column(String, nullable=False)
    duration_time = Column(String, nullable=False)
    customer_contact = Column(String, nullable=False)
    subscription_id = Column(String, nullable=True)
    start_date = Column(String, nullable=False)
    type_of_purchase = Column(String, nullable=True)
    form_id = Column(Integer, ForeignKey("form.id", ondelete="CASCADE"))
    form = relationship("Form", back_populates="software")
