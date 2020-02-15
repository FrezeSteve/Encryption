
from .app import db
from sqlalchemy import Column, Integer, DateTime, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
from uuid import uuid4


# Accounts
class Anonymous(db.Model):
    id = Column(Integer, primary_key=True)
    session_id = Column(Text, unique=True, index=True, nullable=False)
    session_token = Column(Text, unique=True)
    create_date = Column(DateTime(), default=datetime.utcnow)
    last_login = Column(DateTime(), default=datetime.utcnow, nullable=False)

    def __init__(self, token, session_id):
        self.session_token = token
        self.session_id = session_id

    def __repr__(self):
        return f"<Anonymous '{self.session_id}'>"


class User(db.Model):
    id = Column(Text, primary_key=True, unique=True, index=True, nullable=False, default=uuid4)
    username = Column(String(120), unique=True, index=True, nullable=False)
    password = Column(String(120), unique=True, nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)

    admin = Column(Boolean, nullable=False, default=False)
    active = Column(Boolean, nullable=False, default=True)
    authenticated = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime(), default=datetime.utcnow)
    last_login = Column(DateTime(), default=datetime.utcnow)

    token = relationship('Token', uselist=False, backref="auth")

    def __init__(self, username, email, password):
        self.public_id = str(uuid4())
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def __repr__(self):
        return f"User<'{self.username}'>"


class Token(db.Model):
    id = Column(Text, primary_key=True, unique=True, index=True, nullable=False, default=uuid4)
    token = Column(Text, unique=True, index=True, nullable=False)
    expiration = Column(DateTime(), default=datetime.utcnow)
    user = Column(Integer, ForeignKey('user.id'), nullable=False)

    def __init__(self, token, user_id):
        self.token = token
        self.expiration = datetime.utcnow() + timedelta(hours=24)
        self.user = user_id

    def __repr__(self):
        return f"<Token '{self.user}'>"
