from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/qsvm/', methods=["POST", "GET"])
def qsvm():
    datos = ['Red', 'Blue', 'Black', 'Orange']
    return render_template('qsvm.html', datos=datos)


@app.route('/qnn/', methods=["POST", "GET"])
def qnn():
    datos = ['Red', 'Blue', 'Black', 'Orange']
    return render_template('qnn.html', datos=datos)


@app.route('/ejecucion', methods=["POST", "GET"])
def ejecucion():
    dispositivos = ['Red1', 'Blue2', 'Black3', 'Orange4']
    if request.method == 'GET':
        datos = request.args.get('datos')
        tipoEjecucion = request.args.get('tipoEjecucion')
    else:
        tipoEjecucion = "Local"
        datos = "básico"
    return render_template('ejecucion.html', datos=datos, tipoEjecucion=tipoEjecucion, dispositivos=dispositivos)
