import hashlib
from . import app, db
from flask import render_template, g, redirect, url_for, request, jsonify, flash
import json
import requests
from .models import *
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask import send_from_directory
from functools import wraps
import sys
import os
from datetime import date, datetime, timedelta
import jwt
import requests
from PIL import Image
import numpy as np


def create_token(user):
    payload = {
        # subject
        'sub': user.id,
        # issued at
        'iat': datetime.utcnow(),
        # expiry
        'exp': datetime.utcnow() + timedelta(days=1)
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token.decode('unicode_escape')


def parse_token(req):
    token = req.headers.get('Authorization').split()[1]
    return jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.headers.get('Authorization'):
            response = jsonify(message='Missing authorization header')
            response.status_code = 401
            return response
        try:
            payload = parse_token(request)
        except DecodeError:
            response = jsonify(message='Token is invalid')
            response.status_code = 401
            return response
        except ExpiredSignature:
            response = jsonify(message='Token has expired')
            response.status_code = 401
            return response
        user_id = payload['sub']
        try:
            user = User.query.filter_by(id=user_id).first()
        except Exception as e:
            response = jsonify(message='User doesn\'t exist')
            response.status_code = 401
            return response
        return f(user=user, *args, **kwargs)
    return decorated_function


@app.route('/api/sign_up/', methods=['GET', 'POST'])
def signup():
    """
    Implements signup functionality. Allows username, email and password for new user.
    Hashes password with salt using werkzeug.security.
    Stores username and hashed password inside database.
    Username should to be unique else raises sqlalchemy.exc.IntegrityError.
    """

    if request.method == 'POST':
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
        db.session.commit()
        new_user.token = create_token(new_user)
        db.session.commit()

        try:
            db.session.commit()
        except Exception as e:
            return jsonify({}), 301

        print('sign_up OK')
        return jsonify({'token': new_user.token})

    return jsonify({}), 301


@app.route('/api/sign_in/', methods=['POST'])
def signin():
    """
    Implements signin functionality.
    """
    if request.method == 'POST':
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
            user.token = create_token(user)
            return jsonify({'token': user.token})
        else:
            return jsonify({}), 301
    return jsonify({}), 301


@app.route('/api/sign_out/', methods=['POST'])
@login_required
def signout(user):
    """
    Implements signout functionality.
    """
    return jsonify({}), 200


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    try:
        photo = Photo.query.filter_by(filename=filename).first()
    except Exception as e:
        return jsonify(message='File doesn\'t exist'), 301
    #if photo.owner_id != user.id:
    #    return jsonify(message='You don\'t have access to this photo'), 301
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename=filename)


def alpha_composite(front, back):
    front = np.asarray(front)
    back = np.asarray(back)
    result = np.empty(front.shape, dtype='float')
    alpha = np.index_exp[:, :, 3:]
    rgb = np.index_exp[:, :, :3]
    falpha = front[alpha] / 255.0
    balpha = back[alpha] / 255.0
    result[alpha] = falpha + balpha * (1 - falpha)
    old_setting = np.seterr(invalid='ignore')
    result[rgb] = (front[rgb] * falpha + back[rgb] * balpha * (1 - falpha)) / result[alpha]
    np.seterr(**old_setting)
    result[alpha] *= 255
    np.clip(result, 0, 255)
    result = result.astype('uint8')
    result = Image.fromarray(result, 'RGBA')
    return result


def alpha_composite_with_color(image, color=(255, 255, 255)):
    back = Image.new('RGBA', size=image.size, color=color + (255,))
    return alpha_composite(image, back)


