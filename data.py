from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://b12ca07045f6b4:ecd9bf61@us-cdbr-iron-east-05.cleardb.net/heroku_fac9af395886b6b'
db = SQLAlchemy(app)

# class for the database model of the app


class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(80))
    body = db.Column(db.Text, nullable=False)
    create_date = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.username


article1 = Articles(title='How red 5 was founded',
                    author='chucky', body="Danston Mugarura a global business expert of Ugandan – British descent\
                    He is an accomplished serial entrepreneur and a self-made millionaire.He founded Red Five ")


# db.session.add(article1)
db.session.add(article1)
db.session.commit()
