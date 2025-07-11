from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
@app.route("/login", methods=["GET", "POST"])
def login ():
    if request.method == "POST":
        username = request.form ["username"]
        password = request.form ["password"]
        print("username:",username)
        print("password", password)
    return render_template("login.html")
app.run(debug=True)
