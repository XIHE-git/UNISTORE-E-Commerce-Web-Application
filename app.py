import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify
from flask_session import Session
from helpers import login_required, AccountUpdateForm, ProductUpdate, usd
from werkzeug.security import check_password_hash, generate_password_hash
import uuid
from datetime import datetime

# Configure application
app = Flask(__name__)

# Configure a secret key
app.config['SECRET_KEY'] = 'secrfgdgret'

# Ensure templates are auto-reloaded [Previously if you modify your codes, only codes in .py file (not html or css) can be reloaded]
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)  # session are how web servers remembers information about each user. enable staying logging in and saving items to own shopping cart

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///SecondHandTransaction.db")

# Custom filter
app.jinja_env.filters["usd"] = usd


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


"""
index --- A default route which renders the main page. The main page should be able to list all the products that are currently on sale. A login is required for this page.
          Both "GET" and "POST" methods are availiable. Users' input should be validated.
@return:
    "POST" method:
        index.html --- A html file which contains all the products
        row_sell --- A list of dictionary containing products that are on sale
    "GET" method:
        index.html --- A html file which contains all the products
        row_sell --- A list of dictionary containing products that are on sale
"""
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    # Users reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Users submitted a search request to filter products
        if "search" in request.form:
            product_name = request.form.get("product_name")
            product_type = request.form.get("product_type")
            university = request.form.get("university")
            address = request.form.get("address")
            price = request.form.get("priceselect")

            university_row = db.execute(
                "SELECT * FROM university WHERE name = ?", university.strip().upper())
            address_row = db.execute(
                "SELECT * FROM university WHERE address = ?", address.strip().upper())
            match_row = db.execute("SELECT * FROM university WHERE name = ? and address = ?",
                                   university.strip().upper(), address.strip().upper())

            # Check if an university is submitted
            if not university:
                flash("Empty University/College!")
            # Check if an address is submitted
            elif not address:
                flash("Empty University Address!")
            # Check if an university is correct
            elif len(university_row) != 1:
                flash("Incorrect University")
            # Check if an address is correct
            elif len(address_row) != 1:
                flash("Incorrect Address")
            # Check if the address match with university:
            elif len(match_row) != 1:
                flash("Address and College do not match")
            # If only address and university select
            elif not product_name and product_type.strip() == 'Product_Type: No Selection' and price.strip() == 'Price: Default':
                university_id = match_row[0]['id']
                row_sell = db.execute(
                    "select * from products where sold = 0 and university = ?", university_id)
                return render_template("index.html", row_sell=row_sell)
            # If only product name select
            elif product_name and product_type.strip() == 'Product_Type: No Selection' and price.strip() == 'Price: Default':
                university_id = match_row[0]['id']
                row_sell = db.execute("select * from products where sold = 0 and university = ? and name like ? or description like ?",
                                      university_id, "%" + product_name + "%", "%" + product_name + "%")
                return render_template("index.html", row_sell=row_sell)
            # If only product type select
            elif not product_name and product_type.strip() != 'Product_Type: No Selection' and price.strip() == 'Price: Default':
                university_id = match_row[0]['id']
                row_sell = db.execute(
                    "select * from products where sold = 0 and university = ? and type = ?", university_id, product_type.strip())
                return render_template("index.html", row_sell=row_sell)
            # If only price select
            elif not product_name and product_type.strip() == 'Product_Type: No Selection' and price.strip() != 'Price: Default':
                university_id = match_row[0]['id']
                if price.strip() == '$0-20':
                    row_sell = db.execute(
                        "select * from products where sold = 0 and university = ? and price >= 0 and price <= 20", university_id)
                    return render_template("index.html", row_sell=row_sell)
                elif price.strip() == '$20-$100':
                    row_sell = db.execute(
                        "select * from products where sold = 0 and university = ? and price >= 20 and price <= 100", university_id)
                    return render_template("index.html", row_sell=row_sell)
                else:
                    row_sell = db.execute(
                        "select * from products where sold = 0 and university = ? and price >= 100", university_id)
                    return render_template("index.html", row_sell=row_sell)
            # If product name and product type selected
            elif product_name and product_type.strip() != 'Product_Type: No Selection' and price.strip() == 'Price: Default':
                university_id = match_row[0]['id']
                row_sell = db.execute("select * from products where sold = 0 and university = ? and name like ? or description like ? and type = ?",
                                      university_id, "%" + product_name + "%", "%" + product_name + "%", product_type.strip())
                return render_template("index.html", row_sell=row_sell)
            # If product name and price selected
            elif product_name and product_type.strip() == 'Product_Type: No Selection' and price.strip() != 'Price: Default':
                university_id = match_row[0]['id']
                if price.strip() == '$0-20':
                    row_sell = db.execute("select * from products where sold = 0 and university = ? and price >= 0 and price <= 20 and name like ? or description like ?",
                                          university_id, "%" + product_name + "%", "%" + product_name + "%")
                    return render_template("index.html", row_sell=row_sell)
                elif price.strip() == '$20-$100':
                    row_sell = db.execute("select * from products where sold = 0 and university = ? and price >= 20 and price <= 100 and name like ? or description like ?",
                                          university_id, "%" + product_name + "%", "%" + product_name + "%")
                    return render_template("index.html", row_sell=row_sell)
                else:
                    row_sell = db.execute("select * from products where sold = 0 and university = ? and price >= 100 and name like ? or description like ?",
                                          university_id, "%" + product_name + "%", "%" + product_name + "%")
                    return render_template("index.html", row_sell=row_sell)
            # If product type and price selected
            elif not product_name and product_type.strip() != 'Product_Type: No Selection' and price.strip() != 'Price: Default':
                university_id = match_row[0]['id']
                if price.strip() == '$0-20':
                    row_sell = db.execute(
                        "select * from products where sold = 0 and university = ? and price >= 0 and price <= 20 and type = ?", university_id, product_type.strip())
                    return render_template("index.html", row_sell=row_sell)
                elif price.strip() == '$20-$100':
                    row_sell = db.execute(
                        "select * from products where sold = 0 and university = ? and price >= 20 and price <= 100 and type = ?", university_id, product_type.strip())
                    return render_template("index.html", row_sell=row_sell)
                else:
                    row_sell = db.execute(
                        "select * from products where sold = 0 and university = ? and price >= 100 and type = ?", university_id, product_type.strip())
                    return render_template("index.html", row_sell=row_sell)
            # If product name, price selected, and product type selected
            elif product_name and product_type.strip() != 'Product_Type: No Selection' and price.strip() != 'Price: Default':
                university_id = match_row[0]['id']
                if price.strip() == '$0-20':
                    row_sell = db.execute("select * from products where sold = 0 and university = ? and price >= 0 and price <= 20 and name like ? or description like ? and type = ?",
                                          university_id, "%" + product_name + "%", "%" + product_name + "%", product_type.strip())
                    return render_template("index.html", row_sell=row_sell)
                elif price.strip() == '$20-$100':
                    row_sell = db.execute("select * from products where sold = 0 and university = ? and price >= 20 and price <= 100 and name like ? or description like ? and type = ?",
                                          university_id, "%" + product_name + "%", "%" + product_name + "%", product_type.strip())
                    return render_template("index.html", row_sell=row_sell)
                else:
                    row_sell = db.execute("select * from products where sold = 0 and university = ? and price >= 100 and name like ? or description like ? and type = ?",
                                          university_id, "%" + product_name + "%", "%" + product_name + "%", product_type.strip())
                    return render_template("index.html", row_sell=row_sell)
            else:
                row_sell = db.execute("select * from products where sold = 0")
                return render_template("index.html", row_sell=row_sell)

    row_sell = db.execute("select * from products A where sold = 0")
    return render_template("index.html", row_sell=row_sell)


