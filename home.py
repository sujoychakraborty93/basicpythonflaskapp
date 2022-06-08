# https://www.youtube.com/watch?v=4nzI4RKwb5I
# https://www.youtube.com/watch?v=4nzI4RKwb5I&list=PLzMcBGfZo4-n4vJJybUVV3Un_NFS5EOgX&index=3
from datetime import timedelta
from flask import Flask, redirect, url_for, render_template, request, session, flash
import json

app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=5)  # days=1

data_dummy = ''


def readdata():
    global data_dummy
    with open('datadummy.json', 'r') as datadummyfile:
        data_dummy = json.load(datadummyfile)
    datadummyfile.close()


def saveNewUser(uname, pswname):
    global data_dummy
    # with open('datadummy.json', 'r') as datadummyfile:
    #     data_dummy = json.load(datadummyfile)
    # datadummyfile.close()

    dict1 = {}
    dict1['username'] = uname
    dict1['password'] = pswname
    data_dummy['users'].append(dict1)

    with open('datadummy.json', 'w') as datadummyfile1:
        json.dump(data_dummy, datadummyfile1)
    datadummyfile1.close()


@app.route("/")
def base():
    global data_dummy
    # return "Hi this is homepage<h1>HELLO</h1>"
    # return render_template("index.html") # this is base html template and works perfectly
    if "sessionUser" in session:
        return render_template("home.html", header1="Homepage", arr=data_dummy['products'], usr=session["sessionUser"])
    else:
        flash("Please login!", "info")
        return redirect(url_for("login"))


@app.route("/home")
def home():
    return redirect(url_for("base"))


@app.route("/login", methods=['POST', 'GET'])
def login():
    global data_dummy
    if "sessionUser" in session:
        return redirect(url_for("base"))
    else:
        if request.method == "GET":
            return render_template("login.html", header1="Login")
        elif request.method == "POST":
            user = request.form["uname"]
            psw = request.form["pswname"]
            for item in data_dummy['users']:
                if user == item["username"] and psw == item["password"]:
                    session["sessionUser"] = user
                    session.permanent = True
                    flash("Login successful!", "info")
                    return redirect(url_for("base"))


@app.route("/custom/<cust>")
def custom(cust):
    # return f"Hello {cust}!"
    return render_template("home.html", header1=cust)


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template("register.html", header1="Registration")
    elif request.method == "POST":
        saveNewUser(request.form["uname"], request.form["pswname"])
        flash(f"Registration successful! Please login now", "info")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    if "sessionUser" in session:
        user = session["sessionUser"]
        flash(f"Hi {user}, you are now logged out!", "info")
    session.pop("sessionUser", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    global global_isLoggedIn

    readdata()
    global_isLoggedIn = False
    app.run(debug=True)
