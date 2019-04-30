import hashlib

from . import app, db
from flask import render_template, g, redirect, url_for, request, jsonify, flash
import json
import requests
from .models import *
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/api/sign_up/', methods=['GET', 'POST'])
def signup():
    """
    Implements signup functionality. Allows username, email and password for new user.
    Hashes password with salt using werkzeug.security.
    Stores username and hashed password inside database.
    Username should to be unique else raises sqlalchemy.exc.IntegrityError.
    """

    if request.method == "POST":
        username = request.json['username']
        password = request.json['password']
        email = request.json['email']

        if not (username and password and email):
            return jsonify({}), 301
        else:
            username = username.strip()
            password = password.strip()

        # Returns salted pwd hash in format : method$salt$hashedvalue
        hashed_pwd = generate_password_hash(password, 'sha256')

        new_user = User(username=username, pass_hash=hashed_pwd, email=email)
        db.session.add(new_user)

        try:
            db.session.commit()
        except Exception as e:
            return jsonify({}), 301

        print('sign_up OK')
        return jsonify({'token': username})

    return jsonify({}), 301


@app.route('/api/sign_in/', methods=['POST'])
def signin():
    """
    Implements signin functionality.
    """
    if request.method == "POST":
        username = request.json['username']
        password = request.json['password']

        if not (username and password):
            return jsonify({}), 301
        else:
            username = username.strip()
            password = password.strip()

        # Returns salted pwd hash in format : method$salt$hashedvalue
        hashed_pwd = generate_password_hash(password, 'sha256')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.pass_hash, password):
            session[username] = True
            return jsonify({'token': username})
        else:
            return jsonify({}), 301
    return jsonify({}), 301


@app.route('/api/sign_out', methods=['POST'])
def signout():
    """
    Implements signout functionality.
    """

    return jsonify({}), 200


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")
