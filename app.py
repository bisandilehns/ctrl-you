from flask import Flask, render_template, request, redirect, url_for, flash, session
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

@app.route('/')
def homepage():
   
    username = session.get('username', 'User')
    return render_template("homepage.html", username=username)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
         
    
        if not username.isalpha():
            flash("Username must contain only letters.")
            return redirect(url_for("login"))
        
        if len(password) < 7:
            flash("Password must be more than 6 characters.")
            return redirect(url_for("login"))

    
        session['username'] = username

        print("username:", username)
        print("password:", password)
        return redirect(url_for("homepage")) 

    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("yourname", "")
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        confirm = request.form.get("confirm", "")


        if not username.isalpha():
            flash("Username must contain only letters.")
            return redirect(url_for("signup"))

        if len(password) < 7:
            flash("Password must be more than 6 characters.")
            return redirect(url_for("signup"))

        if password != confirm:
            flash("Password and confirm password do not match.")
            return redirect(url_for("signup"))

   
        print("name:", name)
        print("username:", username)
        print("password:", password)
        print("confirm:", confirm)

        return redirect(url_for("homepage"))

    return render_template("signup.html")

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for("login"))

@app.route('/tip')
def tip():
    username = session.get('username', 'User')
    return render_template('tip.html', username=username)
    
@app.route('/userprofile')
def userprofile():
    username = session.get('username', 'User')
    return render_template("userprofile.html", username=username)

