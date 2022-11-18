from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import DataRequired, Length, Email


class LoginForm(FlaskForm):

    email = StringField(
        "Email", validators=[DataRequired(), Email()]
    )
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class InitialFormSales(FlaskForm):
    sales_force_id = StringField("Sales Force ID", validators=[DataRequired(), Length(30)])
    vendor_deal_id = StringField("Deal ID", [Length(20)])
    purchase_order = StringField("Purchase Order", validators=[DataRequired(), Length(20)])
    quote_direct = StringField("Quote Direct", validators=[DataRequired(), Length(20)])
    submit = SubmitField("Create Form")

class ChecklistFormSales(FlaskForm):
    sale_note_id = StringField("Sale Note ID", validators=[Length(20)])
    sales_force_id = StringField("Sales Force ID", validators=[DataRequired(), Length(30)])
    vendor_deal_id = StringField("Deal ID", [Length(20)])
    purchase_order = StringField("Purchase Order", validators=[DataRequired(), Length(20)])
    quote_direct = StringField("Quote Direct", validators=[DataRequired(), Length(20)])
    client_manager_name = StringField("Sales Engineer Name", validators=[DataRequired(), Length(20)])
    pre_sales_name = StringField("Pre Sales Engineer Name", validators=[DataRequired(), Length(20)])
    date = DateField("Date", validators=[DataRequired()])
    customer_name = StringField("Customer Name", validators=[DataRequired(), Length(20)])            
    customer_rut = StringField("Customer RUT", validators=[DataRequired(), Length(20)])          
    customer_address = StringField("Customer Address", validators=[DataRequired(), Length(20)])       
    customer_contact_name = StringField("Customer Contact Name", validators=[DataRequired(), Length(20)])   
    customer_contact_phone = StringField("Customer Contact Phone", validators=[DataRequired(), Length(20)]) 
    customer_contact_email = StringField("Customer Contact Email", validators=[DataRequired(), Length(20)])
    dispatch_address = StringField("Dispatch Address", validators=[DataRequired(), Length(20)])       
    dispatch_receiver_name = StringField("Dispatch Receiver Name", validators=[DataRequired(), Length(20)]) 
    dispatch_receiver_phone = StringField("Dispatch Receiver Phone", validators=[DataRequired(), Length(20)])
    dispatch_receiver_email = StringField("Dispatch Receiver Email", validators=[DataRequired(), Length(20)])
    submit = SubmitField("Submit")

class Vendor(FlaskForm):
    vendor_name = StringField("Vendor Name", validators=[DataRequired(), Length(10)])
    account_manager_name = StringField("Account Manager Name", validators=[DataRequired(), Length(10)])
    account_manager_phone = StringField("Account Manager Phone", validators=[DataRequired(), Length(15)])
    account_manager_email = StringField("Account Manager Email", validators=[DataRequired(), Email()])
    smart_account = StringField("Smart Account", validators=[Length(20)])
    virtual_account = StringField("Virtual Account", validators=[Length(20)])

# Checklist form Vendor
# Checklist form Software
