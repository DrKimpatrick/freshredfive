# just write the scrapper with in this script bro.
from flask import Flask, render_template
app = Flask(__name__)




@app.route('/', methods=['GET'])
def index():
    # for item in agric_prices:
    return  render_template('index.html')



@app.route('/dinnershow')
def dinnershow():
    return render_template('dinnershow.html')


if __name__ == '__main__':
    app.run(debug=True)
