from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, BooleanField, SelectField, EmailField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo


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
    vendor_deal_id = StringField("Cisco Vendor Deal ID", validators=[
                                 Length(min=5, max=30)], render_kw={"placeholder": "N/A"})
    purchase_order = StringField("Purchase Order", validators=[Length(
        min=4, max=20)], render_kw={"placeholder": "NoPO", "readonly": False})
    quote_direct = StringField("Quote Direct", validators=[
                               DataRequired(), Length(min=5, max=30)], render_kw={"readonly": False})
    sw_include = BooleanField("Software", default='checked')
    other_vendor_include = BooleanField("Other Vendor", default='checked')
    cisco_include = BooleanField(" Cisco Vendor", default='checked')
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
    pre_sales_name = StringField("Pre Sales Engineer Name", validators=[
                                 DataRequired(), Length(min=5, max=30)], render_kw={"readonly": False})
    date = DateField("Date", validators=[DataRequired()])
    customer_name = StringField("Customer Name", validators=[
                                DataRequired(), Length(min=5, max=30)], render_kw={"readonly": False})
    customer_rut = StringField("Customer RUT", validators=[
                               DataRequired(), Length(min=5, max=30)], render_kw={"readonly": False})
    customer_address = StringField("Customer Address", validators=[
                                   DataRequired(), Length(min=5, max=30)], render_kw={"readonly": False})
    customer_contact_name = StringField("Customer Contact Name", validators=[
                                        DataRequired(), Length(min=5, max=30)], render_kw={"readonly": False})
    customer_contact_phone = StringField("Customer Contact Phone", validators=[
                                         DataRequired(), Length(min=5, max=30)], render_kw={"readonly": False})
    customer_contact_email = EmailField("Customer Contact Email", validators=[
                                        DataRequired(), Length(min=5, max=30)], render_kw={"readonly": False})
    dispatch_address = StringField("Dispatch Address", validators=[
                                   DataRequired(), Length(min=5, max=30)], render_kw={"readonly": False})
    dispatch_receiver_name = StringField("Dispatch Receiver Name", validators=[
                                         DataRequired(), Length(min=5, max=30)], render_kw={"readonly": False})
    dispatch_receiver_phone = StringField("Dispatch Receiver Phone", validators=[
                                          DataRequired(), Length(min=5, max=30)], render_kw={"readonly": False})
    dispatch_receiver_email = EmailField("Dispatch Receiver Email", validators=[
                                         DataRequired(), Length(min=5, max=30)], render_kw={"readonly": False})

    comments = TextAreaField("Comments", validators=[DataRequired(), Length(
        min=5, max=2000)], render_kw={"placeholder": "Enter your comments"})

    submit = SubmitField("Submit")


class Vendor(FlaskForm):
    vendor_deal_id = StringField(
        "Deal ID", [Length(min=5, max=30)], render_kw={"readonly": False})
    vendor_name = StringField("Vendor Name", validators=[
                              DataRequired(), Length(min=5, max=10)])
    account_manager_name = StringField("Account Manager Name", validators=[
                                       DataRequired(), Length(min=5, max=10)])
    account_manager_phone = StringField("Account Manager Phone", validators=[
                                        DataRequired(), Length(min=5, max=15)])
    account_manager_email = EmailField(
        "Account Manager Email", validators=[DataRequired(), Email()])


class Cisco_vendor(FlaskForm):
    vendor_deal_id = StringField(
        "Deal ID", [Length(min=5, max=30)], render_kw={"readonly": False})
    account_manager_name = StringField("Account Manager Name", validators=[
                                       DataRequired(), Length(min=5, max=10)])
    account_manager_phone = StringField("Account Manager Phone", validators=[
                                        DataRequired(), Length(min=5, max=15)])
    account_manager_email = EmailField(
        "Account Manager Email", validators=[DataRequired(), Email()])
    smart_account = StringField("Smart Account", validators=[
                                DataRequired(), Length(min=5, max=30)], render_kw={"readonly": False})
    virtual_account = StringField("Virtual Account", validators=[
                                  DataRequired(), Length(min=5, max=30)], render_kw={"readonly": False})


class Software_Form(FlaskForm):
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
    preSalesValidation = SelectField("Pre Sales Validation")
    insidePreSalesValidation = SelectField("Inside Pre Sales Validation")
    plValidation = SelectField("P&L Valdiation")
    approved = SelectField("Approved")
# Checklist form Vendor
# Checklist form Software
