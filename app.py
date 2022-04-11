from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/ejecucion')
def que():
    return render_template('ejecucion.html')
