from flask import render_template, request, redirect, url_for, flash, session, g
from flask_login import login_required, logout_user, current_user, login_user
from src.forms import LoginForm, RegistrationForm, ForgotPassword, ResetPassword,InitialFormSales, ChecklistFormSales, Vendor, Software, Cisco, CustomerForm,RequestAccount, replicateForm, is_data_validated, encap_form
from src import app, login_manager, bcrypt, schema, mail, sender_email_address
from src.crud import get_user, get_role, get_customer, create_form, create_vendor, create_software, display_partial_form, display_full_form, get_user_role, apply_form_changes, update_user_password, create_customers, create_user
import json
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return get_user("id", user_id)

@app.before_request
def assign_role_name_to_user():
    if current_user.is_authenticated:
        query = schema.Query(column="id", value=current_user.role_id)
        role = get_role(query)
        current_user.role_name = role.role_name

    query = schema.Query(column="role_name", value="admin")
    admin_role = get_role(query)
    g.admin = admin_role

    query = schema.Query(column="role_name", value="Sales")
    sales_role = get_role(query)
    g.sales = sales_role



@app.route("/", methods=["GET", "POST"])
def login():

    form = LoginForm()
    if current_user.is_authenticated:  # type: ignore
        return render_template("home.html")

    if form.validate_on_submit():
        user = get_user("email", form.email.data.lower())
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            flash("You Have been logged In!", "success")
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else render_template('home.html')

        else:
            flash("Invalid username or password", "danger")

    return render_template("login.html", title="login", form=form)


@app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/home")
@login_required
def home():
    return render_template("home.html")


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
    pre_sales_role = get_role(schema.Query(
        column="role_name", value="PreSales"))
    pre_sales = get_user_role(
        pre_sales_role.id)  # type: ignore
    form.set_choices([pre_sale.name for pre_sale in pre_sales], form.pre_sales_name.name)
    form.set_choices([pre_sales_role.role_name], form.status.name)  # type: ignore
    if request.method == "POST":
        customers = [dict(customer) for customer in get_customer(schema.Query())] if get_customer(schema.Query()) else None # type: ignore
        if not customers:
            flash("You need to have customers before creating a checklist", "danger")
            return redirect(url_for("create_customer"))
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
                comments = form.format_comments_save(current_user.name, current_user.role_name),
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
            checklist = create_form(new_form)
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
                        cisco = create_vendor(new_cisco_form)
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
                        vendor = create_vendor(new_vendor_form)
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
                        software = create_software(new_software_form)
                        result.append(software.message)
            flash(f"Form have been created successfully!", "success")
            return redirect(url_for("mychecklist"))
        return render_template("checklist.html", form=form, forms_vendor=forms_vendor, forms_software=forms_software, forms_cisco=forms_cisco, customer=customer, customers=customers)
    return redirect(url_for("initial"))

@app.route('/mychecklist', methods=["GET"])
@login_required
def mychecklist():
    forms = []
    if request.method == "GET":
        if current_user.role_name == "admin":
            query = schema.Query()
            forms = [dict(form) for form in display_partial_form(query)]
            return render_template("mychecklist.html", title="Histoy Checklist", form_history=forms)
        else:
            query = schema.Query(column="status", value=current_user.role_name)
            forms = [dict(form) for form in display_partial_form(query)]         
            return render_template("mychecklist.html", title="Histoy Checklist", form_history=forms)

    return render_template("mychecklist.html", title="Histoy Checklist", form_history=forms)

@app.route('/history', methods=["GET"])
@login_required
def history():
    query = schema.Query()
    form_history = [dict(form) for form in display_partial_form(query)]
    return render_template("history_checklist.html", title="Histoy Checklist", form_history=form_history)


