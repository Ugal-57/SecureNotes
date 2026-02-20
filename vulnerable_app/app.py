import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "insecure_secret_key"   # intentionally weak (vulnerable version)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Database connection
def get_db():
    conn = sqlite3.connect("database.db")
    return conn

# Home → Login
@app.route("/")
def home():
    return redirect("/login")

# Register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()

        # ❌ VULNERABLE — Plain text password storage
        cursor.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')")

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()

        # ❌ VULNERABLE — SQL Injection
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        result = cursor.execute(query).fetchone()

        conn.close()

        if result:
            session["user"] = username
            return redirect("/dashboard")

    return render_template("login.html")

#Dashboard
@app.route("/dashboard")
def dashboard():
    if "user" in session:

        conn = get_db()
        cursor = conn.cursor()

        notes = cursor.execute(
            f"SELECT note FROM notes WHERE username='{session['user']}'"
        ).fetchall()

        conn.close()

        return render_template("dashboard.html", user=session["user"], notes=notes)

    return redirect("/login")




@app.route("/add_note", methods=["POST"])
def add_note():
    if "user" in session:
        note = request.form["note"]

        conn = get_db()
        cursor = conn.cursor()

        # stable insert (prevents crash)
        cursor.execute(
            "INSERT INTO notes (username, note) VALUES (?, ?)",
            (session["user"], note)
        )

        conn.commit()
        conn.close()

    return redirect("/dashboard")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "user" in session:
        file = request.files["file"]

        if file:
            # ❌ VULNERABLE — no validation
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

    return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True,  port=5001)