@app.route('/api/upload_photo/', methods=['POST'])
@login_required
def upload_photo(user):
    if request.method == 'POST':
        if 'images[]' not in request.files:
            return jsonify({}), 301

        file = request.files['images[]']
        with open('log5.txt', 'w') as f:
            f.write(str(dir(file.headers)))

        if file:
            filename = secure_filename(file.filename)
            photo = Photo(name=filename, owner_id=user.id)
            photo.filename = generate_password_hash(filename + user.username + str(datetime.utcnow()), 'sha256') + '.png'
            photo.path = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename)
            file.save(photo.path)
            db.session.add(photo)
            db.session.commit()
            photo.photo_wo_bg_path = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename[:-4] + '_wobg.png')
            #'''
            response = requests.post(
                'https://api.remove.bg/v1.0/removebg',
                files={'image_file': open(photo.path, 'rb')},
                data={'size': 'auto'},
                headers={'X-Api-Key': 'SNpTGgwghok9jiQ7Ptd1DJFf'},
            )
            if response.status_code == requests.codes.ok:
                with open(photo.photo_wo_bg_path, 'wb') as out:
                    out.write(response.content)
                image = Image.open(photo.photo_wo_bg_path)
                image = alpha_composite_with_color(image)
                image.save(photo.photo_wo_bg_path)
            else:
                with open('log.txt', 'w') as f:
                    f.write('Error:' + str(response.status_code) + str(response.text))
                return jsonify({'api doesn\'t work'}), 505
            #'''
            return jsonify({'success': True, 'error': '',
                            'url': request.url_root[:-1] + url_for('uploaded_file', filename=(photo.filename[:-4] + '_wobg.png')), 'id': photo.id}), 200
            #return jsonify({'success': True, 'error': '',
            #                'url': request.url_root[:-1] + url_for('uploaded_file', filename=(photo.filename)),
            #                'id': photo.id}), 200

        return jsonify({'success': False, 'error': 'nu eto gg', 'url': './'}), 301


@app.route('/api/upload_cropped_photo/', methods=['POST'])
@login_required
def upload_cropped_photo(user):
    if request.method == 'POST':
        if 'images[]' not in request.files or 'photoId' not in request.headers:
            return jsonify({}), 301

        file = request.files['images[]']
        photo_id = request.headers['photoId']

        try:
            photo = Photo.query.filter_by(id=photo_id).first()
        except Exception as e:
            return jsonify({}), 301

        if photo.owner_id != user.id:
            return jsonify({}), 402

        if file:
            photo.cropped_photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename[:-4] + '_cropped.png')
            db.session.commit()
            file.save(photo.cropped_photo_path)
            return jsonify({'success': True, 'error': '',
                            'url': request.url_root[:-1] + url_for('uploaded_file', filename=photo.filename),
                            'id': photo.id}), 200

        return jsonify({'success': False, 'error': 'nu eto gg', 'url': './'}), 301


def get_wh(size, dpi):
    if size == '3см x 4 см':
        width = int(3 / 2.54 * dpi)
        height = int(4 / 2.54 * dpi)
    elif size == '4см x 6см':
        width = int(4 / 2.54 * dpi)
        height = int(6 / 2.54 * dpi)
    return width, height


@app.route('/api/get_final_photo/', methods=['GET'])
@login_required
def create_photo(user):
    size = request.args.get('size')
    paper = request.args.get('paper')
    color = request.args.get('color')
    count = request.args.get('count')
    photo_id = request.args.get('photoId')
    dpi = int(request.args.get('dpi')[:-2])

    try:
        photo = Photo.query.filter_by(id=photo_id).first()
    except Exception as e:
        return jsonify(message=str(e)), 301
    image = Image.open(photo.cropped_photo_path)

    if color == 'Черно-белая':
        image = image.convert('L')
    image = image.resize(get_wh(size, dpi))
    new_photo = Photo(name=(str(datetime.utcnow()) + user.username), filename=(str(datetime.utcnow()) + user.username + '.png'),
                      owner_id=user.id)
    db.session.add(new_photo)
    new_photo.path = os.path.join(app.config['UPLOAD_FOLDER'], new_photo.filename)
    db.session.commit()
    image.save(new_photo.path)
    return jsonify({'success': True, 'error': '', 'url': request.url_root[:-1] +
                                                         url_for('uploaded_file', filename=new_photo.filename)}), 200


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template('index.html')
