from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.login_model import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# home page


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/register', methods=['POST'])
def register():
    if not User.validate_registration(request.form):
        return redirect('/')
    # create the hash
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    # put the pw_hash into the data dictionary
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash
    }
    # call the create @classmethod on User
    user_id = User.create(data)
    # store user id into session
    session['user_id'] = user_id
    return redirect('/result')


@app.route('/login', methods=['POST'])
def login():
    message = "Invalid Email/Password"
    # check if the login and Password is empty
    if not request.form['login_email'] or not request.form['login_password']:
        flash(message)
        return redirect('/')
    user_in_db = User.get_by_email(request.form['login_email'])
    print(user_in_db)
    if not user_in_db:
        flash(message)
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['login_password']):
        flash(message)
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/result')


@app.route('/result')
def result():
    if "user_id" not in session:
        return redirect('/')
    one_user = User.get_one(session["user_id"])
    return render_template("result.html", one_user=one_user)


@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')
