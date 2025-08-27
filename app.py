from flask import Flask, render_template, request, redirect, url_for, flash, session
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

@app.route('/')
def homepage():
    # checks if a user is logged in w their accounr
    username = session.get("username")
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

        # stores username in session so homepage can use it after saving
        session['username'] = username  

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

        session['username'] = username  # log them in immediately after signup
        return redirect(url_for("homepage"))

    return render_template("signup.html")

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for("login"))

@app.route('/tip')
def tip():
    return render_template('tip.html')

@app.route('/userprofile')
def userprofile():
    # only if loggedin
    if 'username' not in session:
        flash("Please log in to view your profile.")
        return redirect(url_for("login"))
    return render_template('userprofile.html', username=session['username'])

@app.route('/aboutapp')
def aboutapp():
    return render_template('aboutapp.html')
@app.route('/quiz')
def quiz():
    return render_template('quiz.html')



if __name__ == "__main__":
    app.run(debug=True)
