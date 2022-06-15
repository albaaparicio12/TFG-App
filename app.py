from flask import Flask, render_template, request

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
    dispositivos = ['statevector (32 qubits)', 'ibmq_qasm (32 qubits)', 'extended_stabilizer (63 qubits)', 'mps (100 qubits)', 'stabilizer (5000 qubits)']
    if request.method == 'GET':
        datos = request.args.get('datos')
        tipoEjecucion = request.args.get('tipoEjecucion')
    else:
        tipoEjecucion = "Local"
        datos = "básico"
    return render_template('ejecucion.html', datos=datos, tipoEjecucion=tipoEjecucion, dispositivos=dispositivos)

@app.route('/resumen', methods=["POST", "GET"])
def resumen():
    return render_template('resumen.html')