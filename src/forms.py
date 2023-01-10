from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField, TextAreaField, SelectField, IntegerField, ValidationError, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp
from src import schema
from typing import Union, Any
from src.crud import get_form
from src.db import db


class LoginForm(FlaskForm):

    email = EmailField(
        "Email", validators=[DataRequired(), Email()]
    )
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):

    email = EmailField('Email',
                       validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])

    rol = StringField('Rol',
                      validators=[DataRequired()])
    submit = SubmitField('Sign Up')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

   

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')




class InitialFormSales(FlaskForm):
    sales_force_id = StringField("Sales Force ID",
                                 validators=[DataRequired(), Length(min=5, max=30), Regexp(r"^(?=.*[0-9])(?=.*[a-zA-Z])[0-9a-zA-Z]+$", message="Should include letters and numbers")])
    purchase_order = StringField("Purchase Order", render_kw={"placeholder": "NoPO"})
    quote_direct = StringField("Quote Direct", validators=[
                               DataRequired(), Length(min=5, max=30), Regexp(r"^[0-9.]+$", message="Only numbers with no spaces")])
    submit = SubmitField("Create Form")
    
    def validate_quote_direct(self, quote_direct):
        if(get_form("quote_direct", quote_direct.data, db())):
            raise ValidationError("The quote from direct already exist in the Database")

class CustomerForm(FlaskForm):
    customer_name = StringField("Customer Name", validators=[
                                DataRequired(), Length(min=5, max=30)])
    customer_rut = StringField("Customer RUT", validators=[
                               DataRequired(), Length(min=5, max=30)])
    submit=SubmitField("Create Customer")

class ChecklistFormSales(FlaskForm):
    sales_force_id = StringField("Sales Force ID", validators=[
                                 DataRequired(), Length(min=5, max=30), Regexp(r"^(?=.*[0-9])(?=.*[a-zA-Z])[0-9a-zA-Z]+$", message="Sales Force ID should include letters and numbers")])
    purchase_order = StringField("Purchase Order", render_kw={"placeholder": "NoPO"})
    quote_direct = StringField("Quote Direct", validators=[
                               DataRequired(), Length(min=5, max=30), Regexp(r"^[0-9.]+$", message="Only numbers with no spaces")])
    pre_sales_name = SelectField("Pre Sales Engineer", choices=[])
    customer_address = TextAreaField("Customer Address", validators=[
        DataRequired(), Length(min=5, max=300)])
    client_manager_name = StringField("Customer Contact Name", validators=[
                                        DataRequired(), Length(min=4, max=30), Regexp(r"^[A-Za-z\s]+$", message="The name should only include letters")])
    customer_contact_name = StringField("Customer Contact Name", validators=[
                                        DataRequired(), Length(min=4, max=30), Regexp(r"^[A-Za-z\s]+$", message="The name should only include letters")])
    customer_contact_phone = StringField("Customer Contact Phone", validators=[
                                         DataRequired(), Length(min=5, max=15), Regexp(r"^[0-9]+$", message="The phone should only include numbers")])
    customer_contact_email = EmailField("Customer Contact Email", validators=[
                                        DataRequired(), Length(min=5, max=30), Email()])
    dispatch_address = TextAreaField("Dispatch Address", validators=[DataRequired(), Length(min=5, max=300)])                                    
    dispatch_receiver_name = StringField("Dispatch Receiver Name", validators=[
                                         DataRequired(), Length(min=4, max=30), Regexp(r"^[A-Za-z\s]+$", message="The name should only include letters")])
    dispatch_receiver_phone = StringField("Dispatch Receiver Phone", validators=[
                                          DataRequired(), Length(min=5, max=15), Regexp(r"^[0-9]+$", message="The phone should only include numbers")])
    dispatch_receiver_email = EmailField("Dispatch Receiver Email", validators=[
                                         DataRequired(), Length(min=5, max=30), Email()])
    
    sale_note = StringField("Sale Note")
    date = DateField("Date")
    comments = TextAreaField("Comments", validators=[DataRequired(), Length(
        min=5, max=2000)], render_kw={"placeholder": "Enter your comments"})
    
    status = SelectField("Assign", choices=[])
    customer_id = IntegerField("Customer ID", validators=[DataRequired()])
    db_validation = True
    submit = SubmitField("Submit")

    def set_choices(self, choices, field_name, default_value=""):
        if field_name == "pre_sales_name":
            self.pre_sales_name.choices = choices
            self.pre_sales_name.default = default_value 
        elif field_name == "status":
            self.status.choices = choices
            self.status.default = default_value

    def validate_quote_direct(self, quote_direct):
        if(get_form("quote_direct", quote_direct.data, db()) and self.db_validation):
            raise ValidationError("The quote from direct already exist in the Database")

