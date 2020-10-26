import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db
from flaskr.db import query_db
import re

bp = Blueprint('auth', __name__, url_prefix='/auth')


import re
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif len(password) < 8:
            error = 'Password Must Have Length of 8'
        elif len(password) >= 8:
            nUpper = nLower = nAlphanum = 0
            regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
            for c in password:
                if c.isupper():
                    nUpper += 1
                if c.islower():
                    nLower += 1
                if c.isalpha():
                    nAlphanum += 1
            if nUpper == 0:
                error = 'Password must include 1 Upper Case leter'
            if nLower == 0:
                error = 'Password must include 1 Lower Case Letter'
            if nAlphanum == 0:
                error = 'Password must include 1 Numeric digit'
            if regex.search(password) == None:
                error = 'Password must include 1 Special Character 1'
        if query_db(
            'SELECT ID FROM usertemp WHERE username = %s', (username,)
        ).fetchfirst() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            prehash = password+username
            query_db(
                'INSERT INTO usertemp (username, password) VALUES (%s, %s)',
                (username, generate_password_hash(prehash), )
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        prehash = password+username
        db = get_db()
        error = None
        user = query_db(
            'SELECT * FROM usertemp WHERE username = %s', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], prehash):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = query_db(
            'SELECT * FROM usertemp WHERE id = %s', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view