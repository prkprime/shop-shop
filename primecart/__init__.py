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
    products = list(app.config['PRODUCT_COLLECTION'].find().limit(20))
    cart_items = app.config['CARTS_COLLECTION'].find({'CustomerId' : current_user.get_id()})
    cart_item_list = []
    cart_item_list_str = []
    for i in cart_items:
        cart_item_list_str.append(i['ProductId'])
        cart_item_list.append(int(i['ProductId']))
    print(cart_item_list)
    suggestion_ids = suggestions(cart_item_list, new_rules)
    print(suggestion_ids)
    suggested_products = app.config['PRODUCT_COLLECTION'].find({'ProductId' : {'$in' : list(map(str, suggestion_ids.keys()))}})

    return render_template('index.html', products=products, cart_items_list_str=cart_item_list_str, suggested_products=suggested_products)


@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = app.config['USERS_COLLECTION'].find_one({'CustomerName': request.form['username']})
        if user and User.validate_login(user['CustomerPassword'], request.form['password']):
            user_object = User(user['CustomerName'], user['CustomerType'])
            login_user(user_object)
            next = request.args.get('next')
            print(f'{current_user.get_username()} Logged in successfully!')
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
            maxid = app.config['USERS_COLLECTION'].find().sort([('CustomerId',-1)]).limit(1)
            app.config['USERS_COLLECTION'].insert_one({'CustomerId' : int(maxid[0]['CustomerId'])+1, 'CustomerName': username, 'CustomerPassword': password, 'CustomerType': user_type})
            print('User created successfully')
            return redirect(url_for('login'))
        except DuplicateKeyError:
            print('User already exists')
    return render_template('register.html')

@app.route('/index/add_to_cart', methods=['GET', 'POST'])
def add_to_cart():
    if request.method == 'POST':
        product_id = request.form['id']
        customer_id = current_user.get_id()
        quantity = randint(1, 9)
        app.config['CARTS_COLLECTION'].insert_one({'CustomerId' : customer_id, 'ProductId' : product_id, 'Quantity' : quantity})
    return redirect(url_for('index'))
