# -*- coding: utf-8 -*-

from flask import render_template
from flask import send_from_directory
from flask import redirect, url_for
from flask import request

from flask_login import login_required
from flask_login import login_user
from flask_login import current_user
from flask_login import logout_user

from app import app
from app import db

from app import login_manager

from app.models import User
from app.forms import LoginForm


@login_manager.user_loader
def load_user(user_id):
    return db.Session().query(User).get(user_id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/robots.txt')
def get_robots():
    return send_from_directory(app.static_folder, 'robots.txt')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = LoginForm()
    params = {'form': form, 'message': ''}
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        with db.Session() as session:
            user = session.query(User).filter(User.email == email).first()

        if user is None:
            params['message'] = 'Такого пользователя не существует'
            return render_template('login.html', **params)

        if not user.check_password(password):
            params['message'] = 'Некорректный пароль'
            return render_template('login.html', **params)

        login_user(user, remember=True)
        return redirect(url_for('dashboard'))

    return render_template('login.html', **params)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/dashboard')
@login_required
def dashboard():
    params = {'current_user': current_user}
    return render_template('dashboard.html', **params)
