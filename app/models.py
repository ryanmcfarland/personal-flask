from hashlib import md5
from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login

class Grocery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Grocery %r>' % self.name

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    sheets = db.relationship('Sheet', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Sheet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    character_class = db.Column(db.String(128))
    background = db.Column(db.String(128))
    level = db.Column(db.Integer)
    xp = db.Column(db.Integer)
    max_hp = db.Column(db.Integer)
    current_hp = db.Column(db.Integer)
    attack_bonus = db.Column(db.Integer)
    system_strain = db.Column(db.Integer)
    ac1 = db.Column(db.Integer)
    ac2 = db.Column(db.Integer)
    mental_save = db.Column(db.Integer)
    evasion_save = db.Column(db.Integer)
    physical_save = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def process_form(self, form):
        self.name=form.name.data
        self.character_class=form.character_class.data
        self.background=form.background.data
        self.level=form.level.data
        self.xp=form.xp.data
        self.max_hp=form.max_hp.data
        self.current_hp=form.current_hp.data
        self.attack_bonus=form.attack_bonus.data
        self.system_strain=form.system_strain.data
        self.ac1=form.ac1.data
        self.ac2=form.ac2.data
        self.mental_save=form.mental_save.data
        self.physical_save=form.physical_save.data
        self.evasion_save=form.evasion_save.data

    def __repr__(self):
        return '<Sheet {}>'.format(self.name)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))