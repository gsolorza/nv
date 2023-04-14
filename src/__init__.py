from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)

sender_email_address = ""
email_server = "" # example, smtp.googlemail.com
email_server_port = 465
email_password = ""

app.config["SECRET_KEY"] = "54b555c45fc50eb75e3eb9a50794e6be"
app.config["SECURITY_PASSWORD_SALT"] = "mW3o3W9Riu6L4m2Z"
app.config.update(
    MAIL_SERVER=email_server,
    MAIL_PORT=email_server_port,
    MAIL_USE_SSL=True,
    MAIL_USE_TLS=False,
    MAIL_USERNAME=sender_email_address,
    MAIL_PASSWORD=email_password)
bcrypt = Bcrypt(app)
mail = Mail(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # type: ignore

from src import routes
