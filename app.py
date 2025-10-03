from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.config['MYSQL_HOST'] = os.getenv("MYSQL_HOST")
app.config['MYSQL_USER'] = os.getenv("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD")
app.config['MYSQL_DB'] = os.getenv("MYSQL_DB")
mysql = MySQL(app)

# Home
@app.route("/")
def index():
    return render_template("index.html")

# Register GET
@app.route("/register", methods=["GET"])
def register_get():
    return render_template("register.html")

# Register POST
@app.route("/register", methods=["POST"])
def register_post():
    username = request.form['username']
    password = request.form['password']
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (%s,%s)", (username, password))
    mysql.connection.commit()
    cursor.close()
    return redirect("/")

# Add workout GET
@app.route("/add_workout", methods=["GET"])
def add_workout_get():
    return render_template("add_workout.html")

# Add workout POST
@app.route("/add_workout", methods=["POST"])
def add_workout_post():
    userId = request.form['userId']
    type_ = request.form['type']
    duration = request.form['duration']
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO workouts (user_id, type, duration) VALUES (%s,%s,%s)",
                   (userId, type_, duration))
    mysql.connection.commit()
    cursor.close()
    return redirect("/workouts")

# List workouts
@app.route("/workouts", methods=["GET"])
def list_workouts():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT user_id, type, duration, date FROM workouts")
    rows = cursor.fetchall()
    workouts = [{"userId": r[0], "type": r[1], "duration": r[2], "date": r[3]} for r in rows]
    cursor.close()
    return render_template("list_workouts.html", workouts=workouts)
