# -*- coding: utf-8 -*-

from flask import render_template
from flask import send_from_directory

from app import app


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/robots.txt')
def get_robots():
    return send_from_directory(app.static_folder, 'robots.txt')
