import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session

# Create the database and users table if it doesn't exist
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def add_user(username, password):
    """Add a new user. Returns True if successful, False if username exists."""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def check_user(username, password):
    """Check if a user exists with the given password."""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

@app.route('/')
def homepage():
    # checks if a user is logged in w their account
    username = session.get("username")
    return render_template("homepage.html", username=username)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
         
        if not username.isalpha():
            flash("Username must contain only letters.")
            return render_template("login.html")
        
        if len(password) < 7:
            flash("Password must be more than 6 characters.")
            return render_template("login.html")

        # stores username in session so homepage can use it after saving
        if check_user(username, password):
            session['username'] = username
            return redirect(url_for("homepage"))
        else:
            flash("Login unsuccessful: incorrect username or password.")
            return render_template("login.html")
    
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

        if add_user(username, password):
            session['username'] = username  # log them in immediately
            flash("Account created successfully!")
            return redirect(url_for("homepage"))
        else:
            flash("Username already exists!")
            return redirect(url_for("signup"))

    return render_template("signup.html")


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for("login"))

@app.route('/tip')
def tip():
    return render_template('tip.html')

from datetime import datetime

@app.route('/userprofile')
def userprofile():
    username = session.get('username')
    if username:
        # user is logged in → show profile info
        return render_template(
            'userprofile.html',
            username=username,
            join_date=datetime.now().strftime("%B %d, %Y")  # placeholder
        )
    else:
        # user not logged in → show login/signup form
        return render_template('login.html')


@app.route('/aboutapp')
def aboutapp():
    return render_template('aboutapp.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')


if __name__ == "__main__":
    app.run(debug=True)