@app.route("/form/<int:form_id>", methods=["GET", "POST"])
@login_required
def form_update(form_id):
    query = schema.Query(column="id", value=form_id)
    role_list = get_role(schema.Query())
    form_data = display_full_form(query)
    pre_sales_role = get_role(schema.Query(column="role_name", value="PreSales"))
    pl_role = get_role(schema.Query(column="role_name", value="P&L"))
    pre_sales = get_user_role(pre_sales_role.id)  # type: ignore
    comments = json.loads(form_data.form.comments) if form_data.form.comments else False
    form = ChecklistFormSales()
    form.set_choices(choices=[pre_sale.name for pre_sale in pre_sales], field_name=form.pre_sales_name.name)
    form.set_choices(choices=[role.role_name for role in role_list if role.role_name != "admin"], field_name=form.status.name)  # type: ignore
    if current_user.role_id == pl_role.id or current_user.role_id == g.admin.id:
        form.status.choices.append(schema.Status.completed.value)
    elif current_user.role_id == g.sales.id:
        form.status.choices = [pre_sales_role.role_name]
    form.client_manager_name.data = form_data.form.client_manager_name
    customer = CustomerForm()
    customers = [dict(customer) for customer in get_customer(schema.Query())] # type: ignore
    cisco_has_data = True if form_data.cisco else False
    vendor_has_data = True if form_data.vendor else False
    software_has_data = True if form_data.software else False
    cisco_quantity = len(form_data.cisco) if cisco_has_data else 1 # type: ignore
    vendor_quantity = len(form_data.vendor) if vendor_has_data else 1 # type: ignore
    software_quantity = len(form_data.software) if software_has_data else 1 # type: ignore
    if request.method == "POST":
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
            apply_form_changes(form_data, request.form, current_user.name, current_user.role_name)
            return redirect(url_for("mychecklist"))
        return render_template("form_update.html", title="Checklist", form=form, forms_vendor=forms_vendor, forms_cisco=forms_cisco, forms_software=forms_software, customer=customer, customers=customers, pl_role=pl_role, comments=comments)
    customer.customer_name.data = form_data.customer.customer_name
    customer.customer_rut.data = form_data.customer.customer_rut
    form = encap_form(form, form_data)
    forms_cisco = encap_form(Cisco(), form_data) if cisco_has_data else replicateForm(Cisco(),  request.form, cisco_quantity)
    forms_vendor = encap_form(Vendor(), form_data) if vendor_has_data else replicateForm(Vendor(),  request.form, vendor_quantity)
    forms_software = encap_form(Software(), form_data) if software_has_data else replicateForm(Software(),  request.form, software_quantity)
    if current_user.role_id == g.admin.id:
        return render_template("form_update.html", title="Checklist", form=form, forms_vendor=forms_vendor, forms_cisco=forms_cisco, forms_software=forms_software, customer=customer, customers=customers, pl_role=pl_role, comments=comments)
    elif form.status.data != current_user.role_name:
        form.status.choices = [form.status.data]
        return render_template("form_history.html", title="Checklist History", form=form, forms_vendor=forms_vendor, forms_cisco=forms_cisco, forms_software=forms_software, customer=customer, customers=customers, pl_role=pl_role, comments=comments)
    return render_template("form_update.html", title="Checklist", form=form, forms_vendor=forms_vendor, forms_cisco=forms_cisco, forms_software=forms_software, customer=customer, customers=customers, pl_role=pl_role, comments=comments)
    

@app.route("/create_customer",methods=["GET","POST"])
@login_required
def create_customer():
    customer = CustomerForm()
    if customer.validate_on_submit():
        new_customer = schema.CreateCustomer(
            customer_name=customer.customer_name.data,
            customer_rut=customer.customer_rut.data
        )
        response = create_customers(new_customer)
        if response:
            flash("Customer has been created successfully", "success")
            return render_template("create_customer.html", title="Create Customer",customer=customer)
        else:
            flash("Customer creation failed, contact Administrator", "danger")
            return render_template("create_customer.html", title="Create Customer",customer=customer)
    return render_template("create_customer.html", title="Create Customer",customer=customer)

@app.route("/forgot_password",methods=["GET","POST"])
def forgot_password():
    form = ForgotPassword()
    if form.validate_on_submit():
        serializer = Serializer(app.config["SECRET_KEY"])
        token = serializer.dumps(form.email.data, salt=app.config["SECURITY_PASSWORD_SALT"])
        url = url_for("reset_password", token=token, _external=True)
        try:
            msg = Message(
            "Reset Password Notification",
            sender=sender_email_address,
            recipients=[form.email.data]
            )
            msg.body = f"Click on this link to reset your password --> {url}"
            mail.send(msg)
        except Exception:
            flash("Error sending Email please contact Administrator", "danger")
            return render_template("forgot_password.html", title="Forgot Password ",form=form)
        flash("An email has been sent to you with a link to reset your password", "success")
        return render_template("forgot_password.html", title="Forgot Password ",form=form)
    return render_template("forgot_password.html", title="Forgot Password ",form=form)

@app.route("/reset_password/<token>",methods=["GET","POST"])
def reset_password(token):
    form = ResetPassword()
    serializer = Serializer(app.config["SECRET_KEY"])
    if form.validate_on_submit():
        try:
            # Validate if the token is valid based on the max_age attribute
            email = serializer.loads(
                token,
                salt=app.config["SECURITY_PASSWORD_SALT"],
                max_age=600
            )
        except Exception:
            forgot_password_form = ForgotPassword()
            flash("The password reset link expired, please try generating a new one")
            return render_template("forgot_password.html", title="Forgot Password ",form=forgot_password_form)
        if request.method == "POST":
            try:
                update_user_password(email, form.password.data)
                flash("Try to log in with your new password", "success")
                return redirect(url_for("login"))
            except Exception:
                flash("Error setting the new password, please contact your Administrator", "danger")
                return render_template("reset_password.html", title="Reset Password",form=form)
    return render_template("reset_password.html", title="Reset Password",form=form)

@app.route("/create_account", methods=["GET","POST"])
@login_required
def create_account():
    if current_user.role_id == g.admin.id:
        form = RegistrationForm()
        role_list = get_role(schema.Query())
        form.set_role_choices(choices=[(role.id, role.role_name) for role in role_list if role.role_name != "admin"])
        if form.validate_on_submit():
            new_user = [schema.CreateUser(
                name=form.name.data,
                email=form.email.data,
                password=form.password.data,
                role_id=form.role.data
            )]
            create_user(new_user)
            flash("User has been created successfuly", "success")
            return redirect(url_for("home"))
        return render_template("register.html", title="Create Account",form=form)
    
    return redirect(url_for("login"))
