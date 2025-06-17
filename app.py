from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database connection details
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "password_baru",
    "database": "employee"
}

def get_db_connection():
    """Establish and return a new database connection."""
    return mysql.connector.connect(**DB_CONFIG)

# Route untuk menampilkan data
@app.route("/")
def index():
    db = get_db_connection()
    cursor = db.cursor()
    query = "SELECT * FROM users"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template("index.html", data=results)

# Route untuk membuat data baru
@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        name = request.form["name"]
        umur = request.form["umur"]
        email = request.form["email"]
        db = get_db_connection()
        cursor = db.cursor()
        query = "INSERT INTO users (name, umur, email) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, umur, email))
        db.commit()
        cursor.close()
        db.close()
        return redirect(url_for("index"))
    # Render a create form (ensure you have a `create.html`)
    return render_template("create.html")

# Route untuk mengupdate data
@app.route("/update/<id>", methods=["GET", "POST"])
def update(id):
    db = get_db_connection()
    cursor = db.cursor()
    if request.method == "POST":
        name = request.form["name"]
        umur = request.form["umur"]
        email = request.form["email"]
        query = "UPDATE users SET name = %s, umur = %s, email = %s WHERE id = %s"
        cursor.execute(query, (name, umur, email, id))
        db.commit()
        cursor.close()
        db.close()
        return redirect(url_for("index"))
    query = "SELECT * FROM users WHERE id = %s"
    cursor.execute(query, (id,))
    result = cursor.fetchone()
    cursor.close()
    db.close()
    return render_template("update.html", data_update=result)  # Use an `update.html` form

# Route untuk menghapus data
@app.route("/delete/<id>")
def delete(id):
    db = get_db_connection()
    cursor = db.cursor()
    query = "DELETE FROM users WHERE id = %s"
    cursor.execute(query, (id,))
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)