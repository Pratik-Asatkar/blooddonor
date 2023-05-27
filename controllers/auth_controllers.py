from flask import Blueprint, render_template, request, make_response, redirect
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

import models.user as user_db

import tools.utils as utils

auth = Blueprint('auth', __name__, template_folder="templates")


@auth.route('/login', methods=['GET', 'POST'])
def login(role):
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        phno = request.form.get('phno').strip()
        passwd = request.form.get('passwd').strip()
        role = request.form.get('role').strip()

        user_data = user_db.get_user_details(phno, role)

        if user_data:
            # authenticate user
            if passwd == user_data['passwd']:
                # user auth success

                payload = {
                    "sub": phno,
                    "role": role,
                    "iat": utils.current_epoch()
                }

                access_token = create_access_token(identity=payload)
                resp = make_response(redirect('/'))
                resp.set_cookie('access_token_cookie', access_token)

                return resp
        return render_template('login.html', err="Incorrect Username/Password")


@auth.route('/logout')
@jwt_required(locations='cookies')
def logout():
    user = get_jwt_identity()

    resp = make_response(redirect('/'))
    resp.set_cookie('access_token_cookie', '', expires=0)

    print(f"{user['sub']} has successfully logged out!")

    return resp


@auth.route('/register/<role>', methods=['GET', 'POST'])
def register(role):
    if request.method == 'GET':
        if role == "hospital":
            return render_template('register_hospital.html')
        elif role == "donar":
            return render_template('register_donar.html')
    elif request.method == 'POST':
        phno = request.form.get('phno').strip()

        if role == "hospital":
            data = {
                "_id": phno,
                "role": role,
                "name": request.form.get('org_name').strip(),
                "email": request.form.get('email').strip(),
                "passwd": request.form.get('passwd').strip(),
                "head_name": request.form.get('head_name').strip(),
                "address": request.form.get('address').strip(),
                "state": request.form.get('state').strip(),
                "district": request.form.get('district').strip()
            }
        elif role == "donar":
            data = {
                "_id": phno,
                "role": role,
                "name": request.form.get('name').strip(),
                "email": request.form.get('email').strip(),
                "passwd": request.form.get('passwd').strip(),
                "age": request.form.get('age').strip(),
                "blood": request.form.get('blood').strip(),
                "address": request.form.get('address').strip(),
                "district": request.form.get('district').strip(),
                "state": request.form.get('state').strip(),
                "pincode": request.form.get('pincode').strip()
            }
        
        err = user_db.register(data)
        if err:
            return render_template('register.html', err=err)
        else:
            # login user
            payload = {
                "sub": phno,
                "role": role,
                "iat": utils.current_epoch()
            }

            access_token = create_access_token(identity=payload)
            resp = make_response(redirect('/'))
            resp.set_cookie('access_token_cookie', access_token)

            return resp
