# -*- coding: utf-8 -*-

from flask import render_template
from flask import send_from_directory
from flask import request

from app import app
from app import db

from app import login_manager

from app.models import User


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
    if request.method == 'GET':
        return render_template('login.html')
    return ''''''
