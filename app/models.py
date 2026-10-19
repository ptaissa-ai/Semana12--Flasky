from datetime import datetime, timezone
from . import db

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    users = db.relationship('User', backref='role', lazy=True)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

class EmailEnviado(db.Model):
    __tablename__ = 'emails_enviados'
    id = db.Column(db.Integer, primary_key=True)
    destinatario = db.Column(db.String(120), nullable=False)
    assunto = db.Column(db.String(200), nullable=False)
    usuario = db.Column(db.String(80), nullable=False)
    prontuario = db.Column(db.String(30), nullable=False)
    nome_aluno = db.Column(db.String(120), nullable=False)
    data_envio = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))

def create_default_roles():
    for name in ('Administrator', 'Moderator', 'User'):
        if db.session.query(Role).filter_by(name=name).first() is None:
            db.session.add(Role(name=name))
    db.session.commit()
