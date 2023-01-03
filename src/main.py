from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from forms import LoginForm
from forms import RegistrationForm, InitialFormSales, ChecklistFormSales, Vendor, Software, Cisco, Status,CustomerForm
# from src.database.schema import Status
from db import SessionLocal, engine
import crud
import models
import schema
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_required, logout_user, current_user, login_user
from pprint import pprint

models.Base.metadata.create_all(bind=engine)

app = Flask(__name__)

app.config["SECRET_KEY"] = "54b555c45fc50eb75e3eb9a50794e6be"
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # type: ignore


def db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


@login_manager.user_loader
def load_user(user_id):
    return crud.get_user("id", user_id, db())

# @app.before_request
# def get_role():
#     role = crud.get_role(schema.Query(column="id", value=current_user.role_id), db())
#     current_user.role_name = role.role_name

@app.route("/", methods=["GET", "POST"])
def login():

    form = LoginForm()
    if current_user.is_authenticated:  # type: ignore
        query = schema.Query(
            column="id", value=current_user.role_id)  # type: ignore
        role = crud.get_role(query, db())
        return render_template("home.html", role=role)

    if form.validate_on_submit():
        user = crud.get_user("email", form.email.data.lower(), db())
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            flash("You Have been logged In!", "primary")
            login_user(user, remember=form.remember.data)
            query = schema.Query(column="id", value=user.role_id)
            role = crud.get_role(query, db())
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else render_template('home.html', role=role)

        else:
            flash("Invalid Credentials", "danger")

    return render_template("login.html", title="login", form=form)


@app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/home")
@login_required
def home():
    query = schema.Query(
        column="id", value=current_user.role_id)  # type: ignore
    role = crud.get_role(query, db())
    print(session)
    return render_template("home.html", role=role)


@app.route("/initial_form", methods=["GET", "POST"])
@login_required
def initial():
    initial_form = InitialFormSales()
    return render_template("initial_form.html", title="initial Information", form=initial_form)


@app.route('/checklist', methods=["GET", "POST"])
@login_required
def checklist():
    form = ChecklistFormSales()
    status = Status()
    customer = CustomerForm()
    role_list = crud.get_role(schema.Query(), db())
    pre_sales_role = crud.get_role(schema.Query(
        column="role_name", value="PreSales"), db())
    pre_sales = crud.get_user_role(
        pre_sales_role.id, db())  # type: ignore
    form.set_choices([pre_sale.name for pre_sale in pre_sales])
    status.set_choices([role.role_name for role in role_list if role.id != current_user.role_id])  # type: ignore
    if request.method == "POST":
        pprint(request.form)
        customers = [dict(customer) for customer in crud.get_customer(schema.Query(), db())] # type: ignore      
        cisco_quantity = request.form.get("cisco_quantity")
        vendor_quantity = request.form.get("vendor_quantity")
        software_quantity = request.form.get("software_quantity")
        forms_cisco = crud.replicateForm(Cisco(), request.form) if not cisco_quantity \
        else crud.replicateForm(Cisco(),  request.form, int(cisco_quantity))
        forms_vendor = crud.replicateForm(Vendor(), request.form) if not vendor_quantity \
        else crud.replicateForm(Vendor(),  request.form, int(vendor_quantity))
        forms_software = crud.replicateForm(Software(), request.form) if not software_quantity \
        else crud.replicateForm(Software(),  request.form, int(software_quantity))
        if form.validate_on_submit():
            # new_form = schema.CreateForm(
            #     sales_force_id = form.sales_force_id.data,
            #     purchase_order = form.purchase_order.data,
            #     quote_direct = form.quote_direct.data,
            #     client_manager_name = current_user.name,
            #     pre_sales_name = form.pre_sales_name.data,
            #     customer_id = form.customer_id.data,
            #     comments = form.comments.data,
            #     status = status.assignment.data,
            #     customer_address = form.customer_address,
            #     customer_contact_name = form.customer_contact_name,
            #     customer_contact_phone = form.customer_contact_phone,
            #     customer_contact_email = form.customer_contact_email,
            #     dispatch_address = form.dispatch_address.data,
            #     dispatch_receiver_name = form.dispatch_receiver_name.data,
            #     dispatch_receiver_phone = form.dispatch_receiver_phone.data,
            #     dispatch_receiver_email = form.dispatch_receiver_email.data
            # )
            flash(f"data validated successfully", "primary")
            print("VALIDATED")
            return render_template("checklist.html", form=form, forms_vendor=forms_vendor, forms_software=forms_software, forms_cisco=forms_cisco, status=status, customer=customer, customers=customers)
        flash(
            f'initial information, added correctly!', 'primary')
        return render_template("checklist.html", form=form, forms_vendor=forms_vendor, forms_software=forms_software, forms_cisco=forms_cisco, status=status, customer=customer, customers=customers)
    return redirect(url_for("initial"))


@app.route('/test', methods=["GET", "POST"])
def test():
    return render_template("about.html")


@ app.route('/mychecklist', methods=["GET", "POST"])
@ login_required
def mychecklist():
    query = schema.Query()
    if request.method == "POST":
        data = request.form.get("sales_force_id")
        query = schema.Query(column="sales_force_id", value=data)

    form_history = crud.display_partial_form(query, db())
    return render_template("mychecklist.html", title="Histoy Checklist", form_history=form_history)


@ app.route('/history', methods=["GET", "POST"])
@ login_required
def history():

    query = schema.Query()
    if request.method == "POST":
        data = request.form.get("sales_force_id")
        query = schema.Query(column="sales_force_id", value=data)

    form_history = crud.display_partial_form(query, db())
    return render_template("history_checklist.html", title="Histoy Checklist", form_history=form_history)


@ app.route("/form/<int:form_id>", methods=["GET", "POST"])
def form_update(form_id):
    query = schema.Query(column="id", value=form_id)
    form_data = crud.display_full_form(query, db())
    form = crud.encap_form(ChecklistFormSales(), form_data)
    form_vendor = crud.encap_form(Vendor(), form_data)
    form_cisco = crud.encap_form(Cisco(), form_data)
    form_software = crud.encap_form(Software(), form_data)
    return redirect(url_for("home"))

@app.route("/CreateCustomer",methods=["GET","POST"])
def CreateCustomer():
    customer = CustomerForm()
    return render_template("create_customer.html", title="Create Customer",customer=customer)



if __name__ == "__main__":
    app.run(debug=True, port=5000)
