from datetime import timedelta

from flask import Flask, render_template, redirect, url_for, request
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required

from controllers.auth_controllers import auth

import models.user as user_db

import config.secrets as secrets


app = Flask(__name__)
app.secret_key = secrets.APP_SECRET
app.config['JWT_SECRET_KEY'] = secrets.JWT_SECRET
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=4)


jwt = JWTManager(app)


@jwt.unauthorized_loader
def custom_unauthorized_response(_err):
    return redirect(url_for('auth.login'))


@jwt.expired_token_loader
def custom_expired_token_response(jwt_header, jwt_payload):
    return redirect(url_for('auth.login'))


@app.route('/')
def home():
    return "Home"


@app.route('/profile')
@jwt_required(locations='cookies')
def profile():
    user = get_jwt_identity()

    user_data = user_db.get_user_details(user['sub'], user['role'])
    
    if user['role'] == "donar":
        return render_template('profile_donar.html', user=user_data)
    elif user['role'] == "hospital":
        return render_template('profile_hospital.html', user=user_data)


@app.route('/findblood', methods=['GET', 'POST'])
def find_blood():
    if request.method == "GET":
        return render_template('find_blood.html')
    elif request.method == "POST":
        blood = request.form.get('blood')
        state = request.form.get('state')
        district = request.form.get('district')

        donars = user_db.find_donars(blood, state, district)
        hospitals = user_db.find_hospitals(state, district)

        return render_template("find_blood.html", donars=donars, hospitals=hospitals)


# Register Blueprints
app.register_blueprint(auth, url_prefix="/auth")


if __name__ == "__main__":
    app.run(debug=True)
