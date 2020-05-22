from flask import Flask
from flask_login import LoginManager, current_user
from flask import request, redirect, render_template, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash
from pymongo.errors import DuplicateKeyError
from primecart.user import User
from primecart.parse_association_rules import new_rules, suggestions
from random import randint

app = Flask(__name__)
app.config.from_object('config')
loginmanager = LoginManager()
loginmanager.init_app(app)
loginmanager.login_view = 'login'


@loginmanager.user_loader
def load_user(username):
    u = app.config['USERS_COLLECTION'].find_one({"CustomerName": username})
    if not u:
        return None
    return User(u['CustomerName'], u['CustomerType'], u['CustomerId'])


@app.route('/')
@login_required
def index():
    print(current_user.get_type().lower())
    if current_user.get_type().lower() == 'admin':
        return redirect(url_for('admin'))
    products = list(app.config['PRODUCT_COLLECTION'].find().limit(20))
    cart_items = app.config['CARTS_COLLECTION'].find({'CustomerId': current_user.get_int_id()})
    cart_item_list = []
    cart_item_list_str = []
    for i in cart_items:
        cart_item_list_str.append(i['ProductId'])
        cart_item_list.append(int(i['ProductId']))
    print(cart_item_list)
    suggestion_ids = suggestions(cart_item_list, new_rules)
    print(suggestion_ids)
    suggested_products = app.config['PRODUCT_COLLECTION'].find(
        {'ProductId': {'$in': list(map(str, suggestion_ids.keys()))}})
    return render_template('index.html', products=products, cart_items_list_str=cart_item_list_str,
                           suggested_products=suggested_products)


@app.route('/admin')
@login_required
def admin():
    if current_user.get_type().lower() == 'admin':
        #return render_template('admin.html')
        return redirect("https://datastudio.google.com/embed/reporting/2eb5bb18-f630-4948-89b7-fb3dc23a3c5f/page/nHKRB")
    else:
        return 'What are you thinking? you are not an admin'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = app.config['USERS_COLLECTION'].find_one({'CustomerName': request.form['username']})
        if user and User.validate_login(user['CustomerPassword'], request.form['password']):
            user_object = User(user['CustomerName'], user['CustomerType'], user['CustomerId'])
            login_user(user_object)
            next = request.args.get('next')
            print(f'{current_user.get_id()} Logged in successfully!')
            if current_user.get_type().lower() == 'admin':
                return redirect(url_for('admin'))
            return redirect(next or url_for('index'))
        print('Wrong username or password!')
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']
        try:
            maxid = app.config['USERS_COLLECTION'].find().sort([('CustomerId', -1)]).limit(1)
            app.config['USERS_COLLECTION'].insert_one(
                {'CustomerId': int(maxid[0]['CustomerId']) + 1, 'CustomerName': username, 'CustomerPassword': password,
                 'CustomerType': user_type})
            print('User created successfully')
            return redirect(url_for('login'))
        except DuplicateKeyError:
            print('User already exists')
    return render_template('register.html')


@app.route('/add_to_cart', methods=['GET', 'POST'])
@login_required
def add_to_cart():
    if request.method == 'POST':
        product_id = request.form['id']
        customer_id = current_user.get_int_id()
        quantity = randint(1, 9)
        app.config['CARTS_COLLECTION'].insert_one(
            {'CustomerId': customer_id, 'ProductId': product_id, 'Quantity': quantity})
    return redirect(url_for('index'))


@app.route('/view_cart')
@login_required
def view_cart():
    if current_user.get_type() == 'admin':
        return '<p class="text-dark">Dude... why do you have a cart? you are admin xD</p> <a href="/admin" class="text-dark">GoTo admin</a>'
    cart_items = app.config['CARTS_COLLECTION'].find({'CustomerId': current_user.get_int_id()})
    cart_item_ids = []
    quantity = []
    count = 0;
    for i in cart_items:
        cart_item_ids.append(i['ProductId'])
        quantity.append(i['Quantity'])
        count += 1
    if count == 0:
        return '<p class="text-dark">Nothing here... Cart is empty</p> <a href="/" class="text-dark">Go back and do some shopping</a>'
    cart_products = app.config['PRODUCT_COLLECTION'].find({'ProductId': {'$in': cart_item_ids}})
    cart_products = dict(zip(quantity, cart_products))
    print(type(cart_products))
    return render_template('cart.html', cart_products=cart_products)


@app.route('/view_cart/empty_cart')
@login_required
def empty_cart():
    app.config['CARTS_COLLECTION'].remove({'CustomerId': current_user.get_int_id()})
    return redirect(url_for('view_cart'))


@app.route('/view_cart/check_out')
@login_required
def check_out():
    max_invoice_id = app.config['PURCHASE_COLLECTION'].find().sort([('InvoiceId', -1)]).limit(1)
    invoice_id = int(max_invoice_id[0]['InvoiceId'])
    products = app.config['CARTS_COLLECTION'].find(
        {'CustomerId': {'$in': [str(current_user.get_int_id()), int(current_user.get_int_id())]}})
    for product in products:
        app.config['PURCHASE_COLLECTION2'].insert_one(
            {'InvoiceId': invoice_id + 1, 'CustomerId': product['CustomerId'], 'ProductId': product['ProductId'],
             'Quantity': product['Quantity']})
    app.config['CARTS_COLLECTION'].remove({'CustomerId': current_user.get_int_id()})
    return '<p class="text-dark">Checkout successful... Cart is empty</p> <a href="/" class="text-dark">Go back and do some more shopping</a>'


@app.route('/view_cart/remove_product', methods=['GET', 'POST'])
@login_required
def remove_product():
    if request.method == 'POST':
        product_id = request.form['product_id']
        app.config['CARTS_COLLECTION'].remove({'CustomerId': current_user.get_int_id(), 'ProductId': product_id})
    return redirect(url_for('view_cart'))
