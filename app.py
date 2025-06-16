from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Koneksi ke database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="employee"
)

# Membuat cursor
cursor = db.cursor()

# Route untuk menampilkan data
@app.route("/")
def index():
    query = "SELECT * FROM users"
    cursor.execute(query)
    results = cursor.fetchall()
    return render_template("index.html", data=results)

# Route untuk membuat data baru
@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        name = request.form["name"]
        umur = request.form["umur"]
        email = request.form["email"]
        query = "INSERT INTO users (name, umur, email) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, umur, email))
        db.commit()
        return redirect(url_for("index"))
    return render_template("create.html")

# Route untuk mengupdate data
@app.route("/update/<id>", methods=["GET", "POST"])
def update(id):
    if request.method == "POST":
        name = request.form["name"]
        umur = request.form["umur"]
        email = request.form["email"]
        query = "UPDATE users SET name = %s, umur = %s, email = %s WHERE id = %s"
        cursor.execute(query, (name, umur, email, id))
        db.commit()
        return redirect(url_for("index"))
    query = "SELECT * FROM users WHERE id = %s"
    cursor.execute(query, (id,))
    result = cursor.fetchone()
    return render_template("update.html", data=result)

# Route untuk menghapus data
@app.route("/delete/<id>")
def delete(id):
    query = "DELETE FROM users WHERE id = %s"
    cursor.execute(query, (id,))
    db.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
