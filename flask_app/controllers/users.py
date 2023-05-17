
from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import user, chore
from flask_bcrypt import Bcrypt
from flask import flash
bcrypt = Bcrypt(app)




@app.route('/')
def home():
    return render_template('logreg.html')

@app.route('/register', methods=['POST'])
def register():
    if not user.User.validate_reg(request.form):
        session['first_name'] = request.form['first_name']
        session['last_name'] = request.form['last_name']
        session['email'] = request.form['email']
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }
    user_id = user.User.create_user(data)
    session['user_id'] = user_id
    session['user_firstname'] = request.form['first_name']
    print(session['user_id'])
    return redirect('/dashboard')


@app.route('/login', methods=['POST'])
def login():
    data = {
        "email": request.form['email']
    }
    user_in_db = user.User.get_user_by_email(data)
    if not user_in_db:
        flash("Invalid email/password combination", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid email/password combination", "login")
        return redirect('/')
    session['user_id'] = user_in_db.id
    session['user_firstname'] = user_in_db.first_name
    return redirect('/dashboard')

# @app.route('/dashboard')
# def dashboard():
#     if session['user_id']:
#         data = {'id': session['user_id']}
#         return render_template('dashboard.html', user_chores=chore.Chore.get_chores_of_creator(data))
#     else:
#         return redirect('/')

@app.route('/dashboard')
def dashboard():
    user_chore = chore.Chore.get_chores_of_creator({'id': session['user_id']})
    return render_template('dashboard.html', user_chore=user_chore, session=session)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')