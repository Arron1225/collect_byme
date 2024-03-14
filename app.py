from flask import Flask ,render_template, url_for, redirect,request
app = Flask(__name__)
# @app.route("/")
# def hello():
#     return "Hello, World!"

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.debug = True
    app.run()