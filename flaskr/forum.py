from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
from flaskr.db import query_db
bp = Blueprint('forum', __name__)

@bp.route('/')
def index():
    #db = get_db()  
    categories = query_db('SELECT id, * FROM category;')
    return render_template('forum/index.html', categories = categories)

@bp.route('/category/<int:category_id>')
def category(category_id):
    session["category_id"]=category_id
    #db = get_db()
    threads = query_db(
        'SELECT id, * FROM thread WHERE category_id=%s;',(category_id, ))
    return render_template('forum/threads.html', threads = threads)

@bp.route('/category/<int:category_id>/thread/<int:thread_id>')
def thread(thread_id,category_id):
    session["thread_id"]=thread_id
    #db = get_db()
    posts = query_db(
        'SELECT id, * FROM post WHERE thread_id=%s', (thread_id, ))
    return render_template('forum/posts.html', posts=posts, thread_id=thread_id)

@bp.route('/posts')
def posts():
    #db = get_db()
    posts = query_db(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN usertemp u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    )
    return render_template('forum/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        if "thread_id" in session:
            thread_id = session["thread_id"]
        if "category_id" in session:
            category_id = session["category_id"]
        error = None
        if not body:
            error = 'Body is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            query_db(
                'INSERT INTO post (body, author_id, thread_id)'
                ' VALUES ( %s, %s, %s)',
                (body, g.user['id'],thread_id, )
            )
            db.commit()
            return redirect(url_for('forum.thread', category_id=category_id, thread_id=thread_id))

    return render_template('forum/create.html')

def get_post(id, check_author=True):
    #db = get_db()
    post = query_db(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN usertemp u ON p.author_id = u.id'
        ' WHERE p.id = %s',
        (id,), True)

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        if "thread_id" in session:
            thread_id = session["thread_id"]
        if "category_id" in session:
            category_id = session["category_id"]
        body = request.form['body']
        error = None
        if not body:
            error = 'Body is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            query_db(
                'UPDATE post SET body = %s'
                ' WHERE id = %s',
                (body, id, )
            )
            db.commit()
            return redirect(url_for('forum.thread', category_id=category_id, thread_id=thread_id))

    return render_template('forum/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    if "thread_id" in session:
        thread_id = session["thread_id"]
    if "category_id" in session:
        category_id = session["category_id"]
    get_post(id)
    db = get_db()
    query_db('DELETE FROM post WHERE id = %s', (id,))
    db.commit()
    return redirect(url_for('forum.thread', category_id=category_id, thread_id=thread_id))
