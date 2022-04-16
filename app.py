from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/qsvm/', methods=["POST","GET"])
def qsvm():
    return render_template('qsvm.html')

@app.route('/qnn', methods=["POST","GET"])
def qnn():
    datos = ['Red', 'Blue', 'Black', 'Orange']
    return render_template('qnn.html', datos=datos)

@app.route('/ejecucion', methods=["POST","GET"])
def ejecucion():
    datos = ['Red', 'Blue', 'Black', 'Orange']
    return render_template('ejecucion.html', datos=datos)

