from flask import Flask
from flask_login import LoginManager, current_user
from flask import request, redirect, render_template, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash
from pymongo.errors import DuplicateKeyError
from primecart.user import User

app = Flask(__name__)
app.config.from_object('config')
loginmanager = LoginManager()
loginmanager.init_app(app)
loginmanager.login_view = 'login'


@loginmanager.user_loader
def load_user(username):
    u = app.config['USERS_COLLECTION'].find_one({"_id": username})
    if not u:
        return None
    return User(u['_id'], u['user_type'])


@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = app.config['USERS_COLLECTION'].find_one({'_id': request.form['username']})
        if user and User.validate_login(user['password'], request.form['password']):
            user_object = User(user['_id'], user['user_type'])
            login_user(user_object)
            next = request.args.get('next')
            print("Logged in successfully!")
            if current_user.get_type() == 'admin':
                return redirect(url_for('admin'))
            return redirect(next or url_for('index'))
        print("Wrong username or password!")
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
        pass_hash = generate_password_hash(password, method='pbkdf2:sha256')
        try:
            app.config['USERS_COLLECTION'].insert_one({'_id': username, 'password': pass_hash, 'user_type': user_type})
            print('User created successfully')
            return redirect(url_for('login'))
        except DuplicateKeyError:
            print('User already exists')
    return render_template('register.html')
