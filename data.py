'''def Articles():
    articles = [
    {
        'id':1,
        'title':'Article 1',
        'body':'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Asperiores, blanditiis sed molestias illo rerum hic ad ullam, excepturi quasi cupiditate vel! Incidunt illo consectetur fugit repudiandae, et a perferendis magnam.',
        'author':'chucky',
        'create_date':'20-11-2017'
    },
    {
        'id':2,
        'title':'Article 2',
        'body':'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Asperiores, blanditiis sed molestias illo rerum hic ad ullam, excepturi quasi cupiditate vel! Incidunt illo consectetur fugit repudiandae, et a perferendis magnam.',
        'author':'Bozics',
        'create_date':'21-11-2017'
    },
    {
        'id':3,
        'title':'Article 3',
        'body':'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Asperiores, blanditiis sed molestias illo rerum hic ad ullam, excepturi quasi cupiditate vel! Incidunt illo consectetur fugit repudiandae, et a perferendis magnam.',
        'author':'Mobby',
        'create_date':'24-11-2017'
    }

    ]

    return articles

'''
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

admin = User('admin', 'admin@example.com')

if __name__ == '__main__':
    app.run(debug=True)

