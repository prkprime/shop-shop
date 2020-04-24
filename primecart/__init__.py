from flask import Flask
from flask_login import LoginManager
from flask import request, redirect, render_template, url_for, flash
from flask_login import login_user, logout_user, login_required
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
    return User(u['_id'])

@app.route('/')
#@login_required
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = app.config['USERS_COLLECTION'].find_one({'_id' : request.form['username']})
        if user and User.validate_login(user['password'], request.form['password']):
            user_object = User(user['_id'])
            login_user(user_object)
            next = request.args.get('next')
            print("Logged in successfully!")
            return redirect(next or url_for('index'))
        print("Wrong username or password!")
    return render_template('login.html')
