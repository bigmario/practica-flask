from imghdr import tests
import os
from dotenv import load_dotenv
from flask import (
    Flask,
    request,
    make_response,
    redirect,
    url_for,
    render_template,
    session,
    flash,
)
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
import unittest

load_dotenv()

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET")
app.config.update(
    APP=os.getenv("FLASK_APP"),
    ENV=os.getenv("FLASK_ENV"),
    DEBUG=os.getenv("FLASK_DEBUG"),
)

todo_list = ["Comprar cafe", "Dormir", "Comer"]


class LoginForm(FlaskForm):
    username = StringField("Nombre de Usuario", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Enviar")


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner().run(tests)


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html", error=error)


@app.errorhandler(500)
def server_error(error):
    return render_template("500.html", error=error)


@app.route("/")
def index():
    user_ip = request.remote_addr
    response = make_response(redirect("/hello"))
    session["user_ip"] = user_ip
    return response


@app.route("/hello", methods=["GET", "POST"])
def hello():
    user_ip = session.get("user_ip")
    login_form = LoginForm()
    username = session.get("username")

    context = {
        "user_ip": user_ip,
        "todo_list": todo_list,
        "login_form": login_form,
        "username": username,
    }

    if login_form.validate_on_submit():
        username = login_form.username.data
        session["username"] = username
        flash("Nombre de usuario registrado con exito")

        return redirect(url_for("index"))

    return render_template("hello.html", **context)


if __name__ == "__main__":
    app.run()
