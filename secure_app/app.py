import os
import secrets
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, session, flash
import sqlite3

app = Flask(__name__)
bcrypt = Bcrypt(app) # Initialize Bcrypt for password hashing
app.secret_key = secrets.token_hex(32)  # Generate a secure random secret key for session management
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

        # ✅ SECURE — Hash the password before storing it
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_password)
        )
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

        # ✅ SECURE — parameterized query
        cursor.execute(
            "SELECT password FROM users WHERE username=?",
            (username,)
        )
        result = cursor.fetchone()
        conn.close()

        # ✅ check hashed password
        if result and bcrypt.check_password_hash(result[0], password):
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

# ✅ ADD LOGOUT ROUTE HERE
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# Add note (vulnerable)
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

# File upload (secured)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "pdf", "txt"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload", methods=["POST"])
def upload_file():
    if "user" not in session:
        return redirect("/login")

    file = request.files.get("file")

    if not file or file.filename == "":
        flash("No file selected", "error")
        return redirect("/dashboard")

    if not allowed_file(file.filename):
        flash("File type not allowed", "error")
        return redirect("/dashboard")

    filename = secure_filename(file.filename)
    random_name = secrets.token_hex(8) + "_" + filename
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], random_name)

    file.save(filepath)
    flash("File uploaded successfully", "success")

    return redirect("/dashboard")


@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Content-Security-Policy"] = (
    "default-src 'self'; "
    "script-src 'self' https://cdn.jsdelivr.net; "
    "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
    "img-src 'self' data:;"
)
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

if __name__ == "__main__":
    app.run(debug=True)