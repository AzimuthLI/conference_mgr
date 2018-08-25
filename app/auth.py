from flask import (Blueprint, flash, g, redirect, jsonify, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
import functools
from app.models import User_admin

bp = Blueprint('auth', __name__, url_prefix='/auth')

# @bp.route('/register', methods=('GET', 'POST'))
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         error = None

#         if not username:
#             error = 'Username is required.'
#         elif not password:
#             error = 'Password is required.'
#         elif User_admin.query.filter_by(username=username).first() is not None:
#             error = 'User {} is already registered.'.format(username)

#         if error is None:
#             user = User_admin(username, generate_password_hash(password))
#             user.save()
#             return jsonify({'register': True, 'user': username, 'error_msg': error})
#         else:
#             return jsonify({'register': False, 'user': username, 'error_msg': error})
#         flash(error)

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = User_admin.query.filter_by(username = username).first()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            response = jsonify({'login': True, 'user': username, 'error_msg': error})
            return response
        else:
            response = jsonify({'login': False, 'error_msg': error})
            response.status_code = 201
            flash(error)
            return response

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User_admin.query.filter_by(id = user_id).first()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view