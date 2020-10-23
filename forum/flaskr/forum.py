from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('forum', __name__)

@bp.route('/')
def index():
    db = get_db()
    categories = db.execute('SELECT rowid, * FROM category;')
    return render_template('forum/index.html', categories = categories)

@bp.route('/category/<int:category_id>')
def category(category_id):
    db = get_db()
    threads = db.execute(
        'SELECT rowid, * FROM thread;')
    return render_template('forum/threads.html', threads = threads)

@bp.route('/category/<int:category_id>/thread/<int:thread_id>')
def thread(thread_id,category_id):
    db = get_db()
    category = db.execute(
        'SELECT * FROM thread WHERE id=?;', (str(thread_id)))
    return render_template('forum/posts.html')

@bp.route('/posts')
def posts():
    db = get_db()
    posts = db.execute(
        'SELECT p.id,  body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('forum/posts.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        body = request.form['body']
        error = None

       

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (body, author_id)'
                ' VALUES ( ?, ?)',
                (body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('forum.posts'))

    return render_template('forum/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

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
        
        body = request.form['body']
        error = None


        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET , body = ?'
                ' WHERE id = ?',
                ( body, id)
            )
            db.commit()
            return redirect(url_for('forum.posts'))

    return render_template('forum/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('forum.posts'))