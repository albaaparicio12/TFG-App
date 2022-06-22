from flask import Flask, render_template, request
from src.base.QMLAlgorithm import QMLAlgorithm
from src.base.Validator import InvalidValueException, InvalidTokenException

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/qsvm/', methods=["POST", "GET"])
def qsvm():
    datos = ['ad_hoc_data', 'breast_cancer', 'gaussian']
    return render_template('qsvm.html', datos=datos)


@app.route('/qnn/', methods=["POST", "GET"])
def qnn():
    datos = ['ad_hoc_data', 'breast_cancer']
    return render_template('qnn.html', datos=datos)


@app.route('/ejecucion', methods=["POST", "GET"])
def ejecucion():
    dispositivos = ['automatic', 'statevector', 'density_matrix', 'matrix_product_state',
                    'unitary', 'superop']
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

    return render_template('resumen.html', salida=salida.values())


@app.route('/documentacion')
def documentacion():
    return render_template('documentacion.html')


@app.route('/contacto')
def contacto():
    return render_template('contacto.html')


def run(dataset, device, n_executions, token, ml_model):
    execution_type = 'ibm' if token != '' else 'local'
    qml = QMLAlgorithm(dataset, execution_type, ml_model, n_executions, device)
    return qml.run(token)


def handle_errors():
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(1000, invalid_token)
    app.register_error_handler(2000, value_error)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', errors=['PAGE NOT FOUND'])


@app.errorhandler(InvalidValueException)
def invalid_token(e):
    return render_template('error.html', errors=[e.message])


@app.errorhandler(InvalidTokenException)
def value_error(e):
    return render_template('error.html', errors=[e.message])
