import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    # Consultar las acciones que posee el usuario y la cantidad de cada una
    user_stocks = db.execute("""
        SELECT stock_symbol, stock_name, SUM(quantity) as shares
        FROM user_stocks
        WHERE user_id = ?
        GROUP BY stock_symbol, stock_name
    """, user_id)

    # Obtener el saldo de efectivo del usuario
    cash_balance = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

    # Lista para almacenar los detalles de las acciones
    stocks = []
    total_portfolio_value = 0.0

    # Iterar sobre las acciones del usuario y obtener el precio actual de cada una
    for stock in user_stocks:
        current_price = lookup(stock["stock_symbol"])["price"]
        total_value = stock["shares"] * current_price
        total_portfolio_value += total_value

        # Agregar los detalles de la acción a la lista
        stocks.append({
            "name": stock["stock_name"],
            "shares": stock["shares"],
            "current_price": current_price,
            "total_value": total_value
        })

    # Calcular el total general (efectivo + valor de las acciones)
    grand_total = cash_balance + total_portfolio_value

    # Renderizar la plantilla index.html
    return render_template("index.html", stocks=stocks, cash_balance=cash_balance, grand_total=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")

    elif request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Validar símbolo
        if not symbol:
            return apology("Please enter a symbol", 400)

        # Validar que shares sea un número entero positivo
        try:
            shares = int(shares)
            if shares <= 0:
                return apology("Number of shares must be positive", 400)
        except ValueError:
            return apology("Number of shares must be a positive integer", 400)

        # Verificar que el símbolo existe
        stock = lookup(symbol)
        if stock is None:
            return apology("Invalid symbol", 400)

        price = stock["price"] * shares

        # Verificar fondos suficientes
        user_id = session["user_id"]
        rows = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        cash = rows[0]["cash"]

        if cash < price:
            return apology("Not enough cash", 400)

        # Realizar la transacción
        db.execute("""INSERT INTO transactions
                     (type, symbol, stock_name, quantity, price_stock, tot_price, user_id)
                     VALUES (?, ?, ?, ?, ?, ?, ?)""",
                   "buy", stock["symbol"], stock["name"], shares,
                   stock["price"], price, user_id)

        # Actualizar o insertar en user_stocks
        existing = db.execute("""SELECT quantity FROM user_stocks
                               WHERE user_id = ? AND stock_symbol = ?""",
                              user_id, symbol)

        if existing:
            db.execute("""UPDATE user_stocks
                         SET quantity = quantity + ?,
                             price_stock = ?,
                             tot_price = tot_price + ?
                         WHERE user_id = ? AND stock_symbol = ?""",
                       shares, stock["price"], price, user_id, symbol)
        else:
            db.execute("""INSERT INTO user_stocks
                         (user_id, stock_symbol, price_stock, tot_price, quantity, stock_name)
                         VALUES (?, ?, ?, ?, ?, ?)""",
                       user_id, symbol, stock["price"], price, shares, stock["name"])

        # Actualizar el efectivo del usuario
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?",
                   price, user_id)

        flash("Bought!")
        return redirect("/")

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]

    # recuperamos historial de transacciones
    transactions = db.execute("""SELECT type, symbol, stock_name, quantity, price_stock, tot_price, datetime
                                 FROM transactions
                                 WHERE user_id = ?
                                 ORDER BY datetime DESC""", user_id)
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")

    elif request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Please enter a symbol", 400)

        stock = lookup(symbol)
        if stock == None:
            return apology("Please enter a valid symbol", 400)

    return render_template("quoted.html",
                           stock_name=stock["name"],
                           stock_symbol=stock["symbol"],
                           stock_price=usd(stock["price"]))

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Valor por defecto  si no se proporciona
        card_number = request.form.get("card_number", "default")

        if not username:
            return apology("Please enter a username", 400)

        if not password or not confirmation:
            return apology("Please enter a password", 400)

        if password != confirmation:
            return apology("The password and the confirmation must be equal", 400)

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) > 0:
            return apology("username already exists", 400)

        # si no estaba pues lo añadimos a DB
        db.execute("INSERT INTO users (username, hash, card_number, cash) VALUES (?, ?, ?, ?)",
                   username, generate_password_hash(password), card_number, 10000)

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        session["user_id"] = rows[0]["id"]
        flash("You have registered successfully")
        return redirect("/")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]

    if request.method == "GET":

        symbols = db.execute(
            "SELECT DISTINCT stock_symbol FROM user_stocks WHERE user_id = ?", user_id)
        user_symbols = [symbol["stock_symbol"] for symbol in symbols]
        return render_template("sell.html", user_symbols=user_symbols)

        # return render_template("sell.html")

    elif request.method == "POST":
        symbol = request.form.get("symbol").upper()  # Convertir a mayúsculas
        shares = int(request.form.get("shares"))

        if not symbol:
            return apology("Please enter a symbol", 400)
        if not shares or shares < 1:
            return apology("Please enter a valid number of shares", 400)

        # Primero verificamos si el usuario tiene alguna acción
        print("Checking all stocks for user_id:", user_id)
        all_user_stocks = db.execute("SELECT * FROM user_stocks WHERE user_id = ?", user_id)
        print("All user stocks:", all_user_stocks)

        # Consulta específica para el símbolo
        stocks_owned = db.execute("""SELECT id, stock_symbol, stock_name, price_stock, tot_price, quantity
                                     FROM user_stocks
                                     WHERE UPPER(stock_symbol) = ? AND user_id = ?
                                     ORDER BY purchase_date ASC""", symbol, user_id)

        print("Input symbol:", symbol)
        print("Stocks owned for this symbol:", stocks_owned)

        # Si no hay stocks, devolver error
        if not stocks_owned:
            return apology("You do not own stocks from this company", 400)

        # Calcular total de acciones disponibles
        total_shares_owned = sum(stock["quantity"] for stock in stocks_owned)
        print(f"Total shares owned of {symbol}: {total_shares_owned}")

        # Verificar si tiene suficientes acciones
        if shares > total_shares_owned:
            return apology(f"You do not have enough shares. You own {total_shares_owned} shares of {symbol}", 400)

        remaining_shares = shares
        total_sale_profit = 0.0

        for stock in stocks_owned:
            if remaining_shares <= 0:
                break

            if stock["quantity"] >= remaining_shares:
                sale_profit = remaining_shares * stock["price_stock"]
                total_sale_profit += sale_profit

                if stock["quantity"] == remaining_shares:
                    db.execute("DELETE FROM user_stocks WHERE id = ?", stock["id"])
                else:
                    db.execute("UPDATE user_stocks SET quantity = ? WHERE id = ?",
                               stock["quantity"] - remaining_shares, stock["id"])

                db.execute("""INSERT INTO transactions (user_id, symbol, stock_name, quantity, type, price_stock, tot_price)
                              VALUES (?, ?, ?, ?, ?, ?, ?)""",
                           user_id, symbol, stock["stock_name"], -remaining_shares, "sell",
                           stock["price_stock"], sale_profit)

                break
            else:
                sale_profit = stock["quantity"] * stock["price_stock"]
                total_sale_profit += sale_profit
                db.execute("DELETE FROM user_stocks WHERE id = ?", stock["id"])

                db.execute("""INSERT INTO transactions (user_id, symbol, stock_name, quantity, type, price_stock, tot_price)
                              VALUES (?, ?, ?, ?, ?, ?, ?)""",
                           user_id, symbol, stock["stock_name"], -stock["quantity"], "sell",
                           stock["price_stock"], sale_profit)

                remaining_shares -= stock["quantity"]

        current_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
        db.execute("UPDATE users SET cash = ? WHERE id = ?",
                   current_cash + total_sale_profit, user_id)
        flash("Sell completed successfully!")

        return redirect("/")


@app.route("/config", methods=["GET", "POST"])
@login_required
def change_password():

    user_id = session["user_id"]

    if request.method == "GET":

        username = db.execute("SELECT username FROM users WHERE id = ?", user_id)
        nombre = username[0]['username']
        return render_template("config.html", username=nombre)

    elif request.method == "POST":

        username = request.form.get("username")
        old_password = request.form.get("current_password").strip()
        new_password = request.form.get("new_password").strip()

        if not old_password or not new_password:
            return apology("You have to enter all fields", 400)

        old_hash = db.execute("SELECT hash FROM users WHERE id = ?", user_id)

        if not old_hash:
            return apology("Something went wrong", 404)

        # vemos si ha puesto la password antigua bien
        if check_password_hash(old_hash[0]["hash"], old_password):
            if old_password == new_password:
                return apology("Your new password can not be the same as your current password", 400)
            db.execute("UPDATE users SET hash = ? WHERE id = ?",
                       generate_password_hash(new_password), user_id)
            flash("Paswword updated successfully!")
            return redirect("/")

        else:
            return apology("The password is invalid, enter your current password correctly", 400)
