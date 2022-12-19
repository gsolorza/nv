from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, BooleanField, EmailField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp


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
                                 validators=[DataRequired(), Length(min=5, max=30)], render_kw={"readonly": False})
    purchase_order = StringField("Purchase Order", validators=[Length(
        min=4, max=20)], render_kw={"placeholder": "NoPO", "readonly": False})
    quote_direct = StringField("Quote Direct", validators=[
                               DataRequired(), Length(min=5, max=30)], render_kw={"readonly": False})
    include_software = BooleanField("Software", default='checked')
    include_vendor = BooleanField("Other Vendor", default='checked')
    include_cisco = BooleanField(" Cisco Vendor", default='checked')
    submit = SubmitField("Create Form")


class ChecklistFormSales(FlaskForm):
    sale_note = StringField("Sale Note ID", validators=[
        Length(min=5, max=30)], render_kw={"readonly": False})
    sales_force_id = StringField("Sales Force ID", validators=[
                                 DataRequired(), Length(min=5, max=30)])
    purchase_order = StringField("Purchase Order", validators=[
                                 DataRequired(), Length(min=5, max=30)], render_kw={"readonly": False})
    quote_direct = StringField("Quote Direct", validators=[
                               DataRequired(), Length(min=5, max=30)], render_kw={"readonly": False})
    client_manager_name = StringField("Sales Engineer Name", validators=[
                                      DataRequired(), Length(min=5, max=30)], render_kw={"readonly": False})
    pre_sales_name = SelectField("Pre Sales Engineer", validate_choice=False)
    date = DateField("Date", validators=[DataRequired()])
    customer_name = StringField("Customer Name", validators=[
                                DataRequired(), Length(min=5, max=30)], render_kw={"readonly": False})
    customer_rut = StringField("Customer RUT", validators=[
                               DataRequired(), Length(min=5, max=30)], render_kw={"readonly": False})
    customer_address = TextAreaField("Customer Address", validators=[
        DataRequired(), Length(min=5, max=300)], render_kw={"readonly": False})
    customer_contact_name = StringField("Customer Contact Name", validators=[
                                        DataRequired(), Length(min=5, max=30)], render_kw={"readonly": False})
    customer_contact_phone = StringField("Customer Contact Phone", validators=[
                                         DataRequired(), Length(min=5, max=30)], render_kw={"readonly": False})
    customer_contact_email = EmailField("Customer Contact Email", validators=[
                                        DataRequired(), Length(min=5, max=30)], render_kw={"readonly": False})
    dispatch_address = TextAreaField("Dispatch Address", validators=[
        DataRequired(), Length(min=5, max=300)], render_kw={"readonly": False})
    dispatch_receiver_name = StringField("Dispatch Receiver Name", validators=[
                                         DataRequired(), Length(min=5, max=30)], render_kw={"readonly": False})
    dispatch_receiver_phone = StringField("Dispatch Receiver Phone", validators=[
                                          DataRequired(), Length(min=5, max=30)], render_kw={"readonly": False})
    dispatch_receiver_email = EmailField("Dispatch Receiver Email", validators=[
                                         DataRequired(), Length(min=5, max=30)], render_kw={"readonly": False})

    include_software = BooleanField("Software", default='checked')
    include_vendor = BooleanField("Other Vendor", default='checked')
    include_cisco = BooleanField("Cisco Vendor", default='checked')
    comments = TextAreaField("Comments", validators=[DataRequired(), Length(
        min=5, max=2000)], render_kw={"placeholder": "Enter your comments"})

    submit = SubmitField("Submit")


class Vendor(FlaskForm):
    vendor_deal_id = StringField(
        "Deal ID", validators=[DataRequired(), Length(min=5, max=30)], render_kw={"readonly": False})
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
        "Deal ID", validators=[DataRequired(), Length(min=5, max=30)], render_kw={"readonly": False})
    cisco_account_manager_name = StringField("Account Manager Name", validators=[
                                       DataRequired(), Length(min=5, max=10), Regexp(f"[aA-zZ]+", message="The name must contain only letters")])
    cisco_account_manager_phone = StringField("Account Manager Phone", validators=[
                                        DataRequired(), Length(min=5, max=15)])
    cisco_account_manager_email = EmailField(
        "Account Manager Email", validators=[DataRequired(), Email()])
    cisco_smart_account = StringField("Smart Account", validators=[
                                DataRequired(), Length(min=5, max=30)], render_kw={"readonly": False})
    cisco_virtual_account = StringField("Virtual Account", validators=[
                                  DataRequired(), Length(min=5, max=30)], render_kw={"readonly": False})


class Software(FlaskForm):
    software_type = StringField(
        "Subscription/ Software Type", validators=[DataRequired()])
    duration_time = StringField(
        "Duration Time / Months", validators=[DataRequired()])
    customer_contact = StringField(
        "End Costumer contact", validators=[DataRequired()])
    subscription_id = StringField("Subscription ID")
    start_date = StringField("Start Day", validators=[DataRequired()])
    type_of_purchase = StringField(
        "Type of Purchase", validators=[DataRequired()])


class Status(FlaskForm):
    assignment = SelectField("Assign", validate_choice=False)
# Checklist form Vendor
# Checklist form Software
