from flask import render_template, request, redirect, url_for, flash, session, g
from flask_login import login_required, logout_user, current_user, login_user
from src.forms import LoginForm, InitialFormSales, ChecklistFormSales, Vendor, Software, Cisco, CustomerForm, replicateForm, is_data_validated, encap_form
from src import app, login_manager, bcrypt, schema
from src.schema import Status
from src.crud import get_user, get_role, get_customer, create_form, create_vendor, create_software, display_partial_form, display_full_form, get_user_role, apply_form_changes
from src.db import db
from pprint import pprint

@login_manager.user_loader
def load_user(user_id):
    return get_user("id", user_id, db())

@app.before_request
def assign_role_name_to_user():
    path = request.path
    pathList = ["/mychecklist"]

    if path in pathList:
        query = schema.Query(column="id", value=current_user.role_id)
        role = get_role(query, db())
        current_user.role_name = role.role_name

    if path.startswith("/form"):
        query = schema.Query(column="role_name", value="admin")
        admin_role = get_role(query, db())
        g.admin = admin_role

@app.route("/", methods=["GET", "POST"])
def login():

    form = LoginForm()
    if current_user.is_authenticated:  # type: ignore
        query = schema.Query(
            column="id", value=current_user.role_id)  # type: ignore
        role = get_role(query, db())
        return render_template("home.html", role=role)

    if form.validate_on_submit():
        user = get_user("email", form.email.data.lower(), db())
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            flash("You Have been logged In!", "primary")
            login_user(user, remember=form.remember.data)
            query = schema.Query(column="id", value=user.role_id)
            role = get_role(query, db())
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
    role = get_role(query, db())
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
    customer = CustomerForm()
    all_forms = []
    role_list = get_role(schema.Query(), db())
    pre_sales_role = get_role(schema.Query(
        column="role_name", value="PreSales"), db())
    pre_sales = get_user_role(
        pre_sales_role.id, db())  # type: ignore
    form.set_choices([pre_sale.name for pre_sale in pre_sales], form.pre_sales_name.name)
    form.set_choices([role.role_name for role in role_list if role.id != current_user.role_id and role.role_name != "admin"], form.status.name)  # type: ignore
    if request.method == "POST":
        pprint(request.form)
        customers = [dict(customer) for customer in get_customer(schema.Query(), db())] # type: ignore   
        cisco_quantity = request.form.get("cisco_quantity")
        vendor_quantity = request.form.get("vendor_quantity")
        software_quantity = request.form.get("software_quantity")
        cisco_has_data = request.form.get("cisco_has_data")
        vendor_has_data = request.form.get("vendor_has_data")
        software_has_data = request.form.get("software_has_data")
        forms_cisco = replicateForm(Cisco(), request.form) if not cisco_quantity \
        else replicateForm(Cisco(),  request.form, int(cisco_quantity))
        forms_vendor = replicateForm(Vendor(), request.form) if not vendor_quantity \
        else replicateForm(Vendor(),  request.form, int(vendor_quantity))
        forms_software = replicateForm(Software(), request.form) if not software_quantity \
        else replicateForm(Software(),  request.form, int(software_quantity))
        form.client_manager_name.data = current_user.name
        all_forms.append(form)
        if cisco_has_data:
            all_forms.extend(forms_cisco)
        if vendor_has_data:
            all_forms.extend(forms_vendor)
        if software_has_data:
            all_forms.extend(forms_software)
        if is_data_validated(all_forms):
            result = []
            new_form = schema.CreateForm(
                sales_force_id = form.sales_force_id.data,
                purchase_order = form.purchase_order.data,
                quote_direct = form.quote_direct.data,
                client_manager_name = form.client_manager_name.data,
                pre_sales_name = form.pre_sales_name.data,
                customer_id = form.customer_id.data,
                comments = form.comments.data,
                status = form.status.data,
                customer_address = form.customer_address.data,
                customer_contact_name = form.customer_contact_name.data,
                customer_contact_phone = form.customer_contact_phone.data,
                customer_contact_email = form.customer_contact_email.data,
                dispatch_address = form.dispatch_address.data,
                dispatch_receiver_name = form.dispatch_receiver_name.data,
                dispatch_receiver_phone = form.dispatch_receiver_phone.data,
                dispatch_receiver_email = form.dispatch_receiver_email.data
            )
            checklist = create_form(new_form, db())
            result.append(checklist.message)
            if checklist.message.get(schema.MessageType.formCreated):
                if cisco_has_data:
                    for form in forms_cisco:
                        new_cisco_form = schema.CreateCisco(
                                form_id = checklist.message[schema.MessageType.formCreated][0].id,
                                cisco_deal_id = form.cisco_deal_id.data,
                                cisco_account_manager_name = form.cisco_account_manager_name.data,
                                cisco_account_manager_phone = form.cisco_account_manager_phone.data,
                                cisco_account_manager_email = form.cisco_account_manager_email.data,
                                cisco_smart_account = form.cisco_smart_account.data,
                                cisco_virtual_account = form.cisco_virtual_account.data
                        )
                        cisco = create_vendor(new_cisco_form, db())
                        result.append(cisco.message)
                if vendor_has_data:
                    for form in forms_vendor:
                        new_vendor_form = schema.CreateVendor(
                            form_id = checklist.message[schema.MessageType.formCreated][0].id,
                            vendor_deal_id = form.vendor_deal_id.data,
                            vendor_name = form.vendor_name.data,
                            vendor_account_manager_name = form.vendor_account_manager_name.data,
                            vendor_account_manager_phone = form.vendor_account_manager_phone.data, 
                            vendor_account_manager_email = form.vendor_account_manager_email.data
                        )
                        vendor = create_vendor(new_vendor_form, db())
                        result.append(vendor.message)
                if software_has_data:
                    for form in forms_software:
                        new_software_form = schema.CreateSoftware(
                            form_id = checklist.message[schema.MessageType.formCreated][0].id,
                            software_type = form.software_type.data,
                            duration_time = form.duration_time.data,
                            customer_contact = form.customer_contact.data,
                            subscription_id = form.subscription_id.data,
                            start_date = form.start_date.data,
                            type_of_purchase = form.type_of_purchase.data
                        )
                        software = create_software(new_software_form, db())
                        result.append(software.message)
            flash(f"{result}", "primary")
            print("VALIDATED")
            return redirect(url_for("mychecklist"))
        flash(
        f'initial information, added correctly!', 'primary')
        return render_template("checklist.html", form=form, forms_vendor=forms_vendor, forms_software=forms_software, forms_cisco=forms_cisco, customer=customer, customers=customers)
    return redirect(url_for("initial"))