"""
login --- A route which renders the login html page. Users should be able to login on the register.html page. Both "GET" and "POST" methods are availiable.
          Users' login information should be validated. Current user's id should be remembered by system.
@return:
    "POST" method:
        redirect to the default route
    "GET" method:
        login.html --- A login html file
"""
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # Users reached route via POST (as by submitting a form via POST)
    # Users submitted a request to login
    if request.method == "POST":

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Empty Username!")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("must provide password")

        # Ensure username exists and password is correct
        elif len(rows) != 1:
            flash("Invalid Username and/or Password")

        elif not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("Invalid Username and/or Password")

        # If everything is correct
        else:
            # Remember which user has logged in
            session["user_id"] = rows[0]["id"]

            # Configure user's profile
            session["user_profile"] = rows[0]["image_file"]

            # Redirect user to home page
            return redirect("/")

    return render_template("login.html")


"""
register --- A route which renders the register html page or redirect to defaul route. Both "GET" and "POST" methods are availiable.
             Users' registeration information should be validated. Users should be able to register on the register.html page and log into website automatically after registrating.
             Current user's id should be remembered by system.

@return:
    "POST" method:
        redirect to the default route
    "GET" method:
        register.html --- A register html for users to register
"""
@app.route("/register", methods=["GET", "POST"])
def register():
    # Clear session
    session.clear()

    # Users reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))
        # Check if an username is submitted
        if not request.form.get("username"):
            flash("Empty Username!")
        # Check if a password is submitted
        elif not request.form.get("password"):
            flash("Empty Password")
        # Check if a confirmation is submitted
        elif not request.form.get("confirmation"):
            flash("Empty Passowrd Confirmation")
        # Check if a password and a confirmation are matched
        elif request.form.get("password") != request.form.get("confirmation"):
            flash("Password Must Match")
        # Check if an username is exist
        elif len(rows) != 0:
            flash("Username Already Exist")

        # If everything is fine （如果不用else会直接运行下面代码）
        else:
            # Save username and password to users table
            password = generate_password_hash(request.form.get("password"))
            db.execute("INSERT INTO users(username, hash) VALUES (?, ?)",
                       request.form.get("username"), password)
            # Remember which user has logged in
            row = db.execute(
                "SELECT * FROM users WHERE username = ?", request.form.get("username"))
            session["user_id"] = row[0]["id"]
            session["user_profile"] = "default.jpg"

            # Redirect to Main page
            return redirect("/")

    return render_template("register.html")


