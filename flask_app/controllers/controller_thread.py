import re
from unittest import removeResult
from flask import render_template, redirect, request, session, flash, jsonify
from flask_app import app
from flask_app.models.model_user import User
from flask_app.models.model_thread import Thread
from flask_app.models.model_comment import Comment


@app.route('/community')
def show_all_threads():
    threads = Thread.get_all_threads_with_user()

    return render_template('community.html', threads=threads)


@app.route('/threads/<int:id>')
def show_one_thread(id):

    data = {
        'id': id
    }

    if 'thread_id' not in session:
        session['thread_id'] = data['id']
    else:
        del session['thread_id']
        session['thread_id'] = data['id']


    user = Thread.get_one_thread(data)
    comment = Comment.get_all_comments_with_thread()

    return render_template('/thread.html', user=user, comment=comment)


@app.route('/threads/form')
def new_thread():
    if 'uuid' not in session:
        return redirect('/loginReg')

    return render_template('create.html')

@app.route('/threads/create', methods=['post'])
def create_thread():
    if 'uuid' not in session:
        return redirect('/loginReg')


    data = {
        **request.form,
        'user_id' : session['uuid']
    }

    if not Thread.validate_thread(data):
        return redirect ('/threads/form')

    Thread.create_thread(data)

    return redirect('/community')


@app.route('/comments/create', methods=['post'])
def create_comment():
    if 'uuid' not in session:
        return redirect('/loginReg')

    if not Comment.validate_comment(request.form):
        return redirect (f"threads/${session['thread_id']}")

    data = {
        **request.form,
        'user_id' : session['uuid'],
        'thread_id' : session['thread_id']
    }

    id = Comment.create_comment(data)

    comment = Comment.get_one_comment({'id' : id })

    msg = {
        'message' : 'success',
        'content' : {
        'id' : comment.id,
        'content' : comment.content
        }
    }

    return jsonify(msg)


@app.route('/threads/<int:id>/update')
def update_one(id):
    if 'uuid' not in session:
        return redirect('/')

    data = {
        'id' : id
    }

    if 'thread_id' not in session:
        session['thread_id'] = data['id']
    else:
        del session['thread_id']
        session['thread_id'] = data['id']
    
    thread = Thread.get_one_thread(data)

    return render_template('update.html', thread=thread)


@app.route('/threads/update', methods=['post'])
def update_one_thread():
    if 'uuid' not in session:
        return redirect('/loginReg')

    data = {
        'id' :session['thread_id'],
        **request.form
    }
    if not Thread.validate_thread(data):
        return redirect (f"/threads/{session['thread_id']}/update")

    Thread.update_one_thread(data)

    return redirect (f"/threads/{session['thread_id']}")


@app.route('/threads/<int:id>/delete')
def delete_one_thread(id):
    if 'uuid' not in session:
        return redirect('/loginReg')

    data = {
        'id' : id
    }

    Thread.delete_one_thread(data)

    return redirect ('/community')


@app.route('/comments/<int:id>/delete')
def delete_one_comment(id):
    if 'uuid' not in session:
        return redirect('/loginReg')

    data = {
        'id' : id
    }

    Comment.delete_one_comment(data)

    return redirect ('/community')