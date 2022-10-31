from flask import Flask, render_template

app = Flask(__name__)
app.static_folder = "/Users/jaeheon/Desktop/Dev/uzu/static"

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/single.html')
def single():
    return render_template("single.html")


@app.route('/index.html')
def index_2():
    return render_template('index.html')


@app.route('/contact.html')
def contact():
    return render_template('contact.html')


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port="5000", debug=True)
