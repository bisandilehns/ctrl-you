from flask import Flask, render_template, request, redirect, url_for, flash
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  

@app.route('/')
def homepage():
    return render_template("homepage.html")

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

        print("username:", username)
        print("password:", password)
        return "Login successful!"  

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

        # Uncomment for stronger password rules
        # if not re.search(r"[A-Za-z]", password) or not re.search(r"[0-9]", password):
        #     flash("Password must include both letters and numbers.")
        #     return redirect(url_for("signup"))

        if password != confirm:
            flash("Password and confirm password do not match.")
            return redirect(url_for("signup"))

        print("name:", name)
        print("username:", username)
        print("password:", password)
        print("confirm:", confirm)
        
        return redirect(url_for("homepage"))

    return render_template("signup.html") 
if __name__ == "__main__":
    app.run(debug=True)

from flask import render_template, session

@app.route('/dashboard')
def dashboard():
    username = session.get('username')  
    return render_template('dashboard.html', username=username)
session['username'] = user.username  # after successful login
