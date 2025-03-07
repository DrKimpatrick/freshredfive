from flask import Flask, render_template, flash, redirect, url_for, session, request, send_file
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from wtforms.validators import DataRequired
from functools import wraps
import random
from flask_mail import Mail, Message

app = Flask(__name__)

app.config.update(
    DEBUG=True,
    # EMAIL SETTINGS
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='inforedfive@gmail.com',
    MAIL_PASSWORD='fcukoff2017'
)
mail = Mail(app)

app.config['MYSQL_HOST'] = 'us-cdbr-iron-east-05.cleardb.net'
app.config['MYSQL_USER'] = 'b12ca07045f6b4'
app.config['MYSQL_PASSWORD'] = 'ecd9bf61'
app.config['MYSQL_DB'] = 'heroku_fac9af395886b6b'
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

# index route


@app.route('/', methods=['GET', "POST"])
def index():
    if request.method == 'POST':
        name = request.form['fullname']
        email = request.form['email']
        num = request.form['tel']
        # create cursor to the db
        cur = mysql.connection.cursor()

        # execute
        cur.execute("INSERT INTO bookregister(name,email,phone) VALUES(%s,%s,%s)",
                    (name, email, num))

        # commit to db
        mysql.connection.commit()

        # close connection
        cur.close()

        # return redirect(url_for('download'))
        return send_file("static/We Change Lives DAnny\'s Book FInal.pdf")
    return render_template('index.html')


# index recipes
@app.route('/download')
def download():
    flash('Thank you for your subscription.', 'success')
    return render_template('download.html')

# index recipes
@app.route('/recipes')
def recipes():
    return render_template('recipes.html')

# index lunchbox
@app.route('/lunchbox')
def lunchbox():
    return render_template('lunchbox.html')

# index dinnershow
# working on the emailing feature of the app.
@app.route('/dinnershow', methods=['POST', 'GET'])
def dinnershow():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        phone1 = request.form['phone']
        phone2 = request.form['phone2']
        email = request.form['email']
        date = request.form['date']
        time = request.form['time']
        allergies = request.form['allergies']
        first_time = request.form['firsttime']
        number_of_adults = request.form['adults']
        number_of_children = request.form['children']
        notes = request.form['notes']
        msg = "Hey i am booking for a dinnershow \nMY names are {} {} and my mobile numbers are {} {}\
        \nMY email is {}\nThe Date and time i am ordering are {} {} \nWe are {} adults and {} children our allergies {}\
        \nOur reservation notes are {} ".format(
            firstname, lastname, phone1, phone2, email, date, time, number_of_adults, number_of_children, allergies, notes)
        # print(msg)
        try:
            msg = Message("Dinnershow Bookings at Eatforlife",
                          sender="inforedfive@gmail.com",
                          recipients=["alice@eatforlife.ug", "alina@eatforlife.ug", "diana@eatforlife.ug", "admin@eatforlife.ug",
                                      "saidat@eatforlife.ug", "bozicslxye1@gmail.com", "alexshyaka@eatforlife.ug"])
            msg.body = "Hey i am booking for a dinnershow. \nMy names are {} {} and my mobile numbers are {} {}.\
            \nMy email is {}.\nThe Date and time i am ordering are {} {}. \nWe are {} adults and {} children our allergies {}.\
            \nOur reservation notes are {} .".format(
                firstname, lastname, phone1, phone2, email, date, time, number_of_adults, number_of_children, allergies, notes)
            mail.send(msg)
            return "<p> thank you for your inquiry, one of the representatives will get back to you in 24 hours./<a href="">Click here to go back</a> </p> "
        except Exception as e:
            return str(e)
    return render_template('dinnershow.html')

# index cookschool


@app.route('/cookschool', methods=['GET', 'POST'])
def cookschool():
    if request.method == "POST":
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        phone1 = request.form['phone']
        phone2 = request.form['phone2']
        email = request.form['email']
        notes = request.form['notes']
        num_of_people = request.form['otherpeople']
        customer_allergies = request.form['allergies']
        try:
            msg = Message("Cookschool Bookings at Eatforlife",
                          sender="inforedfive@gmail.com",
                          recipients=["alina@eatforlife.ug", "admin@eatforlife.ug", "saidat@eatforlife.ug", "diana@eatforlife.ug", "bozicslxye1@gmail.com", "alexshyaka@eatforlife.ug"])
            msg.body = "Hey i am booking for a Cookschool. \nMy names are {} {} and my mobile numbers are {} {}.\
            \nMy email is {}.\nWe are {} people and our allergies {}.\
            \nOur reservation notes are {} .".format(
                firstname, lastname, phone1, phone2, email, num_of_people, customer_allergies, notes)
            mail.send(msg)
            return "<p> Thanks for booking a cookschool <a href="">Click here to go back</a> </p> "
        except Exception as e:
            return str(e)

    return render_template('cookschool.html')

