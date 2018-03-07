
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
#from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from wtforms.validators import DataRequired
from passlib.hash import pbkdf2_sha256
from functools import wraps

from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message



app = Flask(__name__)
#Articles = Articles()

# config mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
#db = SQLAlchemy(app) 


# config for the email's
app.config.update(
    DEBUG=True,
    # email settings
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='fivered24',
    MAIL_PASSWORD='fivered#@'
)

mail = Mail(app)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'chuck'
app.config['MYSQL_PASSWORD'] = 'sudo'
app.config['MYSQL_DB'] = 'auth'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


mysql = MySQL(app)

# session key

app.secret_key = '\x1c\x940h\xb1\xe3\xf6\x17\xa8.n\x17\xbd{$A\xea\xa3h9v\xa4[\xaf'


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)

        else:
            flash("Unauthorised please log in", 'danger')
            return redirect(url_for('login'))
    return wrap

# index sendmail


@app.route('/sendmail')
def sendmail():
    try:
        msg = Message("Trying out the send mail for red5",
                      sender="fivered24@gmail",
                      recipients=['bozicslxye1@gmail.com', 'sekitocharlse@gmail.com'])
        msg.body = "Yo!\n  The mail feature is still being worked on"
        msg.html = " <P> "
        return 'Mail sent'
    except Exception as e:
        return str(e)


# index route
@app.route('/')
def index():
    return render_template('index.html')

# index recipes


@app.route('/recipes')
def recipes():
    return render_template('recipes.html')


# index lunchbox
@app.route('/lunchbox')
def lunchbox():
    return render_template('lunchbox.html')

# index dinnershow


@app.route('/dinnershow')
def dinnershow():
    return render_template('dinnershow.html')

# index cookschool


@app.route('/cookschool')
def cookschool():
    return render_template('cookschool.html')

# index openhouse


@app.route('/openhouse')
def openhouse():
    return render_template('openhouse.html')


'''
# index article
@app.route('/article')
def article():
    return render_template('article.html')
'''

# usageclub


@app.route('/usageclub')
def usageclub():
    return render_template('usageclub.html')

# life changing route


@app.route('/lifechanging')
def lifechanging():
    return render_template('lifechanging.html')


# layout route


@app.route('/layout')
def layout():
    return render_template('layout.html')


# about route
@app.route('/about')
def about():
    return render_template('about.html')

# creating forms


'''
class RegisterForm(Form):
    name = StringField('Name', validators=[
                       DataRequired(), validators.Length(min=4, max=25)])
    username = StringField('Username', validators=[
                           DataRequired(), validators.Length(min=4, max=25)])
    email = StringField('Email', validators=[
                        DataRequired(), validators.Length(min=8, max=25)])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     validators.Length(min=6, max=25), validators.EqualTo('confirm',
                                                                                                          message='Passwords must match')])
    confirm = PasswordField('Confirm Password')
'''


# login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # get form fields user name and password
        username = request.form['username']
        session['logged_in'] = True
        session['username'] = request.form['username']
        # print(session['username'])
        password_candidate = request.form['password']
        # print(username)
        # print(password_candidate)

        # hard coded username and password
        if username == 'Admin' and password_candidate == "Admin1234":
            flash('You are now logged in', 'success')
            return redirect(url_for('dashboard'))
        else:
            error = 'User not Found'
            return render_template('login.html', error=error)

    return render_template('login.html')


# dashboard
@app.route('/dashboard')
def dashboard():

    # create cursor
    cur = mysql.connection.cursor()

    # get articles
    result = cur.execute("SELECT * FROM articles")
    articles = cur.fetchall()
    if result > 0:
        return render_template('dashboard.html', articles=articles)

    else:
        msg = "No articles where found"
        return render_template('dashboard.html', msg)

    cur.close()


# creating articles form
class ArticleForm(Form):
    title = StringField('Name', validators=[
                        DataRequired(), validators.Length(min=4, max=250)])
    body = TextAreaField('Username', validators=[
                         DataRequired(), validators.Length(min=30)])


# edit article
@app.route('/edit_article/<string:id>', methods=["GET", "POST"])
#@is_logged_in
def edit_article(id):
    # create cursor
    cur = mysql.connection.cursor()

    # get article by id
    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])
    article = cur.fetchone()

    # get the form
    form = ArticleForm(request.form)

    form.title.data = article['title']
    form.body.data = article['body']

    # fill the form of the fields

    if request.method == "POST" and form.validate():
        title = request.form['title']
        body = request.form['body']

        # create cursor to the db
        cur = mysql.connection.cursor()

        # execute
        cur.execute(
            "UPDATE  articles SET title=%s,body=%s WHERE id=%s", (title, body, id))

        # commit to db
        mysql.connection.commit()

        # close connection
        cur.close()

        flash('Article Created', 'success')
        return redirect(url_for('dashboard'))

    return render_template('edit_article.html', form=form)

# delete articles


@app.route('/delete_article/<string:id>', methods=['GET', 'POST'])
#@is_logged_in
def delete_article(id):
    # create db cursor
    cur = mysql.connection.cursor()

    # Execute
    cur.execute("DELETE FROM articles WHERE id=%s", [id])

    # commit to db
    mysql.connection.commit()

    # close connection
    cur.close()

    flash('Article deleted', 'success')
    return redirect(url_for('dashboard'))


@app.route('/add_article', methods=["GET", "POST"])
@is_logged_in
def add_article():
    form = ArticleForm(request.form)

    if request.method == "POST" and form.validate():
        title = form.title.data
        body = form.body.data

        # create cursor to the db
        cur = mysql.connection.cursor()

        # execute
        cur.execute("INSERT INTO articles(title,body,author) VALUES(%s,%s,%s)",
                    (title, body, session['username']))

        # commit to db
        mysql.connection.commit()

        # close connection
        cur.close()

        flash('Article Created', 'success')
        return redirect(url_for('dashboard'))

    return render_template('add_article.html', form=form)


# blog route

@app.route('/blog')
def blog():
    # create cursor
    cur = mysql.connection.cursor()

    # get articles
    result = cur.execute("SELECT * FROM articles")
    articles = cur.fetchall()
    if result > 0:
        return render_template('blog.html', articles=articles)

    else:
        msg = "No articles where found"
        return render_template('articles.html', msg)

    cur.close()

    return render_template('blog.html')


# articles route

@app.route('/articles')
def articles():

    # create cursor
    cur = mysql.connection.cursor()

    # get articles
    result = cur.execute("SELECT * FROM articles")
    articles = cur.fetchall()
    if result > 0:
        return render_template('articles.html', articles=articles)

    else:
        msg = "No articles where found"
        return render_template('articles.html', msg)

    cur.close()

    # return render_template('articles.html',articles=Articles)


# article route
@app.route('/article/<string:id>/')
def article(id):
    cur = mysql.connection.cursor()

    # get articles
    result = cur.execute("SELECT * FROM articles WHERE  id = %s", [id])

    if result > 0:
        article = cur.fetchone()
        return render_template('article.html', article=article)
        cur.close()
    else:
        flash("You the article doesn't exit")
        return redirect(url_for('dashboard'))


# about log out
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