"""
logout --- a route to logout the current user and redirect to login route. Current users' id should be removed by system.
@return:
   redirect to login route
"""
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login route
    return redirect("/")


"""
save_image --- a function to save image into the server
@return:
    picture_name --- the filename of the pictures in string
"""
def save_image(picture_file, purpose='profile'):

    picture_name = picture_file.filename
    # For profile pictures
    if purpose == 'profile':
        # adding some unique code after picture_name
        picture_name = 'profile-' + str(uuid.uuid4())[:5] + picture_name
    # For product pictures
    if purpose == 'product':
        # adding some unique code after picture_name
        picture_name = 'product-' + str(uuid.uuid4())[:8] + picture_name
    picture_path = os.path.join(
        app.root_path, 'static/profile_pics', picture_name)
    # Saving image to the server
    picture_file.save(picture_path)
    return picture_name


"""
profile --- A route which renders profile.html, redirects to profile route, or flash warning massages. Both "GET" and "POST" methods are availiable.
            Users should be able to updating profile pictures, save money, update passwords, view account information, and save personal information to the server through this route.
@return:
    "POST" method:
        redirect to profile route or flash some warning messages

    "GET" method:
        profile.html --- A profile html for the current user's profile page
        form --- A python class containing functionalities of profile image
        img_url --- URL of the current user's profile image in string format
        money --- A numeric type of users' saving amount
        transaction_row --- A list of dictionary containing transaction information (order number, time, total_price, etc.) about every order
        transaction_product --- A list of dictionary containing sold products' information in each order
        product_sell --- A list of dictionary containing the information of all products that the user is selling and sold
        product_time --- A list of dictionary containing the sales time of products sold by the current user
"""
@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():

    form = AccountUpdateForm()
    try:
        # Users reached route via POST (as by submitting a form via POST)
        if request.method == "POST":
            # Users submited a "save" request to save money into accounts
            if "save" in request.form:
                # The amount of money that users want to save
                save_money = request.form.get("amount")
                # Check if has an input
                if not save_money:
                    flash("Empty Saving Input")
                # If saving is invalid
                elif float(save_money) <= 0:
                    flash("Please Enter a Positive number")
                # If everything is fine
                else:
                    # Update user saving
                    db.execute(
                        "UPDATE users SET money = money + (?) WHERE id = (?) ", save_money, session["user_id"])
                    flash("Succes!")
                    return redirect("/profile")

            # Users submited a "change_id" request to change username
            elif "change_id" in request.form:
                user_name = request.form.get("user_name")
                row = db.execute(
                    "select * from users where username = ?", user_name)
                # Ensure an user_name not empty:
                if not user_name:
                    flash("Empty Username")
                # Ensure username not exist in database
                elif len(row) > 0:
                    flash("Username Exist")
                else:
                    # Update username
                    db.execute(
                        "UPDATE users SET username = (?) WHERE id = (?) ", user_name, session["user_id"])
                    flash("Success!")

            # Users submited a request to update/change profile pictures
            elif form.validate_on_submit():
                img_file = save_image(form.picture.data)
                session["user_profile"] = img_file
                db.execute("UPDATE users SET image_file = (?) WHERE id = (?) ",
                           session["user_profile"], session["user_id"])
                return redirect("/profile")
    # If user did input an image
    except:
        flash("No image uploaded")

    # Profile Image URL
    img_url = os.path.join('../static/profile_pics', session["user_profile"])

    # Get the amount of saving from the current user account
    row0 = db.execute("select * from users where id = ?", session["user_id"])
    money = row0[0]["money"]

    # Get the transaction_information rows including order number, time, total_price, etc.
    transaction_row = db.execute(
        "select * from transactions_info where buyer_id = ?", session["user_id"])

    # Get product rows which have sold products' information in each order
    transaction_product = db.execute(
        "select A.order_num as order_num, C.name as name from transactions_info A, transactions B, products C where A.order_num = B.order_num and B.product_id = C.id and buyer_id = ?", session["user_id"])

    # Get the product rows which contain the information of all products that the user is selling and sold
    product_sell = db.execute(
        "select * from products where seller = ?", session["user_id"])

    # Get the product rows which contain the sales time of products sold by the current user
    product_time = db.execute(
        "select C.id as product_id, A.time as time from transactions_info A, transactions B, products C where A.order_num = B.order_num and B.product_id = C.id and seller = ?", session["user_id"])

    return render_template("profile.html", form=form, img_url=img_url, money=money, transaction_row=transaction_row, transaction_product=transaction_product, product_sell=product_sell, product_time=product_time)