# index openhouse


@app.route('/openhouse', methods=['GET', 'POST'])
def openhouse():
    if request.method == "POST":
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        phone1 = request.form['phone']
        phone2 = request.form['phone2']
        email = request.form['email']
        age = request.form['age']
        working_state = request.form['allergies']
        industry = request.form['industry']
        notes = request.form['notes']
        try:
            msg = Message("Open House Bookings at Eatforlife",
                          sender="inforedfive@gmail.com",
                          recipients=["alina@eatforlife.ug", "admin@eatforlife.ug", "saidat@eatforlife.ug", "priscilla@eatforlife.ug",
                                      "vivian@eatforlife.ug", "bozicslxye1@gmail.com", "alexshyaka@eatforlife.ug"])
            msg.body = "Hey i am booking for a OpenHouse. \nMy names are {} {} and my mobile numbers are {} {}.\
            \nMy email is {}.\nMy age is {} and my working state is {}.\
            \nMy working industry is {} \
            \nMy OpenHouse notes are {} .".format(
                firstname, lastname, phone1, phone2, email, age, working_state, industry, notes)
            mail.send(msg)
            return "<p> Thanks for the  Openhouse reservation <a href="">Click here to go back</a> </p> "
        except Exception as e:
            return str(e)

    return render_template('openhouse.html')


# usageclub
@app.route('/usageclub')
def usageclub():
    return render_template('usageclub.html')

# life changing route
@app.route('/lifechanging')
def lifechanging():
    return render_template('lifechanging.html')

# blog route
@app.route('/blog')
def blog():
    # create cursor
    cur = mysql.connection.cursor()

    # get articles
    result = cur.execute("SELECT * FROM articles ORDER BY create_date DESC")

    articles = cur.fetchall()
    article1 = cur.fetchone()
    random_article = random.choice(articles)
    newest = reversed(articles)

    if result > 0:
        return render_template('blog.html', articles=articles,
                               article=random_article, newest=newest, article1=article1)

    else:
        msg = "No articles where found"
        return render_template('articles.html', msg)

    cur.close()

    return render_template('blog.html', articles=articles)


# about route
@app.route('/about')
def about():
    return render_template('about.html')

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
        return render_template('dashboard.html', msg=msg)

    cur.close()

# register route
@app.route('/registered')
@is_logged_in
def registered():

    # create cursor
    cur = mysql.connection.cursor()
    # get registered users
    register_users = cur.execute("SELECT * FROM bookregister")
    users = cur.fetchall()
    if register_users > 0:
        return render_template('registered.html', users=users)

    else:
        msg = "No users where found"
        return render_template('registered.html', msg=msg)
    cur.close()

# creating articles form
class ArticleForm(Form):
    title = StringField('Title', validators=[
                        DataRequired(), validators.Length(min=4, max=250)])

    image = StringField('Enter Image link', validators=[
                        DataRequired(), validators.Length(min=4, max=250)])

    body = TextAreaField('Body', validators=[
                         DataRequired(), validators.Length(min=30)])


# edit article
@app.route('/edit_article/<string:id>', methods=["GET", "POST"])
@is_logged_in
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
    form.image.data = article['images']

    # fill the form of the fields
    if request.method == "POST" and form.validate():
        title = request.form['title']
        body = request.form['body']
        image = request.form['image']

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
@is_logged_in
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
        image = form.image.data
        # create cursor to the db
        cur = mysql.connection.cursor()

        # execute
        cur.execute("INSERT INTO articles(title,body,author,images) VALUES(%s,%s,%s,%s)",
                    (title, body, session['username'], image))

        # commit to db
        mysql.connection.commit()

        # close connection
        cur.close()

        flash('Article Created', 'success')
        return redirect(url_for('dashboard'))

    return render_template('add_article.html', form=form)

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

        print(result)
        article = cur.fetchone()
        return render_template('article.html', article=article)
        cur.close()
    else:
        flash("The article doesn't exit")
        return redirect(url_for('index'))

# about log out


@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
