from flask import Flask, render_template, request
from QMLAlgorithm import QMLAlgorithm

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/qsvm/', methods=["POST", "GET"])
def qsvm():
    datos = ['ad_hoc_data', 'breast_cancer', 'digits', 'gaussian', 'iris', 'wine']
    return render_template('qsvm.html', datos=datos)


@app.route('/qnn/', methods=["POST", "GET"])
def qnn():
    datos = ['ad_hoc_data', 'breast_cancer', 'digits', 'gaussian']
    return render_template('qnn.html', datos=datos)


@app.route('/ejecucion', methods=["POST", "GET"])
def ejecucion():
    dispositivos = ['statevector', 'qasm', 'unitary']
    if request.method == 'GET':
        dataset = request.args.get('dataset')
        tipoEjecucion = request.args.get('tipoEjecucion')
        model = request.args.get('model')
    return render_template('ejecucion.html', dataset=dataset, model=model, tipoEjecucion=tipoEjecucion,
                           dispositivos=dispositivos)


@app.route('/resumen', methods=["POST", "GET"])
def resumen():
    n_executions = request.form['nEjecuciones']
    device = request.form['dispositivo']
    token = request.form['token']
    dataset = request.form['dataset_model'].split(",")[0]
    ml_model = request.form['dataset_model'].split(",")[1]
    salida = run(dataset, device, n_executions, token, ml_model)
    return render_template('resumen.html', salida=salida)


def run(dataset, device, n_executions, token, ml_model):
    print(device)
    execution_type = 'ibm' if device == '' else 'local'

    qml = QMLAlgorithm(dataset, execution_type, ml_model, n_executions, device, token)
    return qml.run()
