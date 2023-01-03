from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, BooleanField, EmailField, TextAreaField, SelectField, IntegerField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp
import re

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


class InitialFormSales(FlaskForm):
    sales_force_id = StringField("Sales Force ID",
                                 validators=[DataRequired(), Length(min=5, max=30), Regexp(r"^(?=.*[0-9])(?=.*[a-zA-Z])[0-9a-zA-Z]+$", message="Should include letters and numbers")])
    purchase_order = StringField("Purchase Order", render_kw={"placeholder": "NoPO"})
    quote_direct = StringField("Quote Direct", validators=[
                               DataRequired(), Length(min=5, max=30), Regexp(r"^[0-9.]+$", message="Only numbers with no spaces")])
    include_software = BooleanField("Software", default='checked')
    include_vendor = BooleanField("Other Vendor", default='checked')
    include_cisco = BooleanField(" Cisco Vendor", default='checked')
    submit = SubmitField("Create Form")

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
    customer_contact_name = StringField("Customer Contact Name", validators=[
                                        DataRequired(), Length(min=4, max=30), Regexp(r"^[A-Za-z\s]+$", message="The name should only include letters")])
    customer_contact_phone = StringField("Customer Contact Phone", validators=[
                                         DataRequired(), Length(min=5, max=30), Regexp(r"^[0-9]+$", message="The phone should only include numbers")])
    customer_contact_email = EmailField("Customer Contact Email", validators=[
                                        DataRequired(), Length(min=5, max=30), Email()])
    dispatch_address = TextAreaField("Dispatch Address", validators=[DataRequired(), Length(min=5, max=300)])                                    
    dispatch_receiver_name = StringField("Dispatch Receiver Name", validators=[
                                         DataRequired(), Length(min=4, max=30), Regexp(r"^[A-Za-z\s]+$", message="The name should only include letters")])
    dispatch_receiver_phone = StringField("Dispatch Receiver Phone", validators=[
                                          DataRequired(), Length(min=6, max=10), Regexp(r"^[0-9]+$", message="The phone should only include numbers")])
    dispatch_receiver_email = EmailField("Dispatch Receiver Email", validators=[
                                         DataRequired(), Length(min=5, max=30), Email()])

    include_software = BooleanField("Software", default='checked')
    include_vendor = BooleanField("Other Vendor", default='checked')
    include_cisco = BooleanField("Cisco Vendor", default='checked')
    comments = TextAreaField("Comments", validators=[DataRequired(), Length(
        min=5, max=2000)], render_kw={"placeholder": "Enter your comments"})
    
    customer_id = IntegerField("Customer ID", validators=[DataRequired()])
    submit = SubmitField("Submit")

    def set_choices(self, choices):
        self.pre_sales_name.choices = choices

class Vendor(FlaskForm):
    vendor_deal_id = StringField(
        "Deal ID", validators=[DataRequired(), Length(min=5, max=30)])
    vendor_name = StringField("Vendor Name", validators=[
                              DataRequired(), Length(min=5, max=10)])
    vendor_account_manager_name = StringField("Account Manager Name", validators=[
                                       DataRequired(), Length(min=5, max=10)])
    vendor_account_manager_phone = StringField("Account Manager Phone", validators=[
                                        DataRequired(), Length(min=5, max=15)])
    vendor_account_manager_email = EmailField(
        "Account Manager Email", validators=[DataRequired(), Email()])


class Cisco(FlaskForm):
    cisco_deal_id = StringField(
        "Deal ID", validators=[DataRequired(), Length(min=5, max=30)])
    cisco_account_manager_name = StringField("Account Manager Name", validators=[
                                       DataRequired(), Length(min=5, max=10), Regexp(f"[aA-zZ]+", message="The name must contain only letters")])
    cisco_account_manager_phone = StringField("Account Manager Phone", validators=[
                                        DataRequired(), Length(min=5, max=15)])
    cisco_account_manager_email = EmailField(
        "Account Manager Email", validators=[DataRequired(), Email()])
    cisco_smart_account = StringField("Smart Account", validators=[
                                DataRequired(), Length(min=5, max=30)])
    cisco_virtual_account = StringField("Virtual Account", validators=[
                                  DataRequired(), Length(min=5, max=30)])


class Software(FlaskForm):
    software_type = SelectField(
        "Subs/Software Type",choices=["SaaS","Embedded in Hardware","Subscription licence"], validators=[DataRequired()])
    duration_time = SelectField(
        "Duration Time in Months",choices=[("12"),("24"),("36"),("48"),("60")], validators=[DataRequired()])
    customer_contact = TextAreaField(
        "End Costumer contact", validators=[DataRequired()],render_kw={"placeholder": "Name/ Phone/ Email"})
    subscription_id = StringField("Subscription ID")

        
    start_date = StringField("Start Day", validators=[DataRequired()])
    type_of_purchase = SelectField(
        "Type of Purchase",choices=[("New"),("Non-automatic Renewal "),("Automatic Renewal")] ,validators=[DataRequired()])
   

class Status(FlaskForm):
    assignment = SelectField("Assign", choices=[])

    def set_choices(self, choices):
        self.assignment.choices = choices

# Checklist form Vendor
# Checklist form Software
