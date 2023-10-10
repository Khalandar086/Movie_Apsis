

from flask import Flask
from flask import request,redirect
from flask import render_template
from db_conn import PG_CONN
from datetime import datetime
app = Flask(__name__)


@app.route("/movie", methods=['GET', 'POST'])
def movies():
    if request.method == "GET":
        conn = PG_CONN.get_db_connection()
        curr = conn.cursor()
        sql = f"""select id, first_name, last_name from actors;"""
        curr.execute(sql)
        result_set = curr.fetchall()

        sql = """select m.name, a.first_name, m.director, m.production, m.languages, m.rating from movies m inner join movieactors ma on 
                    ma.movie_id=m.id inner join actors a on a.id=ma.actors_id;"""
        curr.execute(sql)
        movies_rs = curr.fetchall()
        movies_list = {}
        for datum in movies_rs:
            name = datum[0]
            actor = datum[1]
            if name in movies_list:
                movie_info = movies_list.get(name)
                movie_info.get("actors").append(actor)
            else:
                movies_list[name] = {
                    "name": name,
                    "director": datum[2],
                    "rating": datum[5],
                    "production": datum[3],
                    "language": datum[4],
                    "actors": [actor]
                }

        data = []
        for datum in result_set:
            d = {}
            d["name"] = datum[1] + " " + datum[2]
            d["id"] = datum[0]
            data.append(d)
        return render_template("create_movie.html", actors=data, movies=movies_list)
    if request.method == "POST":
        movie_name = request.form["movie-name"]
        director = request.form["director-name"]
        actors = request.form.getlist("actor-names")
        language = request.form["language"]
        production = request.form["production-name"]
        rating = request.form["rating"]
        actors = [int(id) for id in actors]
        conn = PG_CONN.get_db_connection()
        curr = conn.cursor()
        sql = f"""INSERT INTO movies(name, director, languages, production, rating) values(%s, %s, %s, %s, %s) RETURNING id;"""
        curr.execute(sql, (movie_name, director, language, production, rating))
        movie_id = curr.fetchone()[0]
        conn.commit()
        for actor_id in actors:
            sql = f"""INSERT INTO movieactors(movie_id, actors_id) values(%s, %s);"""
            curr.execute(sql, (movie_id, actor_id))
        conn.commit()
        curr.close()
        conn.close()
        return redirect("/movie")


@app.route("/actor", methods=['GET', 'POST'])
def actor():
    if request.method == "GET":
        conn = PG_CONN.get_db_connection()
        curr = conn.cursor()
        sql = f"""select * from actors;"""
        curr.execute(sql)
        result_set = curr.fetchall()
        data = []
        for datum in result_set:
            d = {}
            d["first_name"] = datum[1]
            d["last_name"] = datum[2]
            d["industry"] = datum[3]
            d["gender"] = "Male" if datum[4] == "M" else "Female"
            d["dob"] = str(datum[5])
            data.append(d)
        return render_template("create_actors.html",actors=data)
    elif request.method == "POST":
        first_name=request.form["actor-first_name"]
        last_name= request.form["actor-last_name"]
        industry=request.form["actor-industry"]
        gender=request.form["actor-gender"]
        dob=request.form["actor-dob"]
        dob=datetime.strptime(dob,"%Y-%m-%d")


        conn = PG_CONN.get_db_connection()
        curr=conn.cursor()
        sql = f"""INSERT INTO actors(first_name, last_name, gender, industry, dob) values(%s, %s, %s, %s, %s);"""
        curr.execute(sql, (first_name, last_name, industry, gender, dob))
        conn.commit()
        curr.close()
        conn.close()
        return redirect("/actor")

@app.route("/user", methods=['GET', 'POST'])
def user():
    if request.method == "GET":
        conn = PG_CONN.get_db_connection()
        curr = conn.cursor()
        sql = f"""select * from user_registration;"""
        curr.execute(sql)
        result_set = curr.fetchall()
        data = []
        for datum in result_set:
            d = {}
            d["first_name"] = datum[1]
            d["last_name"] = datum[2]
            d["gender"] = "Male" if datum[3] == "M" else "Female"
            data.append(d)
        return render_template("register1.html")
    elif request.method == "POST":
        first_name = request.form["user-first_name"]
        last_name = request.form["user-last_name"]
        gender = request.form["user-gender"]

        conn = PG_CONN.get_db_connection()
        curr = conn.cursor()
        sql = f"""INSERT INTO user_registration(first_name, last_name, gender) values(%s, %s, %s);"""
        curr.execute(sql, (first_name, last_name,gender))
        conn.commit()
        curr.close()
        conn.close()
        return redirect("/user")


@app.route("/suchi", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        conn = PG_CONN.get_db_connection()
        curr = conn.cursor()
        sql = f"""select * from user_login;"""
        curr.execute(sql)
        result_set = curr.fetchall()
        data = []
        for datum in result_set:
            d = {}
            d["user_name"] = datum[1]
            d["password"] = datum[2]
            data.append(d)
        return render_template("user.html")
    elif request.method == "POST":
        user_name = request.form["suchi-user_name"]
        password = request.form["suchi-password"]


        conn = PG_CONN.get_db_connection()
        curr = conn.cursor()
        sql = f"""INSERT INTO user_login(user_name,password) values(%s, %s);"""
        curr.execute(sql, (user_name,password))
        conn.commit()
        curr.close()
        conn.close()
        return redirect("/suchi")




if __name__ == "__main__":
    app.run(debug=True)