class Vendor(FlaskForm):
    vendor_deal_id = StringField(
        "Deal ID", validators=[DataRequired(), Length(min=5, max=30)])
    vendor_name = StringField("Vendor Name", validators=[
                              DataRequired(), Length(min=1, max=20), Regexp(r"^[0-9a-zA-Z]+$", message="The Vendor name should only include letters and numbers")])
    vendor_account_manager_name = StringField(" Manager Name", validators=[
                                       DataRequired(), Length(min=3, max=20), Regexp(r"^[A-Za-z\s]+$", message="The name should only include letters")])
    vendor_account_manager_phone = StringField(" Manager Phone", validators=[
                                        DataRequired(), Length(min=5, max=15), Regexp(r"^[0-9]+$", message="The phone should only include numbers")],render_kw={"placeholder": "5690000000"})
    vendor_account_manager_email = EmailField(
        "Manager Email", validators=[DataRequired(), Email()],render_kw={"placeholder": "email@vendor.com"})
    index = IntegerField("Index", default=0)

class Cisco(FlaskForm):
    cisco_deal_id = StringField(
        "Deal ID", validators=[DataRequired(), Length(min=5, max=30)])
    cisco_account_manager_name = StringField(" Manager Name", validators=[
                                       DataRequired(), Length(min=3, max=20), Regexp(r"^[A-Za-z\s]+$", message="The name should only include letters")])
    cisco_account_manager_phone = StringField(" Manager Phone", validators=[
                                        DataRequired(), Length(min=5, max=15), Regexp(r"^[0-9]+$", message="The phone should only include numbers")],render_kw={"placeholder": "5690000000"})
    cisco_account_manager_email = EmailField(
        "Manager Email", validators=[DataRequired(), Email()],render_kw={"placeholder": "email@cisco.com"})
    cisco_smart_account = StringField("Smart Account", validators=[
                                DataRequired(), Length(min=5, max=30)])
    cisco_virtual_account = StringField("Virtual Account", validators=[
                                  DataRequired(), Length(min=5, max=30)])
    index = IntegerField("Index", default=0)


class Software(FlaskForm):
    software_type = SelectField(
        "Subs/Software Type",choices=["SaaS","Embedded in Hardware","Subscription licence"], validators=[DataRequired()])
    duration_time = SelectField(
        "Duration Time in Months",choices=[("12"),("24"),("36"),("48"),("60")], validators=[DataRequired()])
    customer_contact = TextAreaField(
        "End Costumer contact", validators=[DataRequired()],render_kw={"placeholder": "Name/ Phone/ Email"})
    subscription_id = StringField("Subscription ID")

        
    start_date = StringField("Start Date", validators=[DataRequired()])
    type_of_purchase = SelectField(
        "Type of Purchase",choices=[("New"),("Non-automatic Renewal "),("Automatic Renewal")] ,validators=[DataRequired()])
    index = IntegerField("Index", default=0)



# Functions to work with Form Data

