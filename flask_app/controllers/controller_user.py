from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.model_user import User
from flask_app.models.model_thread import Thread


@app.route('/lessons')
def lessons():
    return render_template('lessons.html')

@app.route('/logout')
def logout():
    if 'uuid' in session:
        del session['uuid']
    
    elif 'uuid' not in session:
        return redirect('/loginReg')

    return redirect('/')


# @app.route('/users')
# def show_users():
#     users = User.get_all()

#     return render_template('/users.html', users=users)


@app.route('/users/<int:id>')
def show_one(id):
    if 'uuid' not in session:
        return redirect('/')

    data = {
        'id': id
    }

    user = User.get_one(data)
    threads = Thread.get_all_threads_with_user()

    return render_template('/account.html', user=user, threads=threads)


# @app.route('/users/<int:id>/update')
# def update_one(id):
#     if 'uuid' not in session:
#         return redirect('/')

#     data = {
#         'id' : id
#     }
    
#     user = User.get_one(data)

#     return render_template('update.html', user=user)


@app.route('/users/update', methods=['post'])
def update_one_user():
    data = {
        'id' :session['uuid'],
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email']
    }
    if not User.validate_user_update(request.form):
        return redirect (f"/users/{session['uuid']}")

    User.update_one(data)

    return redirect (f"/users/{session['uuid']}")


# @app.route('/users/<int:id>/delete')
# def delete_one(id):
#     data = {
#         'id' : id
#     }

#     User.delete_one(data)

#     return redirect ('/users')
