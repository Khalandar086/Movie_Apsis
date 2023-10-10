import bcrypt

from flask import Flask, request, render_template, redirect

from flask_login import LoginManager, login_user, login_required, logout_user

from util import get_db_connection

from util import UserProfile


app = Flask("Auth")

app.config["SECRET_KEY"] = "SECRET_KEY_TO_GEN_SESSION"

login_manager = LoginManager(app)
login_manager.login_view = "login"

salt = "$2b$12$KHi2VI7H2YhWeMSeF45zbO".encode("utf-8")


@login_manager.user_loader
def load_user(user_id):
    return UserProfile.get_user_by_id(user_id)


@app.route("/register")
def render_register_page():
    return render_template("registration.html")


@app.route("/register/user", methods=["POST"])
def create_user():
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"].encode("utf-8")
    passwrod_hash = bcrypt.hashpw(password, salt).decode("utf-8")
    print(passwrod_hash)
    print(name, email, password)
    conn = get_db_connection()
    curr = conn.cursor()
    QUERY = "INSERT INTO userprofile(name, email, password) values(%s, %s, %s);"
    curr.execute(QUERY, (name, email, passwrod_hash))
    conn.commit()
    curr.close()
    conn.close()
    return redirect("/register")


def is_valid_password(stored_password, input_password):
    input_password = input_password.encode("utf-8")
    hash = bcrypt.hashpw(input_password, salt).decode("utf-8")
    print(stored_password)
    print(hash)
    if hash == stored_password:
        return True
    else:
        return False


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("login.html")
    else:
        email = request.form["email"]
        password = request.form["password"]
        user = UserProfile.get_user_by_email(email)
        if user:
            valid = is_valid_password(user.password_hash, password)
            if valid:
                login_user(user)
                return redirect("/home")
            else:
                return render_template("login.html", invalid_user=True)
        else:
            return render_template("login.html", invalid_user=True)


@app.route("/home")
@login_required
def home():
    return render_template("home.html")


@app.route("/user/profile")
@login_required
def user_profile():
    return render_template("user_profile.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)
