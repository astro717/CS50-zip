import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
# igual tengo que hacer el import especifico de session que se vio en lecture

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        if "delete" in request.form:
            name_to_del = request.form.get("nameToDel")
            if not name_to_del:
                return redirect("/")
            # Elimina el registro por nombre si existe
            db.execute("DELETE FROM birthdays WHERE name = ?", name_to_del)
            return redirect("/")

        # Add the user's entry into the database
        name = request.form.get("name")
        if not name or db.execute("SELECT * FROM birthdays WHERE name= ?", name):
            redirect("/")

        month = request.form.get("month")
        if not month:
            redirect("/")
        elif int(month) < 1 or int(month) > 12:
            redirect("/")

        day = request.form.get("day")
        if not day:
            redirect("/")
        elif int(day) < 1 or int(day) > 31:
            redirect("/")

        db.execute("INSERT INTO birthdays (name, month, day) VALUES(?, ?, ?)", name, month, day)


        return redirect("/")


    else:

        # Display the entries in the database on index.html
        rows = db.execute("SELECT * FROM birthdays")

        return render_template("index.html", birthdays=rows)