def encap_form(form: Union[ChecklistFormSales, Vendor, Cisco, Software], data: schema.FullForm):
    if isinstance(form, ChecklistFormSales):
        if data.form and data.customer:
            form.sales_force_id.data = data.form.sales_force_id
            form.purchase_order.data = data.form.purchase_order
            form.quote_direct.data = data.form.quote_direct
            form.client_manager_name.data = data.form.client_manager_name
            form.pre_sales_name.data = data.form.pre_sales_name
            form.customer_id.data = data.form.customer_id
            form.customer_address.data = data.form.customer_address
            form.customer_contact_name.data = data.form.customer_contact_name
            form.customer_contact_phone.data = data.form.customer_contact_phone
            form.customer_contact_email.data = data.form.customer_contact_email
            form.dispatch_address.data = data.form.dispatch_address
            form.dispatch_receiver_name.data = data.form.dispatch_receiver_name
            form.dispatch_receiver_phone.data = data.form.dispatch_receiver_phone
            form.dispatch_receiver_email.data = data.form.dispatch_receiver_email
            form.date.data = data.form.date
            form.status.data = data.form.status
            form.sale_note.data = data.form.sale_note
            form.comments.data = data.form.comments
            return form
        else:
            return None
    elif isinstance(form, Vendor):
        if data.vendor:
            vendor_list: list[Vendor] = []
            i = 0
            for vendor in data.vendor:
                form_vendor = Vendor()
                form_vendor.vendor_deal_id.data = vendor.vendor_deal_id
                form_vendor.vendor_name.data = vendor.vendor_name
                form_vendor.vendor_account_manager_name.data = vendor.vendor_account_manager_name
                form_vendor.vendor_account_manager_phone.data = vendor.vendor_account_manager_phone
                form_vendor.vendor_account_manager_email.data = vendor.vendor_account_manager_email
                form_vendor.vendor_deal_id.name = form_vendor.vendor_deal_id.name+str(i)
                form_vendor.vendor_name.name = form_vendor.vendor_name.name+str(i)
                form_vendor.vendor_account_manager_name.name = form_vendor.vendor_account_manager_name.name+str(i)
                form_vendor.vendor_account_manager_phone.name = form_vendor.vendor_account_manager_phone.name+str(i)
                form_vendor.vendor_account_manager_email.name = form_vendor.vendor_account_manager_email.name+str(i)
                form_vendor.index.data = i
                vendor_list.append(form_vendor)
                i =+ 1
            return vendor_list
        else:
            return data.vendor
    elif isinstance(form, Cisco):
        if data.cisco:
            cisco_list: list[Cisco] = []
            i = 0
            for cisco in data.cisco:
                form_cisco = Cisco()
                form_cisco.cisco_deal_id.data = cisco.cisco_deal_id
                form_cisco.cisco_account_manager_name.data = cisco.cisco_account_manager_name
                form_cisco.cisco_account_manager_phone.data = cisco.cisco_account_manager_phone
                form_cisco.cisco_account_manager_email.data = cisco.cisco_account_manager_email
                form_cisco.cisco_smart_account.data = cisco.cisco_smart_account
                form_cisco.cisco_virtual_account.data = cisco.cisco_virtual_account
                form_cisco.cisco_deal_id.name = form_cisco.cisco_deal_id.name+str(i)
                form_cisco.cisco_account_manager_name.name = form_cisco.cisco_account_manager_name.name+str(i)
                form_cisco.cisco_account_manager_phone.name = form_cisco.cisco_account_manager_phone.name+str(i)
                form_cisco.cisco_account_manager_email.name = form_cisco.cisco_account_manager_email.name+str(i)
                form_cisco.cisco_smart_account.name = form_cisco.cisco_smart_account.name+str(i)
                form_cisco.cisco_virtual_account.name = form_cisco.cisco_virtual_account.name+str(i)
                form_cisco.index.data = i
                cisco_list.append(form_cisco)
                i =+ 1
            return cisco_list
        else:
            return data.cisco
    elif isinstance(form, Software):
        if data.software:
            software_list: list[Software] = []
            i = 0
            for software in data.software:
                form_software = Software()
                form_software.software_type.data = software.software_type
                form_software.duration_time.data = software.duration_time
                form_software.customer_contact.data = software.customer_contact
                form_software.subscription_id.data = software.subscription_id
                form_software.start_date.data = software.start_date
                form_software.type_of_purchase.data = software.type_of_purchase
                form_software.software_type.name = form_software.software_type.name+str(i)
                form_software.duration_time.name = form_software.duration_time.name+str(i)
                form_software.customer_contact.name = form_software.customer_contact.name+str(i)
                form_software.subscription_id.name = form_software.subscription_id.name+str(i)
                form_software.start_date.name = form_software.start_date.name+str(i)
                form_software.type_of_purchase.name = form_software.type_of_purchase.name+str(i)
                form_software.index.data = i
                software_list.append(form_software)
                i =+ 1
            return software_list
        else:
            return data.software


