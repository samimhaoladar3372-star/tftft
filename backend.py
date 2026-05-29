from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "petshop_secret_key"

# =========================
# DATABASE CREATE
# =========================

def init_db():
    conn = sqlite3.connect("petshop.db")
    cursor = conn.cursor()

    # USERS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        email TEXT,
        password TEXT
    )
    """)

    # PRODUCTS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price INTEGER,
        image TEXT,
        description TEXT
    )
    """)

    # ORDERS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        product_name TEXT,
        payment_method TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# =========================
# HOME PAGE
# =========================

@app.route("/")
def home():

    conn = sqlite3.connect("petshop.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    conn.close()

    return render_template("index.html", products=products)

# =========================
# REGISTER
# =========================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("petshop.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO users (username, email, password)
        VALUES (?, ?, ?)
        """, (username, email, password))

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")

# =========================
# LOGIN
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("petshop.db")
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM users
        WHERE email=? AND password=?
        """, (email, password))

        user = cursor.fetchone()

        conn.close()

        if user:
            session["user"] = user[1]
            return redirect("/")

    return render_template("login.html")

# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect("/")

# =========================
# PRODUCT DETAILS
# =========================

@app.route("/product/<int:id>")
def product(id):

    conn = sqlite3.connect("petshop.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM products WHERE id=?
    """, (id,))

    product = cursor.fetchone()

    conn.close()

    return render_template("product.html", product=product)

# =========================
# CART
# =========================

cart = []

@app.route("/add-to-cart/<int:id>")
def add_to_cart(id):

    conn = sqlite3.connect("petshop.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM products WHERE id=?
    """, (id,))

    product = cursor.fetchone()

    conn.close()

    if product:
        cart.append(product)

    return redirect("/cart")

@app.route("/cart")
def view_cart():

    total = 0

    for item in cart:
        total += item[2]

    return render_template("cart.html", cart=cart, total=total)

# =========================
# PAYMENT PAGE
# =========================

@app.route("/payment", methods=["GET", "POST"])
def payment():

    if request.method == "POST":

        payment_method = request.form["payment"]

        username = session.get("user", "Guest")

        conn = sqlite3.connect("petshop.db")
        cursor = conn.cursor()

        for item in cart:

            cursor.execute("""
            INSERT INTO orders
            (username, product_name, payment_method)
            VALUES (?, ?, ?)
            """, (username, item[1], payment_method))

        conn.commit()
        conn.close()

        cart.clear()

        return redirect("/success")

    return render_template("payment.html")

# =========================
# SUCCESS PAGE
# =========================

@app.route("/success")
def success():
    return render_template("success.html")

# =========================
# ADMIN PANEL
# =========================

@app.route("/admin", methods=["GET", "POST"])
def admin():

    conn = sqlite3.connect("petshop.db")
    cursor = conn.cursor()

    if request.method == "POST":

        name = request.form["name"]
        price = request.form["price"]
        image = request.form["image"]
        description = request.form["description"]

        cursor.execute("""
        INSERT INTO products
        (name, price, image, description)
        VALUES (?, ?, ?, ?)
        """, (name, price, image, description))

        conn.commit()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    conn.close()

    return render_template("admin.html", products=products)

# =========================
# DELETE PRODUCT
# =========================

@app.route("/delete-product/<int:id>")
def delete_product(id):

    conn = sqlite3.connect("petshop.db")
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM products WHERE id=?
    """, (id,))

    conn.commit()
    conn.close()

    return redirect("/admin")

# =========================
# RUN SERVER
# =========================

if __name__ == "__main__":
    app.run(debug=True)
