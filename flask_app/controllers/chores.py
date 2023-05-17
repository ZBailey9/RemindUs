
from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import chore, user
from flask import flash






@app.route('/process/chore', methods=['POST'])
def process_chore():
    if not chore.Chore.validate_chore(request.form):
        session['chore'] = request.form['chore']
        session['time'] = request.form['time']
        session['questions'] = request.form['questions']
        return redirect('/dashboard')
    data = {
        'user_id': session['user_id'],
        'chore': request.form['chore'],
        'time': request.form['time'],
        'questions': request.form['questions'],
    }
    chore.Chore.create_chore(data)
    session['chore'] = ""
    session['time'] = ""
    session['questions'] = ""
    return redirect('/dashboard')

# @app.route('/edit/chore/<int:chore_id>')
# def edit_chore(chore_id):
#     if not session['user_id']:
#         return redirect('/')
#     data = {'id': chore_id}
#     return render_template('edit_chore.html', chore=chore.Chore.get_one_chore(data))

@app.route('/edit/chore/<int:chore_id>')
def edit_chore(chore_id):
    if not session['user_id']:
        return redirect('/')
    data = {'id': chore_id}
    chore_data = chore.Chore.get_one_chore(data)
    return render_template('edit_chore.html', chore=chore_data)


@app.route('/edit/process/<int:chore_id>', methods=['POST'])
def process_edit(chore_id):
    if not chore.Chore.validate_chore(request.form):
        return redirect(f'/edit/chore/{chore_id}')
    data = {
        'id': chore_id,
        'chore': request.form['chore'],
        'time': request.form['time'],
        'questions': request.form['questions'],
    }
    chore.Chore.edit_chore(data)
    return redirect('/dashboard')




@app.route('/delete/chore/<int:chore_id>')
def process_delete(chore_id):
    data = {'id': chore_id}
    chore.Chore.delete_chore(data)
    return redirect('/dashboard')

@app.route('/chores')
def all_chores_with_votes():
    if not session['user_id']:
        return redirect('/')
    return render_template('/all_chores.html', all_chores=chore.Chore.get_all_chores_with_votes())

@app.route('/show/<int:chore_id>')
def show_one_chore(chore_id):
    data = {
        'user_id': session['user_id'],
        'chore_id': chore_id
    }
    return render_template('show_one_chore.html', chore=chore.Chore.get_one_chore(data), user_is_voter=user.User.is_user_voter(data))

@app.route('/vote/plus_one/<int:chore_id>', methods=['POST'])
def plus_one_vote(chore_id):
    data = {
        'user_id': session['user_id'],
        'chore_id': chore_id
    }
    chore.Chore.add_vote(data)
    return redirect(f'/show/{chore_id}')

@app.route('/vote/minus_one/<int:chore_id>', methods=['POST'])
def minus_one_vote(chore_id):
    data = {
        'user_id': session['user_id'],
        'chore_id': chore_id
    }
    chore.Chore.subtract_vote(data)
    return redirect(f'/show/{chore_id}')