from flask import Flask, render_template, request, redirect, url_for
from forms import LoginForm
from database.db import SessionLocal
import secrets

app = Flask(__name__)

token = secrets.token_hex(16)
app.config["SECRET_KEY"] = token


def db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


@app.route("/", methods=["GET", "POST"])
def home():
    form = LoginForm()
    if form.validate_on_submit():
        if form.password.data == "admin":
            print("Authenticated successfully")
            return redirect(url_for("test"))
        else:
            print("Invalid credentials")
            return redirect(url_for("home"))
    return render_template("forms/index.html", title="Notas de Venta", form=form)


@app.route("/test", methods=["GET"])
def test():
    return "Data is good"


if __name__ == "__main__":
    app.run(debug=True)