@app.route('/test', methods=["GET", "POST"])
def test():
    return render_template("about.html")


@app.route('/mychecklist', methods=["GET"])
@login_required
def mychecklist():
    forms = []
    if request.method == "GET":
        data = request.args.get("sales_force_id")
        if current_user.role_name == "admin":
            query = schema.Query()
            forms = [dict(form) for form in display_partial_form(query, db())]
            return render_template("mychecklist.html", title="Histoy Checklist", form_history=forms)
        elif data:
            assigned_forms = []
            query = schema.Query(column="sales_force_id", value=data)
            forms = [dict(form) for form in display_partial_form(query, db())]
            for form in forms:
                if form.status == current_user.role_name:
                    assigned_forms.append(form)
            return render_template("mychecklist.html", title="Histoy Checklist", form_history=assigned_forms)
        elif not data:
                query = schema.Query(column="status", value=current_user.role_name)
                forms = [dict(form) for form in display_partial_form(query, db())]         
                return render_template("mychecklist.html", title="Histoy Checklist", form_history=forms)

    return render_template("mychecklist.html", title="Histoy Checklist", form_history=forms)

@app.route('/history', methods=["GET"])
@login_required
def history():
    query = schema.Query()
    form_history = [dict(form) for form in display_partial_form(query, db())]
    return render_template("history_checklist.html", title="Histoy Checklist", form_history=form_history)


