# just write the scrapper with in this script bro.
from flask import Flask, render_template,request
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    # for item in agric_prices:
    return render_template('index.html')


@app.route('/dinnershow')
def dinnershow():
    return render_template('dinnershow.html')


@app.route('/login')
def login():
    return render_template('login1.html')

@app.route('/datahander', methods=["GET", "POST"])
def data():
    if request.method == "POST":
        values = request.form
        for i in values:
            return i


@app.route('/signup')
def signup():
    return render_template('signup.html')




if __name__ == '__main__':
    app.run(debug=True)
