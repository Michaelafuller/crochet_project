from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.model_user import User
from flask_app.models.model_magazine import Magazine
from flask_app.controllers import controller_user

@app.route('/magazines/<int:id>')
def show_one_magazine(id):
    if 'uuid' not in session:
        return redirect('/')

    data = {
        'id': id
    }
    user = Magazine.get_one_magazine(data)

    return render_template('/details.html', user=user)


@app.route('/magazines/form')
def new_magazine():
    if 'uuid' not in session:
        return redirect('/')

    return render_template('create.html')

@app.route('/magazines/create', methods=['post'])
def create_sighting():
    if 'uuid' not in session:
        return redirect('/')


    data = {
        **request.form,
        'user_id' : session['uuid']
    }

    if not Magazine.validate_magazine(data):
        return redirect ('/magazines/form')

    Magazine.create_magazine(data)

    return redirect('/dashboard')

@app.route('/magazines/<int:id>/delete')
def delete_one_magazine(id):
    if 'uuid' not in session:
        return redirect('/')

    data = {
        'id' : id
    }

    Magazine.delete_one_magazine(data)

    return redirect (f"/users/{session['uuid']}")