@app.route("/form/<int:form_id>", methods=["GET", "POST"])
def form_update(form_id):
    query = schema.Query(column="id", value=form_id)
    role_list = get_role(schema.Query(), db())
    print("asdasdad")
    form_data = display_full_form(query, db())
    pprint(form_data)
    pre_sales_role = get_role(schema.Query(column="role_name", value="PreSales"), db())
    pl_role = get_role(schema.Query(column="role_name", value="P&L"), db())
    pre_sales = get_user_role(pre_sales_role.id, db())  # type: ignore
    form = ChecklistFormSales()
    form.set_choices(choices=[pre_sale.name for pre_sale in pre_sales], field_name=form.pre_sales_name.name)
    form.set_choices(choices=[role.role_name for role in role_list if role.role_name != "admin"], field_name=form.status.name)  # type: ignore
    if current_user.role_id == pl_role.id:
        form.status.choices.append(schema.Status.completed.value)
    form.client_manager_name.data = form_data.form.client_manager_name
    customer = CustomerForm()
    customers = [dict(customer) for customer in get_customer(schema.Query(), db())] # type: ignore
    cisco_has_data = True if form_data.cisco else False
    vendor_has_data = True if form_data.vendor else False
    software_has_data = True if form_data.software else False
    cisco_quantity = len(form_data.cisco) if cisco_has_data else 1 # type: ignore
    vendor_quantity = len(form_data.vendor) if vendor_has_data else 1 # type: ignore
    software_quantity = len(form_data.software) if software_has_data else 1 # type: ignore
    if request.method == "POST":
        pprint(request.form)
        all_forms = []
        form.db_validation = False
        all_forms.append(form)
        forms_cisco = replicateForm(Cisco(),  request.form, int(cisco_quantity))
        forms_vendor = replicateForm(Vendor(),  request.form, int(vendor_quantity))
        forms_software = replicateForm(Software(),  request.form, int(software_quantity))
        if cisco_has_data:
            all_forms.extend(forms_cisco)
        if vendor_has_data:
            all_forms.extend(forms_vendor)
        if software_has_data:
            all_forms.extend(forms_software)
        if is_data_validated(all_forms):
            apply_form_changes(form_data, request.form, db())
            return redirect(url_for("mychecklist"))
        return render_template("form_update.html", title="Checklist", form=form, forms_vendor=forms_vendor, forms_cisco=forms_cisco, forms_software=forms_software, customer=customer, customers=customers, pl_role=pl_role)
    customer.customer_name.data = form_data.customer.customer_name
    customer.customer_rut.data = form_data.customer.customer_rut
    form = encap_form(form, form_data)
    forms_cisco = encap_form(Cisco(), form_data) if cisco_has_data else replicateForm(Cisco(),  request.form, cisco_quantity)
    forms_vendor = encap_form(Vendor(), form_data) if vendor_has_data else replicateForm(Vendor(),  request.form, vendor_quantity)
    forms_software = encap_form(Software(), form_data) if software_has_data else replicateForm(Software(),  request.form, software_quantity)
    if form.status.data == schema.Status.completed.value and current_user.name != "admin":
        return render_template("form_history.html", title="Checklist History", form=form, forms_vendor=forms_vendor, forms_cisco=forms_cisco, forms_software=forms_software, customer=customer, customers=customers, pl_role=pl_role)
    return render_template("form_update.html", title="Checklist", form=form, forms_vendor=forms_vendor, forms_cisco=forms_cisco, forms_software=forms_software, customer=customer, customers=customers, pl_role=pl_role)
    

@app.route("/CreateCustomer",methods=["GET","POST"])
def CreateCustomer():
    customer = CustomerForm()
    return render_template("create_customer.html", title="Create Customer",customer=customer)