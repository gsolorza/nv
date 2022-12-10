from flask import Flask, render_template, request, redirect, url_for, flash
from forms import LoginForm
from forms import RegistrationForm, InitialFormSales, ChecklistFormSales, Vendor, Software_Form, Cisco_vendor, Status
# from src.database.schema import Status
from db import SessionLocal, engine
import crud
import models
import secrets
import schema
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_required, logout_user, current_user, login_user
from pprint import pprint

models.Base.metadata.create_all(bind=engine)

app = Flask(__name__)

token = secrets.token_hex(16)
app.config["SECRET_KEY"] = token
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


@app.route("/", methods=["GET", "POST"])
def login():

    form = LoginForm()
    if current_user.is_authenticated:  # type: ignore
        role = crud.get_role("id", current_user.role_id, db())  # type: ignore
        return render_template("home.html", role=role)

    if form.validate_on_submit():
        user = crud.get_user("email", form.email.data.lower(), db())
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            flash("You Have been logged In!", "primary")
            login_user(user, remember=form.remember.data)
            role = crud.get_role("id", user.role_id, db())
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
    role = crud.get_role("id", current_user.role_id, db())  # type: ignore
    return render_template("home.html", role=role)


@app.route("/initial_form", methods=["GET", "POST"])
@login_required
def initial():
    form = InitialFormSales()
    if form.validate_on_submit():
        flash(
            f"initial information, added correctly {form.sales_force_id.data}!", "primary")
        return redirect(url_for("home"))
    return render_template("initial_form.html", title="initial Information", form=form)


@app.route('/checklist', methods=["GET", "POST"])
@login_required
def checklist():
    form = ChecklistFormSales()
    formvendor = Vendor()
    form_cisco_vendor = Cisco_vendor()
    formsw = Software_Form()

    if form.validate_on_submit():
        flash(
            f'initial information, added correctly {form.sales_force_id.data}!', 'primary')
        return redirect(url_for('home'))
    return render_template('checklist.html', form=form, formvendor=formvendor, formsw=formsw, form_cisco_vendor=form_cisco_vendor)


@app.route('/mychecklist', methods=["GET", "POST"])
@login_required
def mychecklist():
    query = schema.Query()
    if request.method == "POST":
        data = request.form.get("sales_force_id")
        query = schema.Query(column="sales_force_id", value=data)

    form_history = crud.display_partial_form(query, db())
    return render_template("mychecklist.html", title="Histoy Checklist", form_history=form_history)


@app.route('/history', methods=["GET", "POST"])
@login_required
def history():

    query = schema.Query()
    if request.method == "POST":
        data = request.form.get("sales_force_id")
        query = schema.Query(column="sales_force_id", value=data)

    form_history = crud.display_partial_form(query, db())
    return render_template("history_checklist.html", title="Histoy Checklist", form_history=form_history)


@app.route("/form/<int:form_id>", methods=["GET", "POST"])
def form_update(form_id):
    query = schema.Query(column="id", value=form_id)
    form_data = crud.display_full_form(query, db())
    form = ChecklistFormSales()
    print("Tu sabes")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
