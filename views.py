from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from base64 import urlsafe_b64encode
from os import environ
from dotenv import load_dotenv
from flask_restful import Resource, reqparse
from werkzeug.security import check_password_hash
from datetime import timedelta, datetime
from . import models
from .app import db, app
import jwt


load_dotenv()


def get_key(password):
    digest = hashes.Hash(hashes.SHA512_256(), backend=default_backend())
    digest.update(password)
    return urlsafe_b64encode(digest.finalize())


encoded_password = environ.get('PASSWORD').encode()
key = get_key(encoded_password)
cipher_text = Fernet(key)


class Login(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.time_to_exp = timedelta(hours=24)

    def post(self):
        self.parser.add_argument('login', type=dict, help="login credentials are needed")
        args = self.parser.parse_args()
        login = args['login']
        if login is not None:
            # required fields is email and password
            email = login.get("email", None)
            if email is None or len(email) <= 7:
                return {"error": "email is invalid or empty"}, 400
            if "@" not in email or "." not in email:
                return {"error": "enter a valid email"}, 400
            password = login.get("password", None)
            if password is None or len(password) <= 7:
                return {"error": "Invalid login credentials"}, 401
            qs = models.User.query.filter_by(email=email).first()
            if qs is None:
                return {'error': "Invalid login credentials"}, 401
            elif qs is not None:
                if check_password_hash(qs.password, password):
                    time_exp = datetime.utcnow() + self.time_to_exp
                    token = jwt.encode({'public_id': qs.public_id, 'exp': time_exp}, app.config['SECRET_KEY'], 'HS512')
                    # check whether the current user is in the token table
                    qs.last_login = datetime.utcnow()
                    db.session.add(qs)
                    user = qs.token
                    if user is None:
                        # Add the token to the token table
                        db.session.add(models.Token(token.decode('UTF-8'), qs.id))
                        db.session.commit()
                    else:
                        user.token = token.decode('UTF-8')
                        user.expiration = time_exp
                        db.session.commit()
                    encrypted_token = cipher_text.encrypt(token)
                    return {'Token': encrypted_token.decode("UTF-8")}
                else:
                    return {"error": "Invalid login credentials"}, 401
        else:
            return {"error": "Invalid login credentials"}, 401


