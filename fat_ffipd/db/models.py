from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def create_tables(app: Flask, db: SQLAlchemy):
    # noinspection PyUnresolvedReferences
    from fat_ffipd.db.auth.User import User
    # noinspection PyUnresolvedReferences
    from fat_ffipd.db.auth.ApiKey import ApiKey

    with app.app_context():
        db.create_all()
