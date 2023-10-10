from flask import Flask
from flask import render_template,redirect
from flask import request
from db_conn import PG_CONN
import bcrypt
app=Flask(__name__)
print(app)
salt=bcrypt.gensalt()

@app.route('/')
def hi():
    return 'Hi'
@app.route("/reg")
def reg():
    return 'Hi welocome to register'

@app.route("/register")
def render_register_page():
    return render_template("register1.html")

@app.route("/register/user", methods=["POST"])
def create_user():
    name = request.form["name"]
    password = request.form["password"].encode("utf-8")
    passwrod_hash = bcrypt.hashpw(password, salt).decode("utf-8")
    print(passwrod_hash)
    print(name,password)
    conn = PG_CONN.get_db_connection()
    curr = conn.cursor()
    QUERY = "INSERT INTO user_profile(name,password) values(%s, %s);"
    curr.execute(QUERY, (name,passwrod_hash))
    conn.commit()
    curr.close()
    conn.close()
    return redirect("/register")


if __name__=="__main__":
    app.run(debug=True)