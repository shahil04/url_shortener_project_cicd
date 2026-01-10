
from flask import Flask, request, redirect, render_template, session, flash
import string, random
import MySQLdb
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'  # Change this in production

# Database config (UPDATE THESE  updates 2)
DB_HOST = "database-1.cud2siaa2jqh.us-east-1.rds.amazonaws.com"
DB_USER = "admin"
DB_PASSWORD = "1234root"
DB_NAME = "url_db"

def get_db():
    return MySQLdb.connect(
        host=DB_HOST,
        user=DB_USER,
        passwd=DB_PASSWORD,
        db=DB_NAME
    )

def generate_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

@app.route("/", methods=["GET", "POST"])
def index():
    short_url = None
    if request.method == "POST":
        long_url = request.form['long_url']
        code = generate_code()

        db = get_db()
        cur = db.cursor()
        cur.execute(
            "INSERT INTO urls (short_code, long_url) VALUES (%s, %s)",
            (code, long_url)
        )
        db.commit()
        cur.close()

        short_url = request.host_url + code

    return render_template("index.html", short_url=short_url)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()
        
        if not all([name, email, subject, message]):
            return render_template("contact.html", error="All fields are required!")
        
        # Here you could save to database or send email
        # For now, we'll just show a success message
        return render_template("contact.html", success="Thank you for contacting us! We'll get back to you soon.")
    
    return render_template("contact.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        
        if not email or not password:
            return render_template("login.html", error="Email and password are required!")
        
        # Here you would check against database
        # For now, we'll just show a demo message
        # In production, you'd verify credentials and set session
        return render_template("login.html", success="Login successful! (Demo mode)")
    
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        
        if not all([name, email, password, confirm_password]):
            return render_template("register.html", error="All fields are required!")
        
        if password != confirm_password:
            return render_template("register.html", error="Passwords do not match!")
        
        if len(password) < 6:
            return render_template("register.html", error="Password must be at least 6 characters long!")
        
        # Here you would save to database
        # For now, we'll just show a success message
        return render_template("register.html", success="Registration successful! You can now login.")
    
    return render_template("register.html")

@app.route("/<code>")
def redirect_url(code):
    db = get_db()
    cur = db.cursor()
    cur.execute(
        "SELECT long_url FROM urls WHERE short_code=%s", (code,)
    )
    result = cur.fetchone()

    if result:
        cur.execute(
            "UPDATE urls SET click_count = click_count + 1 WHERE short_code=%s",
            (code,)
        )
        db.commit()
        cur.close()
        return redirect(result[0])
    else:
        cur.close()
        return "URL not found", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
