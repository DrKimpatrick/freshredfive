from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
#from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from wtforms.validators import DataRequired
from passlib.hash import pbkdf2_sha256
from functools import wraps

app = Flask(__name__)
#Articles = Articles()

# config mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'chuck'
app.config['MYSQL_PASSWORD'] = 'sudo'
app.config['MYSQL_DB'] = 'auth'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# session key

app.secret_key = 'my secret'


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)

        else:
            flash("Unauthorised please log in", 'danger')
            return redirect(url_for('login'))
    return wrap

# index route


@app.route('/')
def index():
    return render_template('home.html')

# about route


@app.route('/about')
def about():
    return render_template('about.html')


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


@app.route('/article/<string:id>/')
def article(id):
    cur = mysql.connection.cursor()

    # get articles
    result = cur.execute("SELECT * FROM articles WHERE  id = %s", [id])
    articles = cur.fetchone()
    return render_template('article.html', articles=articles)
    cur.close()


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


# register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = pbkdf2_sha256.hash(str(form.password.data))

        # create the db cursor

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name,email,username,password) VALUES(%s, %s, %s, %s)",
                    (name, email, username, password))

        # commit to db
        mysql.connection.commit()

        # close connection
        cur.close()

        flash('You are now registered and can Login', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# login route


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # get form fields user name and password
        username = request.form['username']
        password_candidate = request.form['password']

        # create db cursor
        cur = mysql.connection.cursor()

        # get user name
        result = cur.execute(
            "SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            # get the stored hash
            data = cur.fetchone()
            password = data['password']

            # comapare the passwords
            if pbkdf2_sha256.verify(password_candidate, password):
                #app.logger.info('password matched')
                # passed passwords
                session['logged_in'] = True
                session['username'] = username
                flash('You are now logged in', 'success')
                return redirect('dashboard')

            else:
                #app.logger.info('no user')
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # close db connection
            cur.close()
        else:
            error = 'User not Found'
            return render_template('login.html', error=error)

    return render_template('login.html')


# about log out
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('index'))

# dashboard


@app.route('/dashboard')
@is_logged_in
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


class ArticleForm(Form):
    title = StringField('Name', validators=[
                        DataRequired(), validators.Length(min=4, max=250)])
    body = TextAreaField('Username', validators=[
                         DataRequired(), validators.Length(min=30)])



#edit article
@app.route('/edit_article/<string:id>', methods=["GET", "POST"])
@is_logged_in
def edit_article(id):
    #create cursor
    cur = mysql.connection.cursor()

    #get article by id
    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])
    article = cur.fetchone()

    #get the form
    form = ArticleForm(request.form)

    form.title.data = article['title']
    form.body.data = article['body']

    #fill the form of the fields


    if request.method == "POST" and form.validate():
        title = request.form['title']
        body = request.form['body']

        # create cursor to the db
        cur = mysql.connection.cursor()

        # execute
        cur.execute("UPDATE  articles SET title=%s,body=%s WHERE id=%s",(title,body,id))


        # commit to db
        mysql.connection.commit()

        # close connection
        cur.close()

        flash('Article Created', 'success')
        return redirect(url_for('dashboard'))

    return render_template('edit_article.html', form=form)



#delete articles
@app.route('/delete_article/<string:id>', methods=['GET','POST'])
@is_logged_in
def delete_article(id):
    #create db cursor
    cur = mysql.connection.cursor()

    #Execute
    cur.execute("DELETE FROM articles WHERE id=%s",[id])

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


if __name__ == '__main__':
    app.run(debug=True)
