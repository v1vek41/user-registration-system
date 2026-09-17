from flask import Flask, render_template, request,redirect,session
import mysql.connector

app = Flask(__name__)
app.secret_key="mysecretkey"


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mypassword",
    database = "db"
)

cursor = mydb.cursor()
print("my sql connected")

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    username= session.get("username")
    return render_template("dashboard.html",username=username)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]

    query = "select username,password from user_details where username=%s and password=%s"
    cursor.execute(query,(username,password))

    result = cursor.fetchone()

    if result:
        session["username"]=result[0]
        return redirect("/dashboard")
    else:
        return "Login failed\nIncorrect username or password"

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method  == "GET":
        return render_template("register.html")
    username = request.form["username"]
    password = request.form["password"]

    query = "insert into user_details(username,password) values(%s,%s)"
    cursor.execute(query,(username,password))

    mydb.commit()

    return "regitered successfully!!"

app.run(debug=True)
