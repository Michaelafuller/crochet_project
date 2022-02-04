from flask import render_template, redirect, request, session, flash
from flask_app import app, bcrypt
from flask_app.models.model_user import User
from flask_app.controllers import controller_user
from flask_app.controllers import controller_thread


@app.route("/")
def index():

    return render_template("index.html")


@app.route('/drawingtool')
def drawing_tool():
    return render_template('drawingTool.html')

@app.route('/loginReg')
def login_reg():
    if 'uuid' in session:
        return redirect('/')

    return render_template('loginReg.html')

@app.route('/users/create', methods=['post'])
def register():
    if not User.validate_user(request.form):
        return redirect ('/loginReg')

    pw_hash = bcrypt.generate_password_hash(request.form['pw'])
    
    data = {
        **request.form,
        'pw' : pw_hash
    }

    user_id = User.create(data)
    
    session['uuid'] = user_id


    return redirect('/')


@app.route('/login', methods=['post'])
def login():
    if not User.validate_login(request.form):
        return redirect('/loginReg')
    
    return redirect('/')