"""
sell --- a route which renders sell.html or save products' information into database. Both "GET" and "POST" methods are availiable.
         The information about products should be validated.

@return:
    "POST" method:
        Save prodcuts information to database and flash warning messages

    "GET" method:
        sell.html --- A html page for users to submit a product selling request
        form --- A python class containing functionalities of profile image
"""
@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    form = ProductUpdate()
    try:
        # Users reached route via POST (as by submitting a form via POST)
        # If the user submit a product selling request
        if form.validate_on_submit():

            # Get information from user input
            product_name = request.form.get("product_name")
            price = request.form.get("price")
            product_type = request.form.get("product_type")
            description = request.form.get("description")
            university = request.form.get("university")
            address = request.form.get("address")

            # Get a list of dictionary about universities based on the user's input of unviersity name
            university_row = db.execute(
                "SELECT * FROM university WHERE name = ?", university.strip().upper())

            # Get a list of dictionary about universities based on the user's input of university address
            address_row = db.execute(
                "SELECT * FROM university WHERE address = ?", address.strip().upper())

            # Get a list of dictionary about unviersities based on the user's input of university name and address
            match_row = db.execute("SELECT * FROM university WHERE name = ? and address = ?",
                                   university.strip().upper(), address.strip().upper())

            # Check if a product name is submitted
            if not product_name:
                flash("Empty product_name!")
            # Check if a price is submitted
            elif not price:
                flash("Empty Price!")
            # Check if a product type is submitted
            elif not product_type:
                flash("Empty Product Type!")
            # Check if an university is submitted
            elif not university:
                flash("Empty University/College!")
            # Check if an address is submitted
            elif not address:
                flash("Empty University Address!")
            # Check if a description is submitted
            elif not description:
                flash("Empty Description")
            # Check if an university is correct
            elif len(university_row) != 1:
                flash("Incorrect University")
            # Check if an address is correct
            elif len(address_row) != 1:
                flash("Incorrect Address")
            # Check if the address and the password are match
            elif len(match_row) != 1:
                flash("Address and College do not match")
            # If everything is fine
            else:
                # Save image to the server
                img_file = save_image(form.picture.data, 'product')
                # save into product database
                db.execute("INSERT INTO products(name, seller, price, description, university, type, sold, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                           product_name, session["user_id"], float(price), description, match_row[0]['id'], product_type, 0, img_file)
                # Flash success image
                flash("success!")
    # No image uploaded
    except:
        flash("No image uploaded")
    return render_template("sell.html", form=form)


"""
cart --- A route which render cart.html, redirect to cart route, or redirect to buy route. Both "GET" and "POST" methods are availiable.
         This route should be able to pass necessary information of products for the shopping cart. This route should also handle requests about
         removing items from the shopping carts, adding items to the shopping cart, and buying all items in the shopping cart.

@return:
    "POST" method:
        redirect to cart route, redirect to buy route, or flash warnining messages

    "GET" method:
        cart.html --- A html page for shopping cart
        n --- An integer of the number of items in the cart
        carts_row --- A list of dictionary of products information in the shopping cart
        total --- A float of total product price in the shopping cart
"""
@app.route("/cart", methods=["GET", "POST"])
@login_required
def cart():
    # Ensure cart exists
    if "cart" not in session:
        session["cart"] = []
    # POST
    if request.method == "POST":
        # Add to Cart request
        if "add" in request.form:
            id = request.form.get("product_id")
            if id:
                if id not in session["cart"]:
                    session["cart"].append(id)
                    return redirect("\cart")
                else:
                    return redirect("\cart")
        # Remove item request
        elif "remove_item" in request.form:
            id = request.form.get("item_id")
            session["cart"].remove(id)
            return redirect("\cart")
        # Buy item request
        elif "buy" in request.form:
            # Get total price
            total_price = float(request.form.get("total_price"))
            # Check if the money is enough
            row = db.execute(
                "select * from users where id = ?", session["user_id"])
            user_money = row[0]['money']
            if total_price > user_money:
                flash("No Enough Money")
                return redirect("\cart")
            # If cart is empty:
            elif session["cart"] == []:
                flash("Empty Cart")
            # With enough money
            else:
                # Product Information Update
                for item_id in session["cart"]:
                    db.execute(
                        "UPDATE products SET sold = (?) WHERE id = (?) ", 1, item_id)
                # Generate a 12-letter/digits transaction number
                order_num = str(uuid.uuid4())[:12]
                # Insert transaction table
                for item_id in session["cart"]:
                    db.execute(
                        "INSERT INTO transactions(order_num, product_id) VALUES (?, ?)", order_num, item_id)
                # Insert transaction_info table
                currentDateTime = datetime.now()
                db.execute("INSERT INTO transactions_info(order_num, time, price, buyer_id) VALUES (?, ?, ?, ?)",
                           order_num, currentDateTime, total_price, session["user_id"])
                # Update buyer table
                db.execute("UPDATE users SET money = (?) WHERE id = (?) ",
                           user_money-total_price, session["user_id"])
                # Update seller saving
                if len(session["cart"]) == 1:
                    row_sell = db.execute(
                        "select * from products where id = ?", session["cart"])
                else:
                    row_sell = db.execute(
                        "select * from products where id in ?", session["cart"])
                for item in row_sell:
                    seller_id = item['seller']
                    product_price = item['price']
                    db.execute(
                        "UPDATE users SET money = money-? WHERE id = (?) ",  product_price, seller_id)
                # Clear shopping cart
                session["cart"] = []
                return redirect("\profile")

    # A list of dictionary of products information in the shopping cart
    carts_row = db.execute(
        "SELECT A.name as name, A.id as id, A.price as price, A.image as image, B.name as university_name FROM products A, university B WHERE A.university = B.id and A.id IN (?)", session["cart"])

    # Calculate total price
    total = 0
    for item in carts_row:
        total = total + item['price']

    return render_template("cart.html", n=len(session["cart"]), carts_row=carts_row, total=total)


"""
product --- a route which renders product.html. A product_id parameter is required as the input.
            to show detailed information about each product
@return:
    product.html --- A html page for every product page
    product_row --- A list of dictionary of specific product information
"""
@app.route("/product/<product_id>")
def product(product_id):

    # A list of dictionary of specific product information
    product_row = db.execute("select A.id as id, A.price as price, A.description as description, A.name as name, A.type as type, A.image as image, B.name as university, B.address as address from products A, university B where B.id = A.university and A.id = ?", product_id)

    return render_template("product.html", product_row=product_row)

"""
searchuniversity --- a route which returns a JSON file about specific university name information based on users' input about names

@return:
    unviersity --- A JSON format of the university name information
"""
@app.route("/searchuniversity")
def searchuniversity():
    q = request.args.get("q")
    if q:
        # A row of dictionary of the university information
        university = db.execute(
            "SELECT * FROM university WHERE name LIKE ? LIMIT 5", "%" + q + "%")
    else:
        university = []
    return jsonify(university)

"""
searchaddress --- a route which returns a JSON file about specific university address information based on users' input about address

@return:
    unviersity --- A JSON format of the university address information
"""
@app.route("/searchaddress")
def searchaddress():
    q = request.args.get("q")
    if q:
        # A row of dictionary of the university address information
        address = db.execute(
            "SELECT * FROM university WHERE address LIKE ? LIMIT 5", "%" + q + "%")
    else:
        address = []
    return jsonify(address)


"""
sort --- a route which returns a JSON file of sorted product list

@return:
    row --- A JSON format of the sorted product list
"""
@app.route("/sort")
def sort():
    q = request.args.get("q")
    if q:
        # Sort by Price from low to high
        if q.strip() == 'Sort by Price (Low to High)':
            row = db.execute(
                "SELECT * FROM products where sold = 0 order by price")
        # Sort by Price from high to low
        elif q.strip() == 'Sort by Price (High to Low)':
            row = db.execute(
                "SELECT * FROM products where sold = 0 order by price DESC")
        # Default Sort
        else:
            row = db.execute("SELECT * FROM products where sold = 0")
    else:
        row = []
    return jsonify(row)
