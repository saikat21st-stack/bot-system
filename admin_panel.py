from flask import Flask, request, redirect, session
import json

app = Flask(__name__)
app.secret_key = "secret123"

USERNAME = "admin"
PASSWORD = "1234"

def load_db():
    with open("database.json") as f:
        return json.load(f)

def save_db(data):
    with open("database.json", "w") as f:
        json.dump(data, f, indent=2)

@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == USERNAME and request.form["password"] == PASSWORD:
            session["logged"] = True
            return redirect("/dashboard")

    return '''
    <h2>Login</h2>
    <form method="post">
    Username:<input name="username"><br>
    Password:<input name="password" type="password"><br>
    <button>Login</button>
    </form>
    '''

@app.route("/dashboard")
def dashboard():
    if not session.get("logged"):
        return redirect("/")

    db = load_db()

    html = "<h2>Orders</h2><table border=1><tr><th>User</th><th>Order</th><th>Status</th></tr>"

    for o in db["orders"]:
        html += f"<tr><td>{o['user']}</td><td>{o['order']}</td><td>{o.get('status','Pending')}</td></tr>"

    html += "</table>"

    html += '''
    <h3>Add Product</h3>
    <form method="post" action="/add">
    Name:<input name="name"><br>
    Country:<input name="country"><br>
    Price:<input name="price"><br>
    <button>Add</button>
    </form>
    '''

    return html

@app.route("/add", methods=["POST"])
def add():
    db = load_db()

    name = request.form["name"]
    country = request.form["country"]
    price = request.form["price"]

    if name not in db["products"]:
        db["products"][name] = {}

    db["products"][name][country] = price

    save_db(db)

    return redirect("/dashboard")

app.run(host="0.0.0.0", port=3000)
