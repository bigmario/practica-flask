from app import create_app
from app.forms import LoginForm
from flask import (
    request,
    make_response,
    redirect,
    url_for,
    render_template,
    session,
    flash,
)

import unittest

app = create_app()

todo_list = ["Comprar cafe", "Dormir", "Comer"]


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