def replicateForm(form, form_data: dict[str, str], quantity: int = 1) -> Any:
    if isinstance(form, Cisco):
        forms = [Cisco() for x in range(quantity)]
        i = 0
        for form in forms:
            form.cisco_deal_id.name = form.cisco_deal_id.name+str(i)
            form.cisco_deal_id.data = form_data.get(form.cisco_deal_id.name)
            form.cisco_account_manager_name.name = form.cisco_account_manager_name.name+str(i)
            form.cisco_account_manager_name.data = form_data.get(form.cisco_account_manager_name.name)
            form.cisco_account_manager_email.name = form.cisco_account_manager_email.name+str(i)
            form.cisco_account_manager_email.data = form_data.get(form.cisco_account_manager_email.name)
            form.cisco_account_manager_phone.name = form.cisco_account_manager_phone.name+str(i)
            form.cisco_account_manager_phone.data = form_data.get(form.cisco_account_manager_phone.name)
            form.cisco_smart_account.name = form.cisco_smart_account.name+str(i)
            form.cisco_smart_account.data = form_data.get(form.cisco_smart_account.name)
            form.cisco_virtual_account.name = form.cisco_virtual_account.name+str(i)
            form.cisco_virtual_account.data = form_data.get(form.cisco_virtual_account.name)
            form.index.data = i
            i += 1
        return forms
    elif isinstance(form, Vendor):
        forms = [Vendor() for x in range(quantity)]
        i = 0
        for form in forms:
            form.vendor_deal_id.name = form.vendor_deal_id.name+str(i)
            form.vendor_deal_id.data = form_data.get(form.vendor_deal_id.name)
            form.vendor_name.name = form.vendor_name.name+str(i)
            form.vendor_name.data = form_data.get(form.vendor_name.name)
            form.vendor_account_manager_name.name = form.vendor_account_manager_name.name+str(i)
            form.vendor_account_manager_name.data = form_data.get(form.vendor_account_manager_name.name)
            form.vendor_account_manager_email.name = form.vendor_account_manager_email.name+str(i)
            form.vendor_account_manager_email.data = form_data.get(form.vendor_account_manager_email.name)
            form.vendor_account_manager_phone.name = form.vendor_account_manager_phone.name+str(i)
            form.vendor_account_manager_phone.data = form_data.get(form.vendor_account_manager_phone.name)
            form.index.data = i
            i += 1
        return forms
    elif isinstance(form, Software):
        forms = [Software() for x in range(quantity)]
        i = 0
        for form in forms:
            form.software_type.name = form.software_type.name+str(i)
            form.software_type.data = form_data.get(form.software_type.name)
            form.duration_time.name = form.duration_time.name+str(i)
            form.duration_time.data = form_data.get(form.duration_time.name)
            form.customer_contact.name = form.customer_contact.name+str(i)
            form.customer_contact.data = form_data.get(form.customer_contact.name)
            form.subscription_id.name = form.subscription_id.name+str(i)
            form.subscription_id.data = form_data.get(form.subscription_id.name)
            form.start_date.name = form.start_date.name+str(i)
            form.start_date.data = form_data.get(form.start_date.name)
            form.type_of_purchase.name = form.type_of_purchase.name+str(i)
            form.type_of_purchase.data = form_data.get(form.type_of_purchase.name)
            form.index.data = i
            i += 1
        return forms

def is_data_validated(forms: list[Union[ChecklistFormSales, Cisco, Vendor, Software]]):
    is_valid = True
    for form in forms:
        if form.validate_on_submit():
            continue
        else:
            is_valid = False
    return is_valid


        