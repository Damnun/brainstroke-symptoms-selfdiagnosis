from flask import Flask, render_template, request

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


@app.route('/checkout.html', methods=['GET', 'POST'])
def checkout():
    if request.method == 'GET':
        return render_template('checkout.html')
    else:
        name = request.form.get('name')
        email = request.form.get('email')
        age = request.form.get('age')
        sex = request.form.get('sex')
        print(name, email, age, sex)
        return "성공"
    return redirect('/')


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port="5000", debug=True